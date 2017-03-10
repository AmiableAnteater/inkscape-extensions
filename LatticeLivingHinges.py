#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Generates a living hinge (lattice).

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

import math

import SvgBasics
import simplestyle

__version__ = "0.1"

class Dimensions(object):
    def __init__(self, inksVoffset, inksLength, inksWidth, inksVspacing):
        self.inksVoffset = inksVoffset
        self.inksLength = inksLength
        self.inksWidth = inksWidth
        self.inksVspacing = inksVspacing
        self.totalHeight = self.inksLength + self.inksVspacing

        self.inksRadius = inksWidth / 2
        self.inksLengthWithoutRadii = inksLength - 2 * self.inksRadius

        # The vertical offset of the cut is normalized , so that is smaller or equal 0 and
        # bigger than -(inksLength + inksVspacing).
        while self.inksVoffset > 0:
            self.inksVoffset -= self.totalHeight
        while self.inksVoffset <= -self.totalHeight:
            self.inksVoffset += self.totalHeight


class LatticeLivingHinges(SvgBasics.BaseEffectExtension):
    def __init__(self):
        SvgBasics.BaseEffectExtension.__init__(self, 'LatticeLivingHinges.inx', False)
        self._epsilon = None
        self._lineWidth = None
        self._hingeHeight = None
        self._hSpacing0 = None
        self._hSpacing1 = None

    def _handleOption(self, param, paramName):
        if paramName == 'active-tab':
            self.OptionParser.add_option('--active-tab', action='store', dest='___unused')
        return paramName == 'active-tab'    
        
    def _isBottomReached(self, absoluteY):
        self.log({'absoluteY':absoluteY, 'self._hingeHeight':self._hingeHeight, 'self._epsilon':self._epsilon,
                  'retval:':absoluteY >= self._hingeHeight - self._epsilon})
        return absoluteY >= self._hingeHeight - self._epsilon

    ####################################################################################
    # Code for hairlines
    ####################################################################################
    def _addHairlineCutAndVspacing(self, cut, inksCurrentY, cutLength, vSpacing):
        if self._isBottomReached(inksCurrentY + cutLength):
            cutLength = self._hingeHeight - inksCurrentY
        cut += SvgBasics.lineRel(0, cutLength)
        inksCurrentY += cutLength
        if self._isBottomReached(inksCurrentY + vSpacing):
            vSpacing = self._hingeHeight - inksCurrentY
        cut += SvgBasics.moveRel(0, vSpacing)
        inksCurrentY += vSpacing
        return inksCurrentY, cut

    def _createHairlines(self, dimensions):
        inksCurrentY = 0
        cut = ''
        if -dimensions.inksVoffset > dimensions.inksLength:
            inksCurrentY = dimensions.totalHeight + dimensions.inksVoffset
            cut = SvgBasics.moveRel(0, inksCurrentY)
        else:
            initialCutLength = dimensions.inksLength + dimensions.inksVoffset
            inksCurrentY, cut = self._addHairlineCutAndVspacing(cut, inksCurrentY, initialCutLength, dimensions.inksVspacing)
        while not self._isBottomReached(inksCurrentY):
            inksCurrentY, cut = self._addHairlineCutAndVspacing(cut, inksCurrentY, dimensions.inksLength,
                                                            dimensions.inksVspacing)
        return cut
    ####################################################################################

    @staticmethod
    def _createArcCutoff(availableHeight, dimensions, isDirIncX, isDirIncY):
        x = dimensions.inksRadius - math.sqrt(
            dimensions.inksRadius * dimensions.inksRadius - availableHeight * availableHeight)
        cutoffWidth = dimensions.inksWidth - 2 * x
        if not isDirIncX:
            x *= -1
            cutoffWidth *= -1
        if not isDirIncY:
            availableHeight *= -1
        cut = SvgBasics.circRel(dimensions.inksRadius, False, False, x, availableHeight)
        cut += SvgBasics.lineRel(cutoffWidth, 0)
        cut += SvgBasics.circRel(dimensions.inksRadius, False, False, x, -availableHeight)
        return cut

    def _createWideCuts(self, dimensions):
        cut = ''
        if -dimensions.inksVoffset > dimensions.inksLength:
            inksCurrentY = dimensions.inksLength + dimensions.inksVspacing + dimensions.inksRadius + \
                           dimensions.inksVoffset
            cut += SvgBasics.moveRel(0, inksCurrentY)
        elif -dimensions.inksVoffset > dimensions.inksLengthWithoutRadii + dimensions.inksRadius:
            arcCenterY = dimensions.inksVoffset + dimensions.inksLengthWithoutRadii + dimensions.inksRadius
            arcStartX = dimensions.inksRadius - math.sqrt(dimensions.inksRadius * dimensions.inksRadius -
                                                          arcCenterY * arcCenterY)
            arcRelEndX = dimensions.inksWidth - 2 * arcStartX
            cut += SvgBasics.moveRel(arcStartX, 0)
            cut += SvgBasics.circRel(dimensions.inksRadius, False, False, arcRelEndX, 0) + ' z '
            inksCurrentY = 2 * dimensions.inksRadius + arcCenterY + dimensions.inksVspacing
            cut += SvgBasics.moveRel(-arcStartX, inksCurrentY)
        elif -dimensions.inksVoffset > dimensions.inksRadius:
            cutLength = dimensions.inksLengthWithoutRadii + dimensions.inksRadius + dimensions.inksVoffset
            cut += SvgBasics.lineRel(0, cutLength)
            cut += SvgBasics.circRel(dimensions.inksRadius, True, False, dimensions.inksWidth, 0)
            cut += SvgBasics.lineRel(0, -cutLength) + ' z '
            inksCurrentY = cutLength + 2 * dimensions.inksRadius + dimensions.inksVspacing
            cut += SvgBasics.moveRel(0, inksCurrentY)
        else:
            inksCurrentY = dimensions.inksRadius + dimensions.inksVoffset
            cut += SvgBasics.moveRel(0, inksCurrentY)
        while not self._isBottomReached(inksCurrentY):
            if self._isBottomReached(inksCurrentY + dimensions.inksLengthWithoutRadii):
                cutLength = self._hingeHeight - inksCurrentY
                cut += SvgBasics.lineRel(0, cutLength)
                cut += SvgBasics.lineRel(dimensions.inksWidth, 0)
                cut += SvgBasics.lineRel(0, -cutLength)
            else:
                cut += SvgBasics.lineRel(0, dimensions.inksLengthWithoutRadii)
                if self._isBottomReached(inksCurrentY + dimensions.inksLengthWithoutRadii + dimensions.inksRadius):
                    availableHeight = self._hingeHeight - (inksCurrentY + dimensions.inksLengthWithoutRadii)
                    cut += LatticeLivingHinges._createArcCutoff(availableHeight, dimensions, True, True)
                else:
                    cut += SvgBasics.circRel(dimensions.inksRadius, True, False, dimensions.inksWidth, 0)
                cut += SvgBasics.lineRel(0, -dimensions.inksLengthWithoutRadii)
            if inksCurrentY < dimensions.inksRadius:
                cut += LatticeLivingHinges._createArcCutoff(inksCurrentY, dimensions, False, False)
            else:
                cut += SvgBasics.circRel(dimensions.inksRadius, True, False, -dimensions.inksWidth, 0)
            cut += ' z '
            if self._isBottomReached(inksCurrentY + dimensions.totalHeight):
                # the top arc of the next cut might still be visible
                if not self._isBottomReached(inksCurrentY + dimensions.totalHeight - dimensions.inksRadius):
                    arcCenterY = inksCurrentY + dimensions.totalHeight - self._hingeHeight
                    arcStartX = dimensions.inksRadius - math.sqrt(dimensions.inksRadius * dimensions.inksRadius -
                                                                  arcCenterY * arcCenterY)
                    arcRelEndX = dimensions.inksWidth - 2 * arcStartX
                    cut += SvgBasics.moveRel(arcStartX, self._hingeHeight - inksCurrentY)
                    cut += SvgBasics.circRel(dimensions.inksRadius, False, True, arcRelEndX, 0) + ' z '
            else:
                cut += SvgBasics.moveRel(0, dimensions.totalHeight)
            inksCurrentY += dimensions.totalHeight
        return cut

    def _createCutString(self, dimensions):
        return self._createHairlines(dimensions) if self.options.useHairlines else self._createWideCuts(dimensions)

    def _getInkscapeMeasures(self, voffset, length, width, vspacing):
        inksWidth = 0 if self.options.useHairlines else self._conv(width)
        inksLength = self._conv(length)
        inksVspacing = self._conv(vspacing)
        inksVoffset = self._conv(voffset)

        return Dimensions(inksVoffset, inksLength, inksWidth, inksVspacing)

    def effect(self):
        self._epsilon = self.unittouu("0.001mm")
        self._lineWidth = self.unittouu("0.01mm")

        self._hingeHeight = self._conv(self.options.hinge_height)
        dimensions0 = self._getInkscapeMeasures(self.options.voffset0, self.options.length0, self.options.width0,
                                                self.options.vspacing0)
        # TODO Add some sanity checks, e.g. cutWidth < cutLength, cutLength <= hinge height
        oddCuts = self._createCutString(dimensions0)

        dimensions1 = self._getInkscapeMeasures(self.options.voffset1, self.options.length1, self.options.width1,
                                                self.options.vspacing1)
        evenCuts = self._createCutString(dimensions1)

        self._hSpacing0 = self._conv(self.options.hspacing0)
        self._hSpacing1 = self._conv(self.options.hspacing1)
        if not self.options.useHairlines:
            self._hSpacing0 += self._conv(self.options.width0)
            self._hSpacing1 += self._conv(self.options.width1)
        style = simplestyle.formatStyle(
            {'stroke': '#000000', 'stroke-width': str(self._lineWidth), 'fill': 'none', 'stroke-linecap': 'round'})
        currentX = 0
        for x in xrange(0, self.options.count_cuts):
            self._addPathToDocumentTree(style, 'M ' + str(currentX) + ',0' + oddCuts)
            currentX += self._hSpacing0
            self._addPathToDocumentTree(style, 'M ' + str(currentX) + ',0' + evenCuts)
            currentX += self._hSpacing1


# Create effect instance and apply it.
effect = LatticeLivingHinges()
effect.affect()
