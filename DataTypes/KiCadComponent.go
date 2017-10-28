// Package DataTypes is a package containing various data types needed
// Componet is a data type that represents a component
package DataTypes

import (
	"strconv"
	"strings"
)

// KiCadComponentList is a list of KiCad Components
type KiCadComponentList []*KiCadComponent

// KiCadComponent is a struct that represents a component in KiCad
type KiCadComponent struct {
	Name            string
	Reference       string
	FootprintSource string
	Footprint       string
	Value           string
	Quantity        int
}

// NewKiCadComponent creates a new KiCadComponent
func NewKiCadComponent() *KiCadComponent {
	return &KiCadComponent{Quantity: 0}
}

// Copy is a copy constructor for KiCadComponents
func (component KiCadComponent) Copy() *KiCadComponent {
	newComponent := NewKiCadComponent()
	newComponent.Name = component.Name
	newComponent.Reference = component.Reference
	newComponent.FootprintSource = component.FootprintSource
	newComponent.Footprint = component.Footprint
	newComponent.Value = component.Value
	newComponent.Quantity = component.Quantity

	return newComponent
}

// Equals is a comparison operator between two KiCadComponents
func (component KiCadComponent) Equals(other *KiCadComponent) bool {
	return component.Footprint == other.Footprint &&
		component.FootprintSource == other.FootprintSource &&
		component.Value == other.Value
}

// Combine will combine quantities, and references of two components that
// are the same
func (component *KiCadComponent) Combine(other *KiCadComponent) {
	if component.Equals(other) && component != other {
		component.Reference = component.Reference + ", " + other.Reference
		component.Quantity = component.Quantity + other.Quantity
	}
}

// GetComponentProperties is used by formatters to retrieve the text value
// that should be the header names for each property
// If you do not want a value to show up in the output, do not return it here
// The order returned here is the order that things will go into the output
func GetComponentProperties() []string {
	return []string{"Name", "Reference", "Footprint", "Value", "Quantity"}
}

// Get is used by formatters, the name parameter will be whatever
// value is returned by the GetComponentPropertyNames() function
func (component KiCadComponent) Get(prop string) string {
	switch strings.ToLower(prop) {
	case "name":
		return component.Name
	case "reference":
		return component.Reference
	case "footprint":
		return component.Footprint
	case "value":
		return component.Value
	case "quantity":
		return string(strconv.Itoa(component.Quantity))
	default:
		return ""
	}
}
