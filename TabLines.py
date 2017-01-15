#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Generates tabbed edges and fitting cut-outs.

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

import simplestyle
import SvgBasics


class TabLines(SvgBasics.BaseEffectExtension):
    def __init__(self):
        SvgBasics.BaseEffectExtension.__init__(self, 'TabLines.inx')

    def effect(self):
        thickness = self._conv(self.options.thickness)
        leadingOffset = self._conv(self.options.leadingOffset)
        lengthOfTabs = self._conv(self.options.lengthOfTabs)
        lengthOfGaps = self._conv(self.options.lengthOfGaps)
        trailingOffset = self._conv(self.options.trailingOffset)
        linewidth = self._conv(self.options.linewidth)

        line = SvgBasics.moveAbs(thickness, thickness)
        cutouts = SvgBasics.moveAbs(3 * thickness, thickness)

        line += SvgBasics.lineRel(0, leadingOffset)
        cutouts += SvgBasics.moveRel(0, leadingOffset)

        for i in xrange(1, self.options.countTabs + 1):
            line += SvgBasics.createTab(thickness, lengthOfTabs)
            cutouts += SvgBasics.createRect(thickness, lengthOfTabs)
            if i < self.options.countTabs:
                line += SvgBasics.lineRel(0, lengthOfGaps)
                cutouts += SvgBasics.moveRel(0, lengthOfTabs + lengthOfGaps)
            elif trailingOffset > 0:
                line += SvgBasics.lineRel(0, trailingOffset)

        style = simplestyle.formatStyle(
            {'stroke': '#000000', 'stroke-width': str(linewidth), 'fill': 'none'})
        self._addPathToDocumentTree(style, line)
        self._addPathToDocumentTree(style, cutouts)

# Create effect instance and apply it.
effect = TabLines()
effect.affect()
