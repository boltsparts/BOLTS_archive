###################################
Changes of the BOLTS specifications
###################################

**********
0.3 to 0.4
**********

* removed fcstd and stl base geometries
* lifted restriction of collection id forbidding gui, common and template
* added class name element and class standard element
* reworked names and standard system in class elements
* naming element renamed to substitution element, changed template requirements
  and removed substitute field
* lifted restriction of parameter names forbidding standard and name
* added restrictions on characters usable for Table Index
* added syntax to group non-standardized parts together

**********
0.2 to 0.3
**********

* added common field to the Parameter element
* added "name" as a forbidden parameter name
* moved collection information from header directly into the element
* explicit collection id
* factored databases out of what was backends
* removed specifications of backends
* moved infos about drawings into a separate database
* added SolidWorks database
* added syntax to specify connectors for OpenSCAD
* added description field to Parameter element
* added table2 2 dimensional lookup tables
* make types mandatory
* distinguish between dimension and connector drawings
* added Angle type



**********
0.1 to 0.2
**********

More or less a complete rewrite
