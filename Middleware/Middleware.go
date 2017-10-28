// Package Middleware is for implementing middleware to alter a list before
// sending to the output formatter
package Middleware

import "kicad-bom-generator/DataTypes"

// SortMiddleware will sort a list of components alphabetically by
// reference
func SortMiddleware(components DataTypes.KiCadComponentList) DataTypes.KiCadComponentList {
	// TODO
	return components
}
