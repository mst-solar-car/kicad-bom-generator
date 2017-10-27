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
func (component KiCadComponent) Copy(other *KiCadComponent) *KiCadComponent {
	newComponent := NewKiCadComponent()
	newComponent.Name = other.Name
	newComponent.Reference = other.Reference
	newComponent.FootprintSource = other.FootprintSource
	newComponent.Footprint = other.Footprint
	newComponent.Value = other.Value
	newComponent.Quantity = other.Quantity

	return newComponent
}

// Equals is a comparison operator between two KiCadComponents
func (component KiCadComponent) Equals(other *KiCadComponent) bool {
	return component.Footprint == other.Footprint &&
		component.FootprintSource == other.FootprintSource &&
		component.Value == other.Value
}
