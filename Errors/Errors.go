// Package Errors is for handling errors
package Errors

import (
	"kicad-bom-generator/Logger"
	"os"
)

var log = Logger.New()

// ErrorLevel is type that represents the level of error
type ErrorLevel int

// Constants used to represent error levels
const (
	NoError ErrorLevel = iota
	Warning
	Fatal
)

// Error object
type Error struct {
	Level ErrorLevel
	Msg   string
}

// New is a blanket constructor for error messages
// Doesn't set anything specific about the error message
// Returns an error object
func New() Error {
	return *(new(Error))
}

// None is a constructor for when there is no error message
// Returns an error object
func None() Error {
	return New()
}

// NewFatal generates a fatal error message
// Returns an error object
func NewFatal(params ...string) Error {
	err := new(Error)
	err.Level = Fatal

	// Combine parameters into one string as the error message
	for i := range params {
		err.Msg = err.Msg + params[i]
	}

	return *err
}

// NewWarning constructs a new warning message
// Returns an error object
func NewWarning(params ...string) Error {
	err := new(Error)
	err.Level = Warning

	// Combine parameters into one string as the error message
	for i := range params {
		err.Msg = err.Msg + params[i]
	}

	return *err
}

// IsFatal is a member of Error and tells if the error is fatal
// Returns true if the error level is fatal
func (err Error) IsFatal() bool {
	return err.Level == Fatal
}

// HasError is a member of Error and tells if an error is set
// Returns true if the level is set not NoError
func (err Error) HasError() bool {
	return err.Level != NoError
}

// Handle allows an error to be handled, exiting the program if it is fatal
func (err Error) Handle() {
	if err.HasError() {
		if err.IsFatal() {
			// Show the error and exit the program
			log.Error(err.Msg)
			os.Exit(-1)
		}

		// Show the warning but do not exit the program
		log.Warn(err.Msg)
	}
}
