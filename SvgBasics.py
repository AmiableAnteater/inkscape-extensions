import inkex
import pprint
import xml.etree.ElementTree as ElTree

"""
General tools and a base class for Inkscape effect plugins.

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

def to_bool(value):
    """
       Converts 'something' to boolean. Raises exception for invalid formats
           Possible True  values: 1, True, "1", "TRue", "yes", "y", "t"
           Possible False values: 0, False, None, [], {}, "", "0", "faLse", "no", "n", "f", 0.0, ...

        Source: http://stackoverflow.com/questions/715417/converting-from-a-string-to-boolean-in-python
    """
    if str(value).strip().lower() in ("yes", "y", "true",  "t", "1"): return True
    if str(value).strip().lower() in ("no",  "n", "false", "f", "0", "0.0", "", "none", "[]", "{}"): return False
    raise Exception('Invalid value for boolean conversion: ' + str(value))


def getColorString(longColor):
    """ Convert the long into a #RRGGBB color value
        - verbose=true pops up value for us in defaults
        conversion back is A + B*256^1 + G*256^2 + R*256^3

        Source: https://github.com/Neon22/inkscape_extension_template
    """
    longColor = long(longColor)
    if longColor <0: longColor = long(longColor) & 0xFFFFFFFF
    hexColor = hex(longColor)[2:-3]
    hexColor = '#' + hexColor.rjust(6, '0').upper()
    return hexColor


def formatCoordinates(x, y):
    return '{0:f},{1:f}'.format(x, y)


def arcRel(radiusX, radiusY, xRot, isLargeArc, isSweep, toX, toY):
    largeArcFlag = '1' if isLargeArc else '0'
    sweepFlag = '1' if isSweep else '0'
    arc = ' a ' + formatCoordinates(radiusX, radiusY) + ' {0} '.format(xRot)
    arc += largeArcFlag + ',' + sweepFlag + ' ' + formatCoordinates(toX, toY)
    return arc


def circRel(radius, isLargeArc, isSweep, toX, toY):
    return arcRel(radius, radius, 0, isLargeArc, isSweep, toX, toY)


def lineRel(x, y):
    return ' l ' + formatCoordinates(x, y)


def moveRel(x, y):
    return ' m ' + formatCoordinates(x, y)


def moveAbs(x, y):
    return ' M ' + formatCoordinates(x, y)


class BaseEffectExtension(inkex.Effect):
    def __init__(self, inxFile, useDebugLogging=False):
        inkex.Effect.__init__(self)
        self.__useDebugLogging = useDebugLogging
        inxTree = ElTree.parse(inxFile)
        root = inxTree.getroot()
        namespacePrefix = root.tag[0:-1 * len('inkscape-extension')]
        try:
            # Python 2.6, which is bundled with Inkscape throws an error, when using the non-deprecated iter method
            for param in root.iter(namespacePrefix + 'param'):
                self._addOption(param)
        except AttributeError:
            for param in root.getiterator(namespacePrefix + 'param'):
                self._addOption(param)

    def log(self, what):
        if self.__useDebugLogging:
            inkex.debug(pprint.pformat(what))

    def _handleOption(self, param, paramName):
        """Override this to handle specific options. Return True, if you handled the option, False otherwise."""
        return False

    def _addOption(self, param):
        attributes = param.attrib
        paramName = attributes['name']
        if self._handleOption(param, paramName):
            return

        defaultValue = None
        paramType = attributes['type']
        if paramType in ['description', 'notebook'] :
            return
        elif paramType in ['optiongroup', 'enum']:
            # if you want ints or floats in an enum, you have to override _handleOption
            # for me there was no need
            paramType = 'string'
            if param[0].attrib['value']:
                defaultValue = param[0].attrib['value']
            else:
                raise Exception('No "value" attribute for first option of ' + paramType + '/' + paramName)
        elif paramType == 'boolean':
            paramType = 'inkbool'
            defaultValue = to_bool(param.text)
        elif paramType == 'float':
            defaultValue = float(param.text)
        elif paramType == 'int':
            defaultValue = int(param.text)
        elif paramType == 'string':
            paramType = 'string'
            defaultValue = str(param.text)
        elif paramType == 'color':
            paramType = 'string'
            defaultValue = getColorString(0)

        helpText = attributes.get('_gui-text', attributes.get('gui-text', ''))

        self.OptionParser.add_option('--' + paramName, action='store', type=paramType, dest=paramName,
                                     default=defaultValue, help=helpText)

    def _checkAndGetUnit(self, unit=None):
        if unit is None:
            if self.options.unit:
                unit = self.options.unit
            else:
                raise Exception("No unit specified")
        return unit

    def logInUnit(self, valuesInInks, prefix='', unit=None):
        unit = self._checkAndGetUnit(unit)
        l = ["%s: %s[%s]" % (k, "{0:.2f}".format(self.uutounit(v, self.options.unit)), unit) for k, v in
             sorted(valuesInInks.items())]
        self.log(prefix + ' ' + '; '.join(l))

    def _conv(self, sizeInUserSpecifiedUnits, unit=None):
        unit = self._checkAndGetUnit(unit)
        return self.unittouu(str(sizeInUserSpecifiedUnits) + unit)

    def _addPathToDocumentTree(self, style, svgPath, name=None):
        lineAttributes = {'style': style, 'd': svgPath}
        if name is not None:
            lineAttributes[inkex.addNS('label', 'inkscape')]=name
        inkex.etree.SubElement(self.current_layer, inkex.addNS('path', 'svg'), lineAttributes)

