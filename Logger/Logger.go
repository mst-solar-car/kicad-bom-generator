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

var mutex *sync.Mutex

// New is the constructor for the Logger object, it will return the instance
// if one has already been created
func New() *Logger {
	// Create the first Logger object
	once.Do(func() {
		instance = &Logger{Level: Normal, Debugging: false}
		mutex = &sync.Mutex{}
	})

	return instance
}

// EnableVerbose enables verbose logging on a logger
func (logger *Logger) EnableVerbose() {
	mutex.Lock()
	if logger.Level != Verbose {
		logger.Level = Verbose
		logger.Warn("Verbose Logging Enabled")
	}
	mutex.Unlock()
}

// EnableDebug allows for debugging statements to be output
func (logger *Logger) EnableDebug() {
	mutex.Lock()
	if logger.Debugging == false {
		logger.Debugging = true
		logger.Warn("Debug mode Enabled")
	}
	mutex.Unlock()
}

// Warn is a member of Logger that outputs a warning message (in yellow)
func (logger Logger) Warn(params ...string) {
	print(color.FgYellow, append([]string{"WARNING: "}, params...))
}

// Log is a member of Logger that outputs a regular message (in white)
func (logger Logger) Log(params ...string) {
	print(color.FgHiWhite, params)
}

// Success is a member function that outputs a message in green
func (logger Logger) Success(params ...string) {
	print(color.FgHiGreen, params)
}

// Error is a member function that outputs a message in red
func (logger Logger) Error(params ...string) {
	print(color.FgHiRed, append([]string{"ERROR: "}, params...))
}

// Verbose is a member function that outputs a regular message when only in
// verbose mode
func (logger Logger) Verbose(params ...string) {
	if logger.Level != Verbose {
		return
	}

	print(color.FgWhite, params)
}

// Info prints informative messages out in blue
func (logger Logger) Info(params ...string) {
	print(color.FgHiCyan, append([]string{"INFO: "}, params...))
}

// Debug is used for debugging statements
func (logger Logger) Debug(params ...string) {
	if !logger.Debugging {
		return
	}

	print(color.FgHiMagenta, append([]string{"DEBUG: "}, params...))
}

// print is a helper function to allow printing with the mutex
func print(clr color.Attribute, strs []string) {
	mutex.Lock()
	headline := color.New(clr)

	msg := ""
	for i := range strs {
		msg = msg + strs[i]
	}

	headline.Println(msg)
	mutex.Unlock()
}
