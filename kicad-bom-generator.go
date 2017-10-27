package main

import (
	"flag"
	"kicad-bom-generator/Errors"
	"kicad-bom-generator/Logger"
	"os"
	"path/filepath"
)

var log = Logger.New()

// main is the main entry point for the program, it is executed when you run
// the program
func main() {
	// Get the current directory to search for KiCad files
	wd, err := os.Getwd()
	if err != nil {
		(Errors.NewFatal(err.Error())).Handle()
	}

	// Command line arguments
	directory := flag.String("dir", wd, "Specify the directory to get files from")
	verbose := flag.Bool("verbose", false, "Enables verbose logging")
	debug := flag.Bool("debug", false, "Enable debugging mode")
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

	getSchematicFilesFrom(*directory)
}

// getSchematicFilesFrom returns a list of all the schematic files in a
// directory (searches recursively)
func getSchematicFilesFrom(dir string) {
	log.Log("Finding KiCad Schematic Files In: ", dir)

	files := getFilesWithExtension(dir, ".sch")

	for i := range files {
		file := files[i]
		log.Info(file)
	}
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
				log.Verbose("Found File: ", path)
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
