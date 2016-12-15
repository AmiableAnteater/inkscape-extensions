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


class DrawDirection:
    def __init__(self, isVertical, runsTowardsOrigin):
        self.isVertical = isVertical
        self.runsTowardsOrigin = runsTowardsOrigin
        self.directionMulitplier = -1 if runsTowardsOrigin else 1

NORTH = DrawDirection(True, True)
EAST = DrawDirection(False, False)
SOUTH = DrawDirection(True, False)
WEST = DrawDirection(False, True)


class LaserBox(SvgBasics.BaseEffectExtension):
    def __init__(self):
        SvgBasics.BaseEffectExtension.__init__(self, "LaserBox.inx")

    def _getRelativeLineCoords(self, length, isVertical):
        if isVertical:
            return '0,' + str(length) + ' '
        else:
            return str(length) + ',0 '

    def _generateIndentedEdge(self, indentCount, indentWidth, drawDirection, startIndented, initialOffset=0,
                              lastOffset=0):
        self.log([indentCount, indentWidth, drawDirection, startIndented, initialOffset, lastOffset])
        relativeLine = ' l'
        currentIndent = -self.thickness if startIndented else self.thickness
        initialEdge = self._getRelativeLineCoords(drawDirection.directionMulitplier * (indentWidth + initialOffset),
                                                  drawDirection.isVertical)
        lastEdge = self._getRelativeLineCoords(drawDirection.directionMulitplier * (indentWidth + lastOffset),
                                               drawDirection.isVertical)
        edge = self._getRelativeLineCoords(drawDirection.directionMulitplier * indentWidth, drawDirection.isVertical)

        for count in xrange(0, indentCount):
            appendEdge = edge
            if count == 0:
                appendEdge = initialEdge
            elif count == indentCount - 1:
                appendEdge = lastEdge

            relativeLine += appendEdge
            if count + 1 < indentCount:
                relativeLine += self._getRelativeLineCoords(currentIndent, not drawDirection.isVertical)
                currentIndent *= -1
        return relativeLine

    def _calculateFinalIndentationAndOffsetForHorizontalLine(self, verticalLineStartedIndented):
        # determine whether the first vertical line drawn is indented at the end
        isEvenNumberOfIndents = self.options.countIndentsSides % 2 == 0
        # the line is indented at the end, if it started indented and the number of indents is odd (verticalLineStartedIndented == True, isEvenNumberOfIndents == False) OR
        #                                  if it started not indented and the number of indents is even (verticalLineStartedIndented == False, isEvenNumberOfIndents == True)
        isIndentedAtEnd = verticalLineStartedIndented != isEvenNumberOfIndents
        # if the last bit of the horizontal line ended NOT indented, we have to add an offset at the start (and at the end in the other case)
        initialOffset = 0 if isIndentedAtEnd else self.thickness
        lastOffset = self.thickness - initialOffset
        return (isIndentedAtEnd, initialOffset, lastOffset)

    def _createIndentedVerticalLine(self, upperLeftOffsetX, upperLeftOffsetY, startIndented):
        # set starting point of line
        joinedLine = 'M ' + str(upperLeftOffsetX) + ',' + str(upperLeftOffsetY)
        # draw southwards
        joinedLine += self._generateIndentedEdge(self.options.countIndentsSides, self.lengthOfSideIndents, SOUTH,
                                                 startIndented)
        isLineToSouthIndentedAtEnd, initialOffset, lastOffset = self._calculateFinalIndentationAndOffsetForHorizontalLine(
            startIndented)
        return (joinedLine, isLineToSouthIndentedAtEnd, initialOffset, lastOffset)

    def _generateSideShape(self, upperLeftOffsetX, upperLeftOffsetY, isForWidthSide):
        horizontalIndentsCount = self.countIndentsTopWidth if isForWidthSide else self.countIndentsTopDepth
        horizontalIndentsWidth = self.lengthOfTopWidthIndents if isForWidthSide else self.lengthOfTopDepthIndents

        # using a variable here enables usage as parameter (not tested!)
        leftSideStartIndented = False
        joinedLine, isLineToSouthIndentedAtEnd, initialOffset, lastOffset = self._createIndentedVerticalLine(
            upperLeftOffsetX, upperLeftOffsetY, leftSideStartIndented)
        joinedLine += self._generateIndentedEdge(horizontalIndentsCount, horizontalIndentsWidth, EAST, True,
                                                 initialOffset, lastOffset)
        joinedLine += self._generateIndentedEdge(self.options.countIndentsSides, self.lengthOfSideIndents, NORTH,
                                                 isLineToSouthIndentedAtEnd)

        # determine whether the second vertical line drawn is indented at the end
        isLineToNorthIndentedAtEnd, initialOffset, lastOffset = self._calculateFinalIndentationAndOffsetForHorizontalLine(
            isLineToSouthIndentedAtEnd)
        if self.options.includeLid:
            joinedLine += self._generateIndentedEdge(horizontalIndentsCount, horizontalIndentsWidth, WEST, False,
                                                     lastOffset, initialOffset)
        joinedLine += 'z'
        return joinedLine

    def _addSideShape(self, name, style, upperLeftOffsetX, upperLeftOffsetY, isForWidthSide):
        svgPath = self._generateSideShape(upperLeftOffsetX, upperLeftOffsetY, isForWidthSide)
        self._addPathToDocumentTree(style, svgPath, name)

    def _generateTopShape(self, upperLeftOffsetX, upperLeftOffsetY):
        joinedLine = 'M ' + str(upperLeftOffsetX) + ',' + str(upperLeftOffsetY)
        joinedLine += self._generateIndentedEdge(self.countIndentsTopDepth, self.lengthOfTopDepthIndents, SOUTH, True)
        joinedLine += self._generateIndentedEdge(self.countIndentsTopWidth, self.lengthOfTopWidthIndents, EAST, False)
        joinedLine += self._generateIndentedEdge(self.countIndentsTopDepth, self.lengthOfTopDepthIndents, NORTH, False)
        joinedLine += self._generateIndentedEdge(self.countIndentsTopWidth, self.lengthOfTopWidthIndents, WEST, True)
        joinedLine += 'z'
        return joinedLine

    def _addTopShape(self, name, style, upperLeftOffsetX, upperLeftOffsetY):
        svgPath = self._generateTopShape(upperLeftOffsetX, upperLeftOffsetY)
        self._addPathToDocumentTree(style, svgPath, name)

    def _addMergedSideShape(self, style, upperLeftOffsetX, upperLeftOffsetY):
        # using a variable here enables usage as parameter (not tested!)
        leftSideStartIndented = False
        joinedLine, isLineToSouthIndentedAtEnd, initialOffset, lastOffset = self._createIndentedVerticalLine(
            upperLeftOffsetX, upperLeftOffsetY, leftSideStartIndented)

        # draw eastwards - two times for the width, two times for the depth
        joinedLine += self._generateIndentedEdge(self.countIndentsTopWidth, self.lengthOfTopWidthIndents, EAST, True,
                                                 initialOffset, lastOffset)
        joinedLine += self._generateIndentedEdge(self.countIndentsTopWidth, self.lengthOfTopWidthIndents, EAST, True,
                                                 initialOffset, lastOffset)
        joinedLine += self._generateIndentedEdge(self.countIndentsTopDepth, self.lengthOfTopDepthIndents, EAST, True,
                                                 initialOffset, lastOffset)
        joinedLine += self._generateIndentedEdge(self.countIndentsTopDepth, self.lengthOfTopDepthIndents, EAST, True,
                                                 initialOffset, lastOffset)

        # draw northwards
        joinedLine += self._generateIndentedEdge(self.options.countIndentsSides, self.lengthOfSideIndents, NORTH,
                                                 isLineToSouthIndentedAtEnd)

        # determine whether the second vertical line drawn is indented at the end
        isLineToNorthIndentedAtEnd, initialOffset, lastOffset = self._calculateFinalIndentationAndOffsetForHorizontalLine(
            isLineToSouthIndentedAtEnd)

        # draw westwards and close the shape
        if self.options.includeLid:
            # repeat the same spiel backwards
            joinedLine += self._generateIndentedEdge(self.countIndentsTopDepth, self.lengthOfTopDepthIndents, WEST,
                                                     False, lastOffset, initialOffset)
            joinedLine += self._generateIndentedEdge(self.countIndentsTopDepth, self.lengthOfTopDepthIndents, WEST,
                                                     False, lastOffset, initialOffset)
            joinedLine += self._generateIndentedEdge(self.countIndentsTopWidth, self.lengthOfTopWidthIndents, WEST,
                                                     False, lastOffset, initialOffset)
            joinedLine += self._generateIndentedEdge(self.countIndentsTopWidth, self.lengthOfTopWidthIndents, WEST,
                                                     False, lastOffset, initialOffset)

        joinedLine += 'z'
        self._addPathToDocumentTree(style, joinedLine, "sides")

        noFillStyle = simplestyle.formatStyle(
            {'stroke': '#000000', 'stroke-width': str(self.linewidth), 'fill': 'none'})
        joinedLine = \
            self._createIndentedVerticalLine(upperLeftOffsetX + self.insideWidth + self.thickness, upperLeftOffsetY,
                                             leftSideStartIndented)[0]
        self._addPathToDocumentTree(noFillStyle, joinedLine, "cut0")
        joinedLine = \
            self._createIndentedVerticalLine(upperLeftOffsetX + 2 * (self.insideWidth + self.thickness),
                                             upperLeftOffsetY,
                                             leftSideStartIndented)[0]
        self._addPathToDocumentTree(noFillStyle, joinedLine, "cut1")
        joinedLine = self._createIndentedVerticalLine(
            upperLeftOffsetX + 2 * (self.insideWidth + self.thickness) + self.insideDepth + self.thickness,
            upperLeftOffsetY, leftSideStartIndented)[0]
        self._addPathToDocumentTree(noFillStyle, joinedLine, "cut2")

    def _calculateDimensions(self):
        # calculate required dimensions in Inkscape units derived from the options
        self.thickness = self._conv(self.options.thickness)
        self.linewidth = self._conv(self.options.linewidth)

        heightDifferenceFactor = 2 if self.options.includeLid else 1
        self.insideHeight = self._conv(
            self.options.height if self.options.insideSpecified else self.options.height - heightDifferenceFactor * self.options.thickness)
        self.insideWidth = self._conv(
            self.options.width if self.options.insideSpecified else self.options.width - 2 * self.options.thickness)
        self.insideDepth = self._conv(
            self.options.depth if self.options.insideSpecified else self.options.depth - 2 * self.options.thickness)

        # further calculations are based on values that are in Inkscape units already
        self.outsideHeight = self.insideHeight + heightDifferenceFactor * self.thickness
        self.outsideWidth = self.insideWidth + 2 * self.thickness
        self.outsideDepth = self.insideDepth + 2 * self.thickness

        warnMessage = ''
        if self.options.countIndentsTopWidth % 2 == 0:
            self.countIndentsTopWidth = self.options.countIndentsTopWidth + 1
            warnMessage += 'Indent top/width count has to be even. You specified ' + str(
                self.options.countIndentsTopWidth) + '. I will use ' + str(self.countIndentsTopWidth) + '.'
        else:
            self.countIndentsTopWidth = self.options.countIndentsTopWidth

        if self.options.countIndentsTopDepth % 2 == 0:
            self.countIndentsTopDepth = self.options.countIndentsTopDepth + 1
            warnMessage += 'Indent top/depth count has to be even. You specified ' + str(
                self.options.countIndentsTopWidth) + '. I will use ' + str(self.options.countIndentsTopWidth + 1) + '.'
        else:
            self.countIndentsTopDepth = self.options.countIndentsTopDepth

        if warnMessage:
            inkex.errormsg(warnMessage)

        self.lengthOfSideIndents = self.outsideHeight / self.options.countIndentsSides
        self.lengthOfTopWidthIndents = self.insideWidth / self.countIndentsTopWidth
        self.lengthOfTopDepthIndents = self.insideDepth / self.countIndentsTopDepth

    def effect(self):
        self._calculateDimensions()
        style = simplestyle.formatStyle({'stroke': '#000000', 'stroke-width': str(self.linewidth), 'fill': '#808080'})
        if self.options.mergeSides:
            self._addMergedSideShape(style, 0, 0);
        else:
            self._addSideShape('front', style, 0, 0, True)
            self._addSideShape('back', style, self.outsideWidth, 0, True)
            self._addSideShape('right', style, 2 * self.outsideWidth, 0, False)
            self._addSideShape('left', style, 2 * self.outsideWidth + self.outsideDepth, 0, False)

        self._addTopShape('bottom', style, self.thickness, self.outsideHeight + self.thickness)
        if self.options.includeLid:
            self._addTopShape('top', style, self.thickness + self.outsideWidth, self.outsideHeight + self.thickness)


# Create effect instance and apply it.
effect = LaserBox()
effect.affect()
