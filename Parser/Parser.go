// Package Parser is responsible for parsing a single schematic file and
// returning the components that it uses
package Parser

import (
	"bufio"
	"kicad-bom-generator/DataTypes"
	"kicad-bom-generator/Errors"
	"kicad-bom-generator/Logger"
	"os"
	"regexp"
	"strconv"
	"strings"
	"sync"
)

var log = Logger.New()

// GetComponentsFromFiles is a function that abstracts away calling GetComponents
// for multiple files
func GetComponentsFromFiles(files []string) DataTypes.KiCadComponentList {
	mutex := &sync.Mutex{}
	group := sync.WaitGroup{}

	var components DataTypes.KiCadComponentList // Complete list of components
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

	return components.CombineComponents()
}

// GetComponents is responsible for parsing a schematic file and returning
// a list of components needed to generate a BOM
func GetComponents(schematicFile string) DataTypes.KiCadComponentList {
	log.Log("Parsing Schematic File: ", schematicFile)

	var components DataTypes.KiCadComponentList // List of components found

	generator := componentGenerator() // Get a generator closure

	for line := range readLine(schematicFile) {
		// Send each line to the component generator to get components
		component := generator(line)

		// Add a component if one has been found
		if component != nil {
			components = append(components, component)
		}
	}

	return components.CombineComponents()
}

type componentGeneratorFn func(line string) *DataTypes.KiCadComponent

// componentGenerator returns a function closure that will accept a line of text
// and is called for every line in the file, it will parse each line and build
// a component and return a pointer to that component when one is found
func componentGenerator() componentGeneratorFn {
	var activeComponent *DataTypes.KiCadComponent

	// Return a function that will read in lines and generate components
	return func(line string) *DataTypes.KiCadComponent {
		// The Line $Comp begins the definition of a component
		if line == "$Comp" {
			activeComponent = DataTypes.NewKiCadComponent()
			return nil
		}

		// If the line $EndComp is found then that component definition is over
		if line == "$EndComp" && activeComponent != nil {
			activeComponent.Quantity = 1

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
		parseComponentSpecLine(line, activeComponent)

		return nil
	}
}

// parseComponentSpecLine is responsible for actually parsing a single line and
// pulling out spec information into the component
// It follows the spec outlined in: http://bazaar.launchpad.net/~stambaughw/kicad/doc-read-only/download/head:/1115%4016bec504-3128-0410-b3e8-8e38c2123bca:trunk%252Fkicad-doc%252Fdoc%252Fhelp%252Ffile_formats%252Ffile_formats.pdf/file_formats.pdf
func parseComponentSpecLine(line string, component *DataTypes.KiCadComponent) {
	// Just in case
	line = strings.TrimSpace(line)

	parts := strings.Split(line, " ") // Split apart at spaces

	// Sanity check
	if len(parts) < 3 {
		log.Warn("Found an invalid line when parsing component: ", line)
		component = nil
		return
	}

	// Friendlier names
	spec := strings.ToUpper(parts[0])

	// L name reference
	if spec == "L" {
		component.Name = stripQuotes(parts[1])
		component.Reference = stripQuotes(parts[2])

		return
	}

	// F num "text"
	if spec == "F" {
		num, err := strconv.Atoi(parts[1])
		if err != nil {
			log.Warn("Found an invalid line when parsing component: ", line)
			component = nil
			return
		}

		parts[2] = stripQuotes(parts[2])

		if num == 1 {
			// F 1 "component_value"
			component.Value = parts[2]

		} else if num == 2 {
			// F 2 "component_footprint"
			footprint := parts[2] // Remove quotes
			footprintWords := strings.Split(footprint, ":")

			if len(footprintWords) >= 2 {
				component.FootprintSource = footprintWords[0]
				component.Footprint = strings.Join(footprintWords[1:len(footprintWords)], ":")
			} else {
				component.Footprint = footprint
			}

		} else if num == 3 {
			// F 3 "datasheet_url"
			component.Datasheet = parts[2]

		} else if num > 3 {
			// F >3 "value" a bunch of junk "name"
			reg, _ := regexp.Compile("\"([^\"]*)\"") // Regex to match things inside quotes

			matches := reg.FindAllString(line, -1)

			// Verify that two results were returned
			if len(matches) >= 2 {
				component.SetCustomField(stripQuotes(matches[1]), stripQuotes(matches[0]))
			}
		}
	}
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
