// Package Parser is responsible for parsing a single schematic file and
// returning the components that it uses
package Parser

import (
	"bufio"
	"kicad-bom-generator/DataTypes"
	"kicad-bom-generator/Errors"
	"kicad-bom-generator/Logger"
	"os"
	"strings"
	"sync"
)

var log = Logger.New()

// activeComponent is a variable representing the current component being parsed
var activeComponent *DataTypes.KiCadComponent

// GetComponentsFromFiles is a function that abstracts away calling GetComponents
// for multiple files
func GetComponentsFromFiles(files []string) []*DataTypes.KiCadComponent {
	mutex := &sync.Mutex{}
	group := sync.WaitGroup{}

	var components []*DataTypes.KiCadComponent // Complete list of components

	for i := range files {
		file := files[i]

		group.Add(1)

		// Go Routine to perform these operations asynchronously
		go func() {
			foundComponents := GetComponents(file)

			// Wait for the mutex to unlock, lock it, add to it and then unlock
			// it for the next go routine that needs it
			mutex.Lock()
			components = append(components, foundComponents...)
			mutex.Unlock()

			group.Done()
		}()
	}

	// Wait for all go routines
	group.Wait()

	return ChangeQuantities(components)
}

// GetComponents is responsible for parsing a schematic file and returning
// a list of components needed to generate a BOM
// Follows the spec for schematics in:
// http://bazaar.launchpad.net/~stambaughw/kicad/doc-read-only/download/head:/1115%4016bec504-3128-0410-b3e8-8e38c2123bca:trunk%252Fkicad-doc%252Fdoc%252Fhelp%252Ffile_formats%252Ffile_formats.pdf/file_formats.pdf
//
func GetComponents(schematicFile string) []*DataTypes.KiCadComponent {
	log.Log("Parsing Schematic File: ", schematicFile)

	var components []*DataTypes.KiCadComponent // List of components found

	for line := range readLine(schematicFile) {
		// Send each line to the component generator to get components
		component := componentGenerator(line)

		// Add a component if one has been found
		if component != nil {
			components = append(components, component)
		}
	}

	return ChangeQuantities(components)
}

// componentGenerator is called when reading lines that define a component
// and it builds the structure to the componet. When fully read then it will
// return that component. Until the line $EndComp is read then this will
// return nil
func componentGenerator(line string) *DataTypes.KiCadComponent {
	// If the line $Comp is read then we need to start a component
	if line == "$Comp" {
		activeComponent = DataTypes.NewKiCadComponent()

		return nil
	}

	// If the line $EndComp is read then we are at the end of a component
	if line == "$EndComp" {
		log.Debug("Parsed Component ", activeComponent.Name)
		activeComponent.Quantity = 1 // Initial Quantity

		cpy := activeComponent
		activeComponent = nil

		return cpy
	}

	// If not $Comp and not $EndComp, but activeCompent is nill then we know
	// that we are not reading a line that deals with a component
	if activeComponent == nil {
		return nil
	}

	// At this point in the function we are parsing a line that specifies
	// a component, handle it and update activeComponent accordingly
	words := strings.Split(strings.TrimSpace(line), " ") // Split at spaces

	// Sanity check
	if len(words) < 3 {
		log.Warn("Found an invalid line when parsing component: ", line)
		activeComponent = nil
		return nil
	}

	switch words[0] {
	// Lines that start with L contain the component name and reference
	case "L":
		activeComponent.Name = stripQuotes(words[1])
		activeComponent.Reference = stripQuotes(words[2])

	// Lines that start with f are other specs about the component
	case "F":
		// F 1... specifies component value
		if words[1] == "1" {
			activeComponent.Value = stripQuotes(words[2])

		} else if words[1] == "2" {
			// F 2... specifies footprints
			footprint := stripQuotes(words[2]) // Remove quotes
			footprintWords := strings.Split(footprint, ":")

			if len(footprintWords) >= 2 {
				activeComponent.FootprintSource = footprintWords[0]
				activeComponent.Footprint = strings.Join(footprintWords[1:len(footprintWords)], ":")
			} else {
				activeComponent.Footprint = footprint
			}
		}
	}

	return nil
}

// ChangeQuantities will accept a list of components, remove duplicates and update
// their quantities to reflect the number of components
func ChangeQuantities(list []*DataTypes.KiCadComponent) []*DataTypes.KiCadComponent {
	log.Verbose("Getting Quantities from parsed component list")

	// finalList is the completed list of components
	var finalList []*DataTypes.KiCadComponent

	// combineWithOthers is a lambda that will look through the list of components
	// and combine ones that are similar with the part passed to it
	combineWithOthers := func(part *DataTypes.KiCadComponent) {
		for i := range list {
			c := list[i]

			// Ignore nils
			if c == nil {
				continue
			}

			// Check if they are the same part (but not the same pointer)
			if part.Equals(c) && part != c {
				// Combine quantity and reference
				part.Combine(c)
				log.Debug("Setting to nil")
				list[i] = nil
			}
		}
	}

	// Loop through the component list
	for i := range list {
		component := list[i]

		// Do not check nil components
		if component == nil {
			continue
		}

		combineWithOthers(component)
		finalList = append(finalList, component)
	}

	return finalList
}

// readLine is a generator that will return the contents of the file line by
// line
func readLine(path string) (c chan string) {
	c = make(chan string)

	go func() {
		file, err := os.Open(path)
		if err != nil {
			close(c)
			(Errors.NewFatal(err.Error())).Handle() // Fatal error and exit
		}

		// Close channel and file when this anonymous function ends
		defer close(c)
		defer file.Close()

		// Begin reading the file
		reader := bufio.NewReader(file)
		for {
			line, err := reader.ReadString('\n') // Read each line
			if err != nil {
				return
			}

			line = strings.TrimSpace(line)
			if line == "" {
				continue // Do not read blank lines
			}

			// Send the file to whatever is reading this channel
			c <- line
		}
	}()

	return c
}

// stripQuotes is a function that will remove the outer most quotes from a string
func stripQuotes(inp string) string {
	inp = strings.TrimSpace(inp)

	if len(inp) >= 2 {
		// Confirm the first and last are quotes
		if (inp[:1] == "\"" && inp[len(inp)-1:] == "\"") || (inp[:1] == "'" && inp[len(inp)-1:] == "'") {
			// Return string without quotes
			return strings.TrimSpace(inp[1 : len(inp)-1])
		}
	}

	return inp // Not wrapped in quotes
}
