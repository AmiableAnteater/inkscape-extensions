# inkscape-extensions

## Installation

1. Download a ZIP of this repository (or clone it) using the green button on the top right.
1. Unpack the ZIP.
1. Copy all *.py and *.inx files into the *<Inkscape installation folder>*/share/extensions directory. 
1. (Re-)Start Inkscape
1. Under the menu "Extensions" there is now a sub-menu "FabLab Laser Tools", which contains these extensions.


## LaserBox

Creates a tabbed box with or without lid.
Parts can be laid out to avoid waste of material.


## Penrose Tiling

Code adapted from http://preshing.com/20110831/penrose-tiling-explained/

Mr. Preshing was kind enough to grant me permission to re-use his code.

### Usage:

1. Generate the Penrose tiling (merging all edges into a single path is advisable to speeed up the generation process).
2. Modify the tiling to fit your needs.
3. Do a "Path --> Stroke to path". Set the fill to None and the stroke width according to the specifics of you laser.


## Lattice Living Hinges

Generates a pattern to make rigid material bendable.


## Reinforced Foldable Box

Generates the layout for a cardboard box that does not need glue.

The black lines have to be cut. The power of the laser should be reduced to create grooves at the red lines to ease
folding of the box.

Folding the box is fairly straightforward:

1. Fold up the two little semi-circles. These will later hold back the sides.
2. Fold up the top an bottom sides an hook the side hooks together (behind the litte semi-cirles).
3. Fold up the sides and fold half of them back into the box, so that the side hooks are hidden. Secure the sides with the semi-circles.
4. Close the lid.
