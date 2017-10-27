// Package Formatters defines formatters to format output
package Formatters

import (
	"kicad-bom-generator/DataTypes"
	"kicad-bom-generator/Logger"
)

// FormatterFunction defines a formatter callback
type FormatterFunction func(components []*DataTypes.KiCadComponent) interface{}

var log = Logger.New()

// GetFormatter is a factory that returns a function that can be used to format
// a BOM list
func GetFormatter(excel bool, json bool, csv bool) FormatterFunction {
	// Turn off Excel (since it defaults to true) if another is on
	if json || csv {
		excel = false
	}

	// Choose a formatting function to return
	if excel {
		log.Verbose("Using the Excel Output Formatter")
		return formatExcel
	} else if json {
		log.Verbose("Using the JSON Output Formatter")
		return formatJSON
	} else if csv {
		log.Verbose("Using the CSV Output Formatter")
		return formatCSV
	}

	log.Warn("Unkown Formatter -- Output Formatter will not format")
	return func(components []*DataTypes.KiCadComponent) interface{} { return components }
}
