// Package Formatters defines formatters to format output
package Formatters

import (
	"kicad-bom-generator/DataTypes"

	"github.com/tealeg/xlsx"
)

// formatExcel formats a component list as an Excel document
func formatExcel(components []*DataTypes.KiCadComponent) interface{} {
	file := xlsx.NewFile()
	sheet, _ := file.AddSheet("Sheet 1")

	props := DataTypes.GetComponentProperties()

	// Add all header rows
	row := sheet.AddRow()
	for i := range props {
		cell := row.AddCell()
		cell.Value = props[i]
	}

	// Add all the components
	for i := range components {
		component := components[i]
		row = sheet.AddRow()

		for j := range props {
			cell := row.AddCell()
			cell.Value = component.Get(props[j])
		}
	}

	file.Save("BOM.xlsx")

	return "BOM.xlsx"
}
