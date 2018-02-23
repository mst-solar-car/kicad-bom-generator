# Formatters
Formatters are what turn a list of components into a format that can easily be read by humans, or by computers.

By default, this program allows for the following output formats:

Name | Extension | Source |
-----|-----------|---------|
Excel | `.xlsx` | [source](excel_formatter.py) |
Comma Separate Value | `.csv` | [source](csv_formatter.py) |
JSON | `.json` | [source](json_formatter.py) |


# Responsibilities
When creating a new formatter, do not over-step your bounds and modify the list, this is the role of `Middleware`.

The only responsibilies of the formatter are:
1. Generate the output
2. Save a file

*Formatters MUST return the absolute path to the file that was saved**

# Creating a Formatter
Creating a formatter only takes 3 simple steps.

## Step 1
The first step is to create a file in the `Formatter` folder (the same folder as this README)

The file **MUST** be in this format: "`*_formatter.py`" where `*` is the name of your formatter

## Step 2
import the `Formatter` module

```py
import Formatter
```

## Step 3
Create a function for your formatter that has registers it using a decorator
This function must accept a list of components, and must return the path to the file that it saved

```py
@Formatter.Register("Extension-Of-Output-File")
def myformatter_formatter(components):
  """ A nice comment about what your formatter does """
  # Code for your formatter
```

*Note:* the formatter name is not case sensitive

Now, in KiCad specify `Extension-Of-Output-File` in the `Command Line` as the file extension of the second parameter `"%O"`.

Example:
`"%O.Extension-Of-Output-File"`

