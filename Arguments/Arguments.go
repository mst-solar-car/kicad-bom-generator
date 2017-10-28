// Package Arguments is a singleton object that will allow all arguments sent
// to this program in the command line be available in any package without
// having to pass as a parameter
package Arguments

import (
	"flag"
	"kicad-bom-generator/Logger"
	"os"
	"sync"
)

var log = Logger.New()

// Arguments is the object to represent arguments
// For every command line argument, there should me a member here
type Arguments struct {
	Directory string
	Verbose   bool
	Debug     bool

	// Formatters
	Excel bool
	Json  bool
	Csv   bool
}

var instance *Arguments
var once sync.Once

// Retrieve is the function to return the singleton argument list
func Retrieve() *Arguments {
	// Only create the instance once
	once.Do(func() {
		wd, _ := os.Getwd()

		// Only retrieve the command line parameters once
		directory := flag.String("dir", wd, "Specify the directory to get files from")
		verbose := flag.Bool("verbose", false, "Enables verbose logging")
		debug := flag.Bool("debug", false, "Enable debugging mode")

		excel := flag.Bool("excel", true, "Format output as an Excel document")
		json := flag.Bool("json", false, "Format output as  JSON")
		csv := flag.Bool("csv", false, "Format output as Comma Separated Values")

		flag.Parse()

		// Only allow one formatter
		if *json || *csv {
			*excel = false
		}

		// Prefer CSV over JSON
		if *json && *csv {
			*json = false
			log.Warn("Only one formatter is allowed, prefering CSV over JSON")
		}

		// Enable verbose on the logger
		if *verbose {
			log.EnableVerbose()
		}

		// Enable debugging in the logger
		if *debug {
			log.EnableDebug()
		}

		// Create the singleton struct
		instance = &Arguments{}
		instance.Directory = *directory
		instance.Verbose = *verbose
		instance.Debug = *debug
		instance.Excel = *excel
		instance.Json = *json
		instance.Csv = *csv
	})
	return instance
}
