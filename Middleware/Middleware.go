// Package Middleware is for implementing middleware to alter a list before
// sending to the output formatter
package Middleware

import (
	"kicad-bom-generator/DataTypes"
	"kicad-bom-generator/Logger"
	"sort"
)

var log = Logger.New()

// SortMiddleware will sort a list of components alphabetically by
// reference
func SortMiddleware(components DataTypes.KiCadComponentList) DataTypes.KiCadComponentList {
	log.Verbose("Sorting list of components")
	sort.Sort(components)
	return components
}
