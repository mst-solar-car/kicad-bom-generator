# Middleware
Middleware is what separates this BOM generator from others, even ones built into
KiCad.

It has the power to completely alter a component list, contact external services, and muchmore.

Some examples of cool potential middleware:
- Using the DigiKey API to find prices or part numbers
- Looking up the part in data base to find internal part numbers, etc...
- Going into the library for the component and retrieving other metadata for it


# How Middleware Works
Middleware works very similar to a "middleman" (hence, the name). It is called after
all the components have been parsed, but before the output formatter is called.

Middleware lives inside the [Middleware.go](Middleware.go) file.

**All Middleware Functions must accept, and return a KiCadComponentList**

Once you've written your middleware function, all you need to do is add it to the
middleware chain that lives inside the `applyMiddleware` function inside `Middleware.go`.

And then you've succesfully implemented new middleware.