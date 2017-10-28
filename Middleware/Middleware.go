// Package Middleware is for implementing middleware to alter a list before
// sending to the output formatter
package Middleware

import (
	"kicad-bom-generator/DataTypes"
	"kicad-bom-generator/Logger"
	"sort"
)

var log = Logger.New()

// Wrap will apply middleware to a list of components
func Wrap(fn func(components DataTypes.KiCadComponentList) interface{}) DataTypes.ComponentListFn {
	// Return function that applies middleware
	return func(components DataTypes.KiCadComponentList) interface{} {
		// Run through middleware
		components = applyMiddleware(components)

		// Send the components list to the wrapped function
		return fn(components)
	}

}

// applyMiddleware will apply middleware functions to the list of components
func applyMiddleware(components DataTypes.KiCadComponentList) DataTypes.KiCadComponentList {
	components = sortMiddleware(components)

	return components
}

// sortMiddleware will sort a list of components alphabetically by
// reference
func sortMiddleware(components DataTypes.KiCadComponentList) DataTypes.KiCadComponentList {
	log.Verbose("Sorting list of components")
	sort.Sort(components)
	return components
}
