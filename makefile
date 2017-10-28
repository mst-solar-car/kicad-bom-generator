ifeq ($(OS),Windows_NT)
    # Windows
    all:
			go test ./...
			go build -o kicad-bom-generator.exe
else
    # Linux
    all:
			go test ./...
			go build -o kicad-bom-generator.out
endif