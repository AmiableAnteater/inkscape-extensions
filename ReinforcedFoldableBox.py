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
import simplestyle


class FoldableBox(SvgBasics.BaseEffectExtension):
    def __init__(self):
        SvgBasics.BaseEffectExtension.__init__(self, "ReinforcedFoldableBox.inx")

    def effect(self):
        self._height = self._conv(self.options.height)
        self._width = self._conv(self.options.width)
        self._depth = self._conv(self.options.depth)
        self._linewidth = self._conv(self.options.linewidth)

        overlap = .1

        # The lid flap holds the two parts of the lid together, when the box is closed.
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
        sideHookCutlineLength = sideHookReducedHeight * sideHookCutlineFactor
        self._sideHookGap = sideHookReducedHeight - self._sideHookOverlap
        self._sideWidthIncludingHook = self._width / 2 + self._sideHookWidth

        startX = 2 * self._height
        startY = lidFlapSize

        outline = SvgBasics.moveAbs(startX, startY)

        # Top left flap
        outline += SvgBasics.arcRel(self._height, .5 * self._width, 0, False, False, -self._height, .5 * self._width)
        outline += SvgBasics.lineRel(self._height, 0)

        # side hook
        outline += self.addLeftSideHook()

        # central flap that folds on itself and is kept in place by the semicircle cutout
        outline += self._addCentralFlap(1)

        # side hook
        outline += self.addLeftSideHook()

        # lower left lid flap
        outline += SvgBasics.lineRel(-self._height, 0)
        outline += SvgBasics.arcRel(self._height, .5 * self._width, 0, False, False, self._height, .5 * self._width)

        # bottom half lid
        outline += SvgBasics.lineRel(.5 * self._depth, 0)
        outline += SvgBasics.circRel(lidFlapSize, False, False, lidFlapSize, lidFlapSize)
        outline += SvgBasics.arcRel(.5 * self._depth - lidFlapSize, lidFlapSize, 0, False, False, .5 * self._depth - lidFlapSize, -lidFlapSize)

        # lower right lid flap
        outline += SvgBasics.arcRel(self._height, .5 * self._width, 0, False, False, self._height, -.5 * self._width)
        outline += SvgBasics.lineRel(-self._height, 0)

        # side hook
        outline += self.addRightSideHook()

        # central flap that folds on itself and is kept in place by the semicircle cutout
        outline += self._addCentralFlap(-1)

        # side hook
        outline += self.addRightSideHook()

        # upper right lid flap
        outline += SvgBasics.lineRel(self._height, 0)
        outline += SvgBasics.arcRel(self._height, .5 * self._width, 0, False, False, -self._height, -.5 * self._width)

        # bottom half lid
        outline += SvgBasics.lineRel(-.5 * self._depth, 0)
        outline += SvgBasics.circRel(lidFlapSize, False, False, -lidFlapSize, -lidFlapSize)
        outline += SvgBasics.arcRel(.5 * self._depth - lidFlapSize, lidFlapSize, 0, False, False, -(.5 * self._depth - lidFlapSize), lidFlapSize)

        outline += ' z '

        firstCutLineVerticalOffset = startY + self._width / 2 + self._sideHookFoldingGap + self._sideHookGap
        secondCutLineVerticalOffset = startY + self._width * 1.5 + self._height + self._sideHookFoldingGap + self._sideHookGap
        leftCutLineHorizontalOffset = 2 * self._height - self._width / 2
        rightCutLineHorizontalOffset = leftCutLineHorizontalOffset + self._depth + self._width
        outline += SvgBasics.moveAbs(leftCutLineHorizontalOffset, firstCutLineVerticalOffset)
        outline += SvgBasics.lineRel(0, sideHookCutlineLength)
        outline += SvgBasics.moveAbs(rightCutLineHorizontalOffset, firstCutLineVerticalOffset)
        outline += SvgBasics.lineRel(0, sideHookCutlineLength)
        outline += SvgBasics.moveAbs(leftCutLineHorizontalOffset, secondCutLineVerticalOffset)
        outline += SvgBasics.lineRel(0, sideHookCutlineLength)
        outline += SvgBasics.moveAbs(rightCutLineHorizontalOffset, secondCutLineVerticalOffset)
        outline += SvgBasics.lineRel(0, sideHookCutlineLength)

        centralArcRadius = self._width / 10
        centralArcX = 2 * self._height
        centralArcY = startY + self._width + self._height - centralArcRadius
        outline += SvgBasics.moveAbs(centralArcX, centralArcY)
        outline += SvgBasics.circRel(centralArcRadius, False, False, 0, 2 * centralArcRadius)
        outline += SvgBasics.moveRel(self._depth, 0)
        outline += SvgBasics.circRel(centralArcRadius, False, False, 0, -2 * centralArcRadius)

        style = simplestyle.formatStyle({'stroke': '#000000', 'stroke-width': str(self._linewidth), 'fill': '#808080'})
        self._addPathToDocumentTree(style, outline)

        foldline = SvgBasics.moveAbs(startX + self._depth / 2, startY)
        foldline += SvgBasics.lineRel(-self._depth / 2, 0)
        foldline += SvgBasics.lineRel(0, self._width / 2)
        foldline += SvgBasics.lineRel(self._depth, 0)
        foldline += SvgBasics.lineRel(0, -self._width / 2)

        foldline += SvgBasics.moveAbs(startX, startY + self._width / 2 + self._sideHookFoldingGap)
        foldline += SvgBasics.lineRel(0, sideHookReducedHeight)
        foldline += SvgBasics.moveRel(self._depth, -sideHookReducedHeight)
        foldline += SvgBasics.lineRel(0, sideHookReducedHeight)
        foldline += SvgBasics.moveRel(0, self._sideHookFoldingGap)
        foldline += SvgBasics.lineRel(-self._depth,0)

        foldline += SvgBasics.moveRel(-self._height, 0)
        foldline += SvgBasics.lineRel(0, self._width)
        foldline += SvgBasics.moveRel(self._height, 0)
        foldline += SvgBasics.lineRel(0, -self._width)
        foldline += SvgBasics.moveRel(self._depth, 0)
        foldline += SvgBasics.lineRel(0, self._width)
        foldline += SvgBasics.moveRel(self._height, 0)
        foldline += SvgBasics.lineRel(0, -self._width)
        foldline += SvgBasics.moveRel(-self._height ,self._width)
        foldline += SvgBasics.lineRel(-self._depth, 0)

        foldline += SvgBasics.moveRel(0, self._sideHookFoldingGap)
        foldline += SvgBasics.lineRel(0, sideHookReducedHeight)
        foldline += SvgBasics.moveRel(self._depth, 0)
        foldline += SvgBasics.lineRel(0, -sideHookReducedHeight)

        foldline += SvgBasics.moveRel(-self._depth / 2, self._sideHookFoldingGap + sideHookReducedHeight + self._width / 2)
        foldline += SvgBasics.lineRel(self._depth / 2, 0)
        foldline += SvgBasics.lineRel(0, -self._width / 2)
        foldline += SvgBasics.lineRel(-self._depth, 0)
        foldline += SvgBasics.lineRel(0, self._width / 2)

        style = simplestyle.formatStyle({'stroke': '#FF0000', 'stroke-width': str(self._linewidth), 'fill': 'none'})
        self._addPathToDocumentTree(style, foldline)

    def _addCentralFlap(self, factor):
        centralFlap = SvgBasics.lineRel(factor * -2 * self._height, 0)
        centralFlap += SvgBasics.lineRel(0, factor * self._width)
        centralFlap += SvgBasics.lineRel(factor * 2 * self._height, 0)
        return centralFlap

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
