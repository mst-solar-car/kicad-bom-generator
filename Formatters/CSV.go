// Package Formatters defines formatters to format output
package Formatters

import (
	"kicad-bom-generator/DataTypes"
	"strings"
)

// formatCSV formats a component list as CSV
func formatCSV(components DataTypes.KiCadComponentList) interface{} {
	props := DataTypes.GetComponentProperties()

	result := ""

	// Create the headers for the file
	for i := range props {
		result += props[i]

		if i < (len(props) - 1) {
			result += ","
		}
	}
	result += "\n"

	// Add all of the components
	for i := range components {
		component := components[i]

		for j := range props {
			result += strings.Replace(component.Get(props[j]), ",", ";", -1)

			if j < (len(props) - 1) {
				result += ","
			}
		}
		result += "\n" // New line separators
	}

	return result
}
