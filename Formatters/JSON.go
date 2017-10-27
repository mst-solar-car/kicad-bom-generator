// Package Formatters defines formatters to format output
package Formatters

import (
	"encoding/json"
	"kicad-bom-generator/DataTypes"
)

// formatJSON formats a component list as json
func formatJSON(components []*DataTypes.KiCadComponent) interface{} {
	result, _ := json.Marshal(components)

	return string(result)
}
