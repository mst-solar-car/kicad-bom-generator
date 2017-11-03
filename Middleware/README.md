# Middleware
Middleware is what separates this BOM generator from others, even ones built into
KiCad.

It has the power to completely alter a component list, contact external services, and muchmore.

Some examples of cool potential middleware:
- Using the DigiKey API to find prices or part numbers
- Looking up the part in data base to find internal part numbers, etc...


# How Middleware Works
Middleware works very similar to a "middleman" (hence, the name). It is called after
all the components have been parsed, but before the output formatter is called.


# Creating Middleware
Creating Middleware is nearly the exact process as creating a Formatter.

**All Middleware Functions must accept, and return a KiCadComponentList**

## Step 1
The first step is to create a file in the `Middleware` folder (the same folder as this README)

The file **MUST** be in this format: "`*_middleware.py`" where `*` is the name of your middleware

## Step 2
import the `Middleware` module

```py
import Middleware
```

## Step 3
Create a function for your middleware that has registers it using a decorator
This function must accept a list of components, and must return a list of components

```py
@Middleware.Register("My-Middleware-Name")
def mymiddleware_middleware(components):
  """ A nice comment about what your Middleware does """
  # Code for your middleware
```

*Note:* the Middleware name is not case sensitive

## Step 4
This is where Middleware and Formatters differ. If you want to add your newly created middleware to the pipeline, add the name of your middleware to the `middleware` array in `config.json`.