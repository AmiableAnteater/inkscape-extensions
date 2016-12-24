#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Generates Inkscape SVG file containing box components for laser cutting.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import SvgBasics
import inkex
import simplestyle


class FoldableBox(SvgBasics.BaseEffectExtension):
    def __init__(self):
        SvgBasics.BaseEffectExtension.__init__(self, "ReinforcedFoldableBox.inx")




    def effect(self):
        self._height = self._conv(self.options.height)
        self._width = self._conv(self.options.width)
        self._depth = self._conv(self.options.depth)
        self._linewidth = self._conv(self.options.linewidth)

        latch_perc = .8
        overlap = .1
        overlapped_half = .5 + overlap


        style = simplestyle.formatStyle({'stroke': '#000000', 'stroke-width': str(self._linewidth), 'fill': '#808080'})

        # Top left flap
        outline = SvgBasics.moveAbs(2 * self._height, 2 * overlap * self._width)

        outline += SvgBasics.lineRel(-latch_perc * self._height, (1 - latch_perc) * .25 * self._width)
        outline += SvgBasics.lineRel(0, latch_perc * .5 * self._width)
        outline += SvgBasics.lineRel(latch_perc * self._height, (1 - latch_perc) * .25 * self._width)

        # second flap with latch
        outline += SvgBasics.lineRel(-.5 * self._width, 0)
        outline += SvgBasics.lineRel(0, overlapped_half * self._height)
        outline += SvgBasics.moveRel(0, -overlap * self._height)
        outline += SvgBasics.lineRel(- (1-latch_perc) * .5 * self._width, -overlap * self._height)
        outline += SvgBasics.lineRel(-.1 * self._width, 0)
        outline += SvgBasics.lineRel(0, overlapped_half * self._height)
        outline += SvgBasics.lineRel(.1 * self._width + (1-latch_perc) * .5 * self._width + .5 * self._width, 0)

        # central flap
        outline += SvgBasics.lineRel(-2 * self._height, 0)
        outline += SvgBasics.lineRel(0, self._width)
        outline += SvgBasics.lineRel(2 * self._height, 0)

        # second flap with latch  TODO - refactor
        outline += SvgBasics.lineRel(-.5 * self._width, 0)
        outline += SvgBasics.lineRel(0, overlapped_half * self._height)
        outline += SvgBasics.moveRel(0, -overlap * self._height)
        outline += SvgBasics.lineRel(- (1-latch_perc) * .5 * self._width, -overlap * self._height)
        outline += SvgBasics.lineRel(-.1 * self._width, 0)
        outline += SvgBasics.lineRel(0, overlapped_half * self._height)
        outline += SvgBasics.lineRel(.1 * self._width + (1-latch_perc) * .5 * self._width + .5 * self._width, 0)

        # Bottom left flap  TODO - refactor
        outline += SvgBasics.lineRel(-latch_perc * self._height, (1 - latch_perc) * .25 * self._width)
        outline += SvgBasics.lineRel(0, latch_perc * .5 * self._width)
        outline += SvgBasics.lineRel(latch_perc * self._height, (1 - latch_perc) * .25 * self._width)

        # bottom half lid
        outline += SvgBasics.lineRel(.5 * self._depth, 0)
        outline += SvgBasics.lineRel(0, overlap * self._width)
        outline += SvgBasics.lineRel(.1 * self._depth, overlap * self._width)
        outline += SvgBasics.lineRel(.4 * self._depth, -2 * overlap * self._width)

        # Bottom right flap  TODO - refactor
        outline += SvgBasics.lineRel(latch_perc * self._height, -(1 - latch_perc) * .25 * self._width)
        outline += SvgBasics.lineRel(0, -latch_perc * .5 * self._width)
        outline += SvgBasics.lineRel(-latch_perc * self._height, -(1 - latch_perc) * .25 * self._width)

        # second flap with latch  TODO - refactor
        outline += SvgBasics.lineRel(.1 * self._width + (1-latch_perc) * .5 * self._width + .5 * self._width, 0)
        outline += SvgBasics.lineRel(0, -overlapped_half * self._height)
        outline += SvgBasics.lineRel(-.1 * self._width, 0)
        outline += SvgBasics.lineRel(-(1-latch_perc) * .5 * self._width, overlap * self._height)
        outline += SvgBasics.moveRel(0, overlap * self._height)
        outline += SvgBasics.lineRel(0, -overlapped_half * self._height)
        outline += SvgBasics.lineRel(-.5 * self._width, 0)

        # central flap
        outline += SvgBasics.lineRel(2 * self._height, 0)
        outline += SvgBasics.lineRel(0, -self._width)
        outline += SvgBasics.lineRel(-2 * self._height, 0)

        # second flap with latch  TODO - refactor
        outline += SvgBasics.lineRel(.1 * self._width + (1-latch_perc) * .5 * self._width + .5 * self._width, 0)
        outline += SvgBasics.lineRel(0, -overlapped_half * self._height)
        outline += SvgBasics.lineRel(-.1 * self._width, 0)
        outline += SvgBasics.lineRel(-(1-latch_perc) * .5 * self._width, overlap * self._height)
        outline += SvgBasics.moveRel(0, overlap * self._height)
        outline += SvgBasics.lineRel(0, -overlapped_half * self._height)
        outline += SvgBasics.lineRel(-.5 * self._width, 0)

        # Top right flap  TODO - refactor
        outline += SvgBasics.lineRel(latch_perc * self._height, -(1 - latch_perc) * .25 * self._width)
        outline += SvgBasics.lineRel(0, -latch_perc * .5 * self._width)
        outline += SvgBasics.lineRel(-latch_perc * self._height, -(1 - latch_perc) * .25 * self._width)

        # top half lid
        outline += SvgBasics.lineRel(-.5 * self._depth, 0)
        outline += SvgBasics.lineRel(0, -overlap * self._width)
        outline += SvgBasics.lineRel(-.1 * self._depth, -overlap * self._width)
        outline += SvgBasics.lineRel(-.4 * self._depth, 2 * overlap * self._width)

        self._addPathToDocumentTree(style, outline)


# Create effect instance and apply it.
effect = FoldableBox()
effect.affect()
