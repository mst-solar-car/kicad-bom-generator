// Package Formatters defines formatters to format output
package Formatters

import (
	"kicad-bom-generator/Arguments"
	"kicad-bom-generator/DataTypes"
	"kicad-bom-generator/Errors"
	"kicad-bom-generator/Logger"
	"kicad-bom-generator/Middleware"
)

var log = Logger.New()
var args = Arguments.Retrieve()

// FormatterFunction defines a formatter callback
type FormatterFunction func(components DataTypes.KiCadComponentList) interface{}

// GetFormatter is a factory that returns a function that can be used to format
// a BOM list
func GetFormatter() FormatterFunction {
	var formatFn FormatterFunction

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

	return formatterMiddleware(formatFn)
}

// formatterMiddleware is used for modifying the component list before it gets
// sent to the actual formatter
func formatterMiddleware(fn FormatterFunction) FormatterFunction {
	return func(components DataTypes.KiCadComponentList) interface{} {
		// Run the component list through middleware here
		components = Middleware.SortMiddleware(components)

		output := fn(components)

		if args.Json {
			// TODO: Save to BOM.json
		} else if args.Csv {
			// TODO: Save to BOM.csv
		}

		return output
	}
}
