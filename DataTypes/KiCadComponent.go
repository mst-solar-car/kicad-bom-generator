// Package DataTypes is a package containing various data types needed
// Componet is a data type that represents a component
package DataTypes

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
