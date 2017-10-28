package Parser

import (
	"kicad-bom-generator/DataTypes"
	"os"
	"testing"
)

// TestParsingASingleFile will parse a single file
func TestParsingASingleFile(t *testing.T) {
	// Assign
	wd, _ := os.Getwd()
	testFile := wd + "/TestFiles/Schematic1.sch"

	expected := []*DataTypes.KiCadComponent{
		makeComponent("Meow", "20K", 1), makeComponent("Meow", "25K", 1),
	}

	// Act
	actual := GetComponents(testFile)

	// Assert
	if len(actual) != len(expected) {
		t.Fatal("Actual does not have the same number of elements as expected")
	}

	for i := range actual {
		found := false

		if actual[i] == nil {
			t.Errorf("Found a nil pointer in actual")
		}

		for j := range expected {
			if actual[i].Equals(expected[j]) {
				found = true
				if actual[i].Quantity == expected[j].Quantity {
					break
				}

				// Mismatch
				t.Errorf("%v (%v) had qty %v instead of %v", actual[i].Footprint, actual[i].Value, actual[i].Quantity, expected[j].Quantity)
			}
		}

		if found == false {
			t.Errorf("%v (%v) was not found in the expected", actual[i].Footprint, actual[i].Value)
		}
	}
}

// makeComponent is a helper function to create a component
func makeComponent(footprint string, value string, qty int) *DataTypes.KiCadComponent {
	return &DataTypes.KiCadComponent{Name: footprint, Footprint: footprint, Value: value, Quantity: qty}
}
