# KiCad Bill-of-Materials Generator
Let's face it... Generating BOMs from KiCad **SUCKS**. This program is looking to change that.

### It's the ★·.·´¯\`·.·★ BOMdigity ★·.·´¯\`·.·★

What this program allows you to do is generate much more friendly output when you're ready
to make your Bill-of-Materials. With the option of completely being able to customize the
internal workings, you can modify, upgrade, and extend this program to your hearts desire.

# Parser
The parser should remain pretty much the same, the goal of this module is to read in `.sch` files, and build a list of components that are used in each one. And then return this so it can be sent to middleware.

# Middleware
This program implements what is known as middleware. Middleware runs between
parsing and retrieving components and the formatter. It can be responsible for a lot
of different tasks. For example:
- Sorting the list of components
- Referencing a database and injecting other data (serial numbers, distributor part numbers, etc)
- Verifying components against some other source

Similar to the formatters, middleware is completely extensible. Read the [Middleware Read Me](Middleware/README.md) for more information.

# Formatters
Formatters let you output your BOM in different formats.

Currently, this program can generate a BOM in the following formats:
- Excel
- Comma Separated Value (CSV)
- JSON

However, it is completely extensible and new formatters can easily be added to
expand the potential output of this program. Read the [Formatters Read Me](Formatter/README.md) for more information.



# Entire Process
Here is a nice diagram that demonstrations the three main parts to this program:
![Parser -> Middleware -> Formatter](diagram.png)

# Usage
This program can be ran directly from inside KiCad!

## Setup
1. Open Eeschema
2. Click on the `Tools > Generate Bill of Materials`
3. Click `Add Plugin` on the right hand side
4. Browse to this folder and select the `__init__.py` file
5. Click `Open`
6. Type in a meaningul name

Now, whenever you are ready to generate your BOM, just select the name that you typed in where it is listed under "`Plugins`" and then click "`Generate`"


### Changing Output Format
If you want to *temporarily* change the output type, in the "`Command Line`" field when you have the plugin selected add `"formatter-name"` to the end (separated by a space from the thing before it [including quotes]). And then click "`Generate`"
