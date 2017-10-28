// Package Formatters defines formatters to format output
package Formatters

import (
	"fmt"
	"kicad-bom-generator/DataTypes"
	"kicad-bom-generator/Errors"
	"kicad-bom-generator/Logger"
	"kicad-bom-generator/Middleware"
)

// FormatterFunction defines a formatter callback
type FormatterFunction func(components DataTypes.KiCadComponentList) interface{}

var log = Logger.New()

// GetFormatter is a factory that returns a function that can be used to format
// a BOM list
func GetFormatter(excel bool, json bool, csv bool, stdout bool) FormatterFunction {
	// Turn off Excel (since it defaults to true) if another is on
	if json || csv {
		excel = false
	}

	// Warn about excel and STDOUT
	if excel && stdout {
		stdout = false
		log.Warn("Can not send output to STDOUT and use Excel formatting, will not output to STDOUT")
	}

	// Warn about multiple formatters specified
	if json && csv {
		log.Warn("Can only use one formatter, preference is given to JSON over CSV")
	}

	var formatFn FormatterFunction // Function that will be used in the closure

	// Choose a formatting function to return
	if excel {
		log.Verbose("Using the Excel Output Formatter")
		formatFn = formatExcel
	} else if json {
		log.Verbose("Using the JSON Output Formatter")
		formatFn = formatJSON
	} else if csv {
		log.Verbose("Using the CSV Output Formatter")
		formatFn = formatCSV
	} else {
		// Should hopefully never happen
		(Errors.NewFatal("Unkown Formatter -- Output Formatter will not output anything")).Handle()
	}

	return formatterMiddleware(formatFn, json, csv, stdout)
}

// formatterMiddleware is used for modifying the component list before it gets
// sent to the actual formatter
func formatterMiddleware(fn FormatterFunction, json bool, csv bool, stdout bool) FormatterFunction {
	return func(components DataTypes.KiCadComponentList) interface{} {
		// This closure function can be used for any middleware (looking up on Digikey etc)
		components = Middleware.SortMiddleware(components)

		output := fn(components)

		// Print to stdout
		if stdout {
			fmt.Println(output)
		} else {
			if json {
				// TODO: Save to BOM.json
			} else if csv {
				// TODO: Save to BOM.csv
			}
		}

		return output
	}
}
