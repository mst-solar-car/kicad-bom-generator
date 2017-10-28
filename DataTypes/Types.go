package DataTypes

// ComponentListFn is just a function that accepts a list of components
// and returns anything
type ComponentListFn func(components KiCadComponentList) interface{}
