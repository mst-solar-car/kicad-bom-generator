// Package Logger is used for logging output to the terminal
package Logger

import (
	"sync"

	"github.com/fatih/color"
)

// LogLevel is a variable type to represent a logging level to be used
// by the singleton logger
type LogLevel int

// Constants to represent logging levels
const (
	Verbose LogLevel = iota
	Normal
)

// Logger is a struct to represent the singleton logger object
type Logger struct {
	Level     LogLevel
	Debugging bool
}

var instance *Logger
var once sync.Once

// New is the constructor for the Logger object, it will return the instance
// if one has already been created
func New() *Logger {
	// Create the first Logger object
	once.Do(func() {
		instance = &Logger{Level: Normal, Debugging: false}
	})

	return instance
}

// EnableVerbose enables verbose logging on a logger
func (logger *Logger) EnableVerbose() {
	logger.Level = Verbose

	logger.Warn("Verbose Logging Enabled")
}

// EnableDebug allows for debugging statements to be output
func (logger *Logger) EnableDebug() {
	logger.Debugging = true

	logger.Warn("Debug mode Enabled")
}

// Warn is a member of Logger that outputs a warning message (in yellow)
func (logger Logger) Warn(params ...string) {
	headline := color.New(color.FgYellow, color.Bold)

	msg := "WARNING: "
	for i := range params {
		msg = msg + params[i]
	}

	headline.Println(msg)
}

// Log is a member of Logger that outputs a regular message (in white)
func (logger Logger) Log(params ...string) {
	headline := color.New(color.FgHiWhite)

	msg := ""
	for i := range params {
		msg = msg + params[i]
	}

	headline.Println(msg)
}

// Success is a member function that outputs a message in green
func (logger Logger) Success(params ...string) {
	headline := color.New(color.FgHiGreen)

	msg := ""
	for i := range params {
		msg = msg + params[i]
	}

	headline.Println(msg)
}

// Error is a member function that outputs a message in red
func (logger Logger) Error(params ...string) {
	headline := color.New(color.FgHiRed)

	msg := "ERROR: "
	for i := range params {
		msg = msg + params[i]
	}

	headline.Println(msg)
}

// Verbose is a member function that outputs a regular message when only in
// verbose mode
func (logger Logger) Verbose(params ...string) {
	if logger.Level == Verbose {
		headline := color.New(color.FgWhite)

		msg := ""
		for i := range params {
			msg = msg + params[i]
		}

		headline.Println(msg)
	}
}

// Info prints informative messages out in blue
func (logger Logger) Info(params ...string) {
	headline := color.New(color.FgHiCyan)

	msg := "INFO: "
	for i := range params {
		msg = msg + params[i]
	}

	headline.Println(msg)
}

// Debug is used for debugging statements
func (logger Logger) Debug(params ...string) {
	if logger.Debugging {
		headline := color.New(color.FgHiMagenta)

		msg := "DEBUG: "
		for i := range params {
			msg = msg + params[i]
		}

		headline.Println(msg)
	}
}
