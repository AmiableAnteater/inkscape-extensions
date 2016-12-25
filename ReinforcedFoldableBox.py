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

        # The lid flap holds the two parts of the lid together, when the box is closed.
        # TODO: unhandled error: this could be bigger thand self._width / 2
        lidFlapSize = 2 * overlap * self._width

        # Section with dimensions of the side hook sides
        self._sideHookFoldingGap = .05 * self._height
        sideHookReducedHeight = self._height - 2 * self._sideHookFoldingGap

        # the width of the hooks
        self._sideHookWidth = 2 * overlap * self._width
        # the vertical overlap of the hooks
        sideHookOverlapFactor = .7
        sideHookCutlineFactor = sideHookOverlapFactor - .5
        self._sideHookOverlap = sideHookReducedHeight * sideHookOverlapFactor
        self._sideHookGap = sideHookReducedHeight - self._sideHookOverlap
        sideHookHeight = self._height - 2 * self._sideHookGap
        self._sideWidthIncludingHook = self._width / 2 + self._sideHookWidth


        startX = 2 * self._height
        startY = lidFlapSize

        outline = SvgBasics.moveAbs(startX, startY)

        # Top left flap
        outline += SvgBasics.circRel(.5 * self._width, False, False, -.5 * self._width, .5 * self._width)
        outline += SvgBasics.lineRel(.5 * self._width, 0)

        # side hook
        outline += self.addLeftSideHook()

        # central flap that folds on itself and is kept in place by the semicircle cutout
        outline += SvgBasics.lineRel(-2 * self._height, 0)
        outline += SvgBasics.lineRel(0, self._width)
        outline += SvgBasics.lineRel(2 * self._height, 0)

        # side hook
        outline += self.addLeftSideHook()

        # lower left lid flap
        outline += SvgBasics.lineRel(-.5 * self._width, 0)
        outline += SvgBasics.circRel(.5 * self._width, False, False, .5 * self._width, .5 * self._width)

        # bottom half lid
        outline += SvgBasics.lineRel(.5 * self._depth, 0)
        outline += SvgBasics.circRel(lidFlapSize, False, False, lidFlapSize, lidFlapSize)
        outline += SvgBasics.arcRel(.5 * self._depth - lidFlapSize, lidFlapSize, 0, False, False, .5 * self._depth - lidFlapSize, -lidFlapSize)

        # lower right lid flap
        outline += SvgBasics.circRel(.5 * self._width, False, False, .5 * self._width, -.5 * self._width)
        outline += SvgBasics.lineRel(-.5 * self._width, 0)

        # side hook
        outline += self.addRightSideHook()

        # central flap that folds on itself and is kept in place by the semicircle cutout
        outline += SvgBasics.lineRel(2 * self._height, 0)
        outline += SvgBasics.lineRel(0, -self._width)
        outline += SvgBasics.lineRel(-2 * self._height, 0)

        # side hook
        outline += self.addRightSideHook()

        # upper right lid flap
        outline += SvgBasics.lineRel(.5 * self._width, 0)
        outline += SvgBasics.circRel(.5 * self._width, False, False, -.5 * self._width, -.5 * self._width)

        # bottom half lid
        outline += SvgBasics.lineRel(-.5 * self._depth, 0)
        outline += SvgBasics.circRel(lidFlapSize, False, False, -lidFlapSize, -lidFlapSize)
        outline += SvgBasics.arcRel(.5 * self._depth - lidFlapSize, lidFlapSize, 0, False, False, -(.5 * self._depth - lidFlapSize), lidFlapSize)

        outline += ' z'

        style = simplestyle.formatStyle({'stroke': '#000000', 'stroke-width': str(self._linewidth), 'fill': '#808080'})
        self._addPathToDocumentTree(style, outline)

        # cutline = SvgBasics.moveAbs(2 * self._height - .5 * self._width, startY + .5 * self._width)
        # cutline += SvgBasics.lineRel(.5 * self._width, 0)
        #
        # cutline += SvgBasics.moveAbs(2 * self._height - .5 * self._width, startY + .5 * self._width + .25 * self._height)
        # cutline += SvgBasics.lineRel(0, .25 * self._height)
        #
        # self._addPathToDocumentTree(style, cutline)

    def addLeftSideHook(self):
        # side flap with hook
        sideHook = SvgBasics.lineRel(0, self._sideHookFoldingGap)
        sideHook += SvgBasics.lineRel(-.5 * self._width, 0)
        sideHook += SvgBasics.lineRel(0, self._sideHookGap)
        # this is the point to add a cut line
        sideHook += SvgBasics.lineRel(-self._sideHookWidth, 0)
        sideHook += SvgBasics.lineRel(0, self._sideHookOverlap)
        sideHook += SvgBasics.lineRel(self._sideWidthIncludingHook, 0)
        sideHook += SvgBasics.lineRel(0, self._sideHookFoldingGap)
        return sideHook

    def addRightSideHook(self):
        # side flap with hook
        sideHook = SvgBasics.lineRel(0, -self._sideHookFoldingGap)
        sideHook += SvgBasics.lineRel(self._sideWidthIncludingHook, 0)
        sideHook += SvgBasics.lineRel(0, -self._sideHookOverlap)
        sideHook += SvgBasics.lineRel(-self._sideHookWidth, 0)
        sideHook += SvgBasics.lineRel(0, -self._sideHookGap)
        sideHook += SvgBasics.lineRel(-.5 * self._width, 0)
        sideHook += SvgBasics.lineRel(0, -self._sideHookFoldingGap)
        return sideHook


# Create effect instance and apply it.
effect = FoldableBox()
effect.affect()
