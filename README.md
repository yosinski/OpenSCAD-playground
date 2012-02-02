What's all this then?
=======================

These are just a few things I've made with [OpenSCAD](http://www.openscad.org/) and [SolidPython](https://github.com/SolidCode/SolidPython). So far:  just this tree.



Tree
=======================

Results of ```python tree.py 918``` rendered in OpenSCAD:

[<img src="https://github.com/yosinski/OpenSCAD-playground/raw/master/generated/tree_918.png" alt="tree" style="max-width:500px;">](https://github.com/yosinski/OpenSCAD-playground/raw/master/generated/tree_918.png)

The tree is based on an [L-system](http://en.wikipedia.org/wiki/L-system) seeded with a random number, in this case, 918.


Try it yourself
=======================


1. Install [OpenSCAD](http://www.openscad.org/) (available for Linux, Mac OS X, and Windows).

2. Clone this repository and run the demo program.

        git clone git://github.com/yosinski/OpenSCAD-playground.git
        cd OpenSCAD-playground
        python tree.py

3. Open the produced ```tree.scad``` file in OpenSCAD. Export as [STL](http://en.wikipedia.org/wiki/STL_%28file_format%29) and 3D print if desired.

That's all you need to get started!

Tweak the parameters in ```tree.py``` to make other L-system designs, or come up with something completely new.



Acknowledgements and License
=======================

The ```pyopenscad.py``` and ```sp_utils.py``` files are copied from [SolidPython](https://github.com/SolidCode/SolidPython) and are included in this distribution, for convenience, under their original [GNU LGPL](http://www.gnu.org/licenses/lgpl.txt) license. All other code is released under [GNU GPL v3](http://www.gnu.org/licenses/gpl.txt).
