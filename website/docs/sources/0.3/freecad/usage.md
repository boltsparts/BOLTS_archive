---
  title: Using BOLTS for FreeCAD
  audience: user
---

You need to have [installed BOLTS for FreeCAD](installation.html).

### Starting the part selector using the macro

Choose <code>Macros</code> from the <code>Macro</code> menu and execute <code>start_bolts.FCMacro</code>.

### Starting the parts selector using a toolbar button

If you have [setup a toolbar button](toolbar.html), you can start the part selector by simply clicking on the button

### The different elements of the part selector

The available parts are sorted in two ways:

1. thematically by collections
2. by the standardization organisation if standardized

By expanding the tree one can browse through the available parts. In the area between the treeview and the button informations about the current selection are displayed.

[<img alt="Expanded treeview" src="{{ site.baseurl }}/images/partsselector2.png" style="width: 100%;"/>]({{ site.baseurl }}/images/partsselector2.png)

You can see that some parts (like DIN931, DIN933) are visible twice in this screenshot, once in the hexagon fastener collection, once in the list of DIN standards.

### Specify parameters and insert the part

If you select a part, for example ISO4017, another hexagon fastener, below the information area additional elements appear that allow to give values for the parameters of the part that are not yet specify.

To lookup the meaning of the parameters, one can consult the [BOLTS specification page of this part]({{ site.baseurl }}/html/classes/ISO4017.html). The navigation of the [specification pages]({{ site.baseurl }}/html/index.html) is structured in the same way as the navigation in the parts selector.

In the case of ISO4017, we need to give a length and a diameter. The diameter can be chosen from the drop down list that lists all choices known to BOLTS, the length can be entered in the line edit. It only accepts positive numbers.

Once the parameters are specified, the part can be inserted into the active document by clicking the `Add part` button. In the combo view on the right side you can see that the label of the object gives the standard and the value of all the parameters we have specified.

[<img alt="Expanded treeview" src="{{ site.baseurl }}/images/partsselector3.png" style="width: 100%;"/>]({{ site.baseurl }}/images/partsselector3.png)
