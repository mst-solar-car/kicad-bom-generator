package main

import (
	"flag"
	"kicad-bom-generator/DataTypes"
	"kicad-bom-generator/Errors"
	"kicad-bom-generator/Formatters"
	"kicad-bom-generator/Logger"
	"kicad-bom-generator/Parser"
	"os"
	"path/filepath"
	"sync"
)

var log = Logger.New()

// main is the main entry point for the program, it is executed when you run
// the program
func main() {
	// Get the current directory to search for KiCad files
	wd, errGetwd := os.Getwd()
	if errGetwd != nil {
		(Errors.NewFatal(errGetwd.Error())).Handle()
	}

	// Command line arguments
	directory := flag.String("dir", wd, "Specify the directory to get files from")
	verbose := flag.Bool("verbose", false, "Enables verbose logging")
	debug := flag.Bool("debug", false, "Enable debugging mode")

	stdout := flag.Bool("stdout", false, "Output to stdout instead of a file")
	excel := flag.Bool("excel", true, "Format output as an Excel document")
	json := flag.Bool("json", false, "Format output as  JSON")
	csv := flag.Bool("csv", false, "Format output as Comma Separated Values")

	flag.Parse()

	// Start the output with this super fancy header
	log.Success("=======================================")
	log.Success("          KiCad BOM Generator          ")
	log.Success("    Missouri S&T Solar Car Team 2017   ")
	log.Success("             Michael Rouse             ")
	log.Success("=======================================\n")

	// Enable verbose logging if needed
	if *verbose {
		log.EnableVerbose()
	}

	// Enable debugging mode if needed
	if *debug {
		log.EnableDebug()
	}

	// Get the output formatter
	formatter := Formatters.GetFormatter(*excel, *json, *csv, *stdout)

	log.Log(*directory)
	// Verify that the directory given is home to a KiCad project (*.pro file)
	validDir := checkForKiCadProject(*directory)
	if validDir == false {
		(Errors.NewFatal("Directory does not contain a KiCad Project")).Handle()
	}

	// Get schematic files from the directory
	files, err := getSchematicFilesFrom(*directory)
	err.Handle()

	// Mutex to control access to the components array
	mutex := &sync.Mutex{}
	group := sync.WaitGroup{} // group allows the program to wait until all go routines are finished

	// Parse components from each file
	var components []*DataTypes.KiCadComponent
	for i := range files {
		file := files[i]

		group.Add(1)

		// Go Routine to perform these operations asynchronously
		go func() {
			foundComponents := Parser.GetComponents(file)

			// Wait for the mutex to unlock, lock it, add to it and then unlock
			// it for the next go routine that needs it
			mutex.Lock()
			components = append(components, foundComponents...)
			mutex.Unlock()

			group.Done()
		}()
	}

	// Wait for all the go routines just created to finish
	group.Wait()

	// Adjust quantitiy values after parsing all the files
	components = Parser.ChangeQuantities(components)

	// Finally, we can now format the output
	formatter(components)
}

// getSchematicFilesFrom returns a list of all the schematic files in a
// directory (searches recursively)
func getSchematicFilesFrom(dir string) ([]string, Errors.Error) {
	log.Log("Finding KiCad Schematic Files In: ", dir)

	files := getFilesWithExtension(dir, ".sch")

	if len(files) == 0 {
		return files, Errors.NewWarning("No Schematic Files Found")
	}

	return files, Errors.None()
}

// getFilesWithExtension finds file recursively in a folder with a specific
// extension, since Go filepath.Glob doesn't support recursion
func getFilesWithExtension(directory string, extension string) []string {
	log.Verbose("Looking for files with the extension \"", extension, "\" in ", directory)
	files := []string{}

	err := filepath.Walk(directory, func(path string, file os.FileInfo, err error) error {
		if err != nil {
			log.Error(err.Error())
		}

		if file.IsDir() == false {
			if filepath.Ext(path) == extension {
				// Found a file!
				log.Verbose("Found Schematic: ", path)
				files = append(files, path)
			}
		}

		return nil
	})

	if err != nil {
		(Errors.NewFatal(err.Error())).Handle()
	}

	return files
}

// checkForKiCadProject is responsible for determining if the directory
// given by the user contains a KiCad project
func checkForKiCadProject(directory string) bool {
	log.Verbose("Checking for KiCad Project file in ", directory)
	f, _ := filepath.Glob(filepath.Join(directory, "*.pro"))
	if len(f) == 0 {
		return false
	}

	return true
}
