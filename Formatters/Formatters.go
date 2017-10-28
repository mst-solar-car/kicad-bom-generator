// Package Formatters defines formatters to format output
package Formatters

import (
	"kicad-bom-generator/Arguments"
	"kicad-bom-generator/DataTypes"
	"kicad-bom-generator/Errors"
	"kicad-bom-generator/Logger"
	"kicad-bom-generator/Middleware"
	"os"
	"path/filepath"
)

var log = Logger.New()
var args = Arguments.Retrieve()

// GetFormatter is a factory that returns a function that can be used to format
// a BOM list
func GetFormatter() DataTypes.ComponentListFn {
	var formatFn DataTypes.ComponentListFn

	// Choose a formatting function to return
	if args.Excel {
		log.Verbose("Using the Excel Output Formatter")
		formatFn = formatExcel
	} else if args.Json {
		log.Verbose("Using the JSON Output Formatter")
		formatFn = formatJSON
	} else if args.Csv {
		log.Verbose("Using the CSV Output Formatter")
		formatFn = formatCSV
	} else {
		// Should hopefully never happen
		(Errors.NewFatal("Unkown Formatter -- Output Formatter will not output anything")).Handle()
	}

	return Middleware.Wrap(formatWrapper(formatFn))
}

// formatWrapper returns a function that will apply a formatter to a list of components
func formatWrapper(formatter DataTypes.ComponentListFn) DataTypes.ComponentListFn {
	// When this return function is called, components will already have gone through
	// middleware, so send them through the formatter function and do more stuff
	return func(components DataTypes.KiCadComponentList) interface{} {
		output := formatter(components)

		// Save file that is not excel
		if !args.Excel {
			path := filepath.Join(args.Directory, "BOM.")

			if args.Json {
				path = path + "json"
			} else if args.Csv {
				path = path + "csv"
			}

			writeToFile(output, path)
			log.Success("BOM saved to: ", path)
		} else {
			// Show where the excel was saved11
			log.Success("BOM saved to: ", output.(string))
		}

		return output
	}

}

// writeToFile will write data to a file
func writeToFile(data interface{}, path string) {
	file, err := os.Create(path)
	if err != nil {
		(Errors.NewFatal(err.Error())).Handle()
	}

	defer file.Close()

	_, err2 := file.WriteString(data.(string))
	if err2 != nil {
		(Errors.NewFatal(err2.Error())).Handle()
	}
}
