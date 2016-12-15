#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Generates a Penrose tiling.

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
import math
import SvgBasics


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # overload only relevant ops
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __div__(self, other):
        return Point(self.x / other, self.y / other)

    def __str__(self):
        return SvgBasics.formatCoordinates(self.x, self.y)

    # done to avoid most floating point problems
    def __eq__(self, other):
        return str(self) == str(other)

    def __hash__(self):
        return self.__str__().__hash__()


class PenroseTriangle(object):
    def __init__(self, isRed, pointA, pointB, pointC):
        self.isRed = isRed
        self.pointA = pointA
        self.pointB = pointB
        self.pointC = pointC


class PenroseTiling(SvgBasics.BaseEffectExtension):
    __goldenRatio = (1 + math.sqrt(5)) / 2

    def __init__(self):
        SvgBasics.BaseEffectExtension.__init__(self, 'PenroseTiling.inx')

    def subdivide(self, triangles):
        result = []
        for triangle in triangles:
            if triangle.isRed:
                # Subdivide red triangle
                P = triangle.pointA + (triangle.pointB - triangle.pointA) / PenroseTiling.__goldenRatio
                result += [PenroseTriangle(True, triangle.pointC, P, triangle.pointB),
                           PenroseTriangle(False, P, triangle.pointC, triangle.pointA)]
            else:
                # Subdivide blue triangle
                Q = triangle.pointB + (triangle.pointA - triangle.pointB) / PenroseTiling.__goldenRatio
                R = triangle.pointB + (triangle.pointC - triangle.pointB) / PenroseTiling.__goldenRatio
                result += [PenroseTriangle(False, R, triangle.pointC, triangle.pointA),
                           PenroseTriangle(False, Q, R, triangle.pointB),
                           PenroseTriangle(True, R, Q, triangle.pointA)]
        return result


    def _drawLine(self, startPoint, endPoint, style):
        if (startPoint, endPoint) in self.drawnLines or (endPoint, startPoint) in self.drawnLines:
            return
        edge = 'M ' + str(startPoint) + " L" + str(endPoint)
        self._addPathToDocumentTree(style, edge)
        self.drawnLines.add((startPoint, endPoint))

    def effect(self):
        self.radius = self._conv(self.options.radius)
        self.linewidth = self._conv(self.options.linewidth)

        # Create wheel of triangles around the origin
        triangles = []
        A = Point(self.radius, self.radius)
        for i in xrange(10):
            phi = (2 * i - 1) * math.pi / 10
            B = Point(self.radius * math.cos(phi), self.radius * math.sin(phi)) + A
            phi = (2 * i + 1) * math.pi / 10
            C = Point(self.radius * math.cos(phi), self.radius * math.sin(phi)) + A
            triangle = PenroseTriangle(True, A, C, B) if i % 2 == 0 else PenroseTriangle(True, A, B, C)
            triangles.append(triangle)

        # Perform subdivisions
        for i in xrange(self.options.subdivisions):
            triangles = self.subdivide(triangles)

        self.drawnLines = set()
        style = simplestyle.formatStyle(
            {'stroke': '#000000', 'stroke-width': str(self.linewidth), 'fill': 'none', 'stroke-linecap': 'round'})
        for triangle in triangles:
            self._drawLine(triangle.pointA, triangle.pointB, style)
            self._drawLine(triangle.pointC, triangle.pointA, style)


# Create effect instance and apply it.
effect = PenroseTiling()
effect.affect()
