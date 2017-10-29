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
	Datasheet       string
	Supplier        string
	SupplierPartNo  string
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
	newComponent.Supplier = component.Supplier
	newComponent.SupplierPartNo = component.SupplierPartNo
	newComponent.Datasheet = component.Datasheet

	return newComponent
}

// Equals is a comparison operator between two KiCadComponents
func (component KiCadComponent) Equals(other *KiCadComponent) bool {
	return component.Footprint == other.Footprint &&
		component.FootprintSource == other.FootprintSource &&
		component.Value == other.Value &&
		component.Supplier == other.Supplier &&
		component.SupplierPartNo == other.SupplierPartNo
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
	return []string{"Name", "Reference", "Footprint", "Value", "Supplier", "Supplier Part Number", "Quantity"}
}

// Get is used by formatters, the name parameter will be whatever
// value is returned by the GetComponentPropertyNames() function
func (component KiCadComponent) Get(prop string) string {
	prop = strings.Replace(strings.ToLower(prop), " ", "_", -1) // Remove spaces

	switch prop {
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
	case "supplier":
		return component.Supplier
	case "supplier_part_number":
		return component.SupplierPartNo
	default:
		return ""
	}
}

// SetCustomField is responsible for determining if the value field is capable of going
// into a component, and then updating accordingly. These are fields that
// are custom, and not defined by the KiCad Spec
func (component *KiCadComponent) SetCustomField(field string, value string) {
	field = strings.Replace(strings.ToLower(field), " ", "_", -1) // Remove spaces
	value = strings.TrimSpace(value)

	if field == "supplier" || field == "supplier_name" {
		component.Supplier = value
	} else if field == "supplier_part_number" || field == "supplier_part" {
		component.SupplierPartNo = value
	} else if field == "datasheet" {
		component.Datasheet = value
	}
}

// CombineComponents will combine the same components
func (list KiCadComponentList) CombineComponents() KiCadComponentList {
	var finalList KiCadComponentList

	// combineWithOthers is a lambda that will look through the list of components
	// and combine ones that are similar with the part passed to it
	combineWithOthers := func(part *KiCadComponent) {
		for i := range list {
			c := list[i]

			// Ignore nils
			if c == nil {
				continue
			}

			// Check if they are the same part (but not the same pointer)
			if part.Equals(c) && part != c {
				// Combine quantity and reference
				part.Combine(c)
				list[i] = nil
			}
		}
	}

	for i := range list {
		component := list[i]

		// Do not check nil components
		if component == nil {
			continue
		}

		combineWithOthers(component)
		finalList = append(finalList, component)
	}

	return finalList
}

// Len is needed for sorting
func (list KiCadComponentList) Len() int {
	return len(list)
}

// Swap will swap two elements in a list
func (list KiCadComponentList) Swap(i int, j int) {
	temp := list[i]

	list[i] = list[j]
	list[j] = temp
}

// Less returns true if index i is less than index j
func (list KiCadComponentList) Less(i int, j int) bool {
	firstRefI := strings.Split(list[i].Reference, ",")[0]
	firstRefJ := strings.Split(list[j].Reference, ",")[0]

	return firstRefI < firstRefJ
}
