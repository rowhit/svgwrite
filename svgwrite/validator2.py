#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: validator2 module - new validator module
# Created: 01.10.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

from data.full11attributes import full11_attributes
from data.full11elements import full11_elements
from data.full11typechecker import Full11TypeChecker

from data.tiny12attributes import tiny12_attributes
from data.tiny12elements import tiny12_elements
from data.tiny12typechecker import Tiny12TypeChecker

from data import pattern

def get_validator(profile, debug=True):
    """ Validator factory """
    if profile == 'tiny':
        return Tiny12Validator(debug)
    elif profile in ('full', 'basic', 'none'):
        return Full11Validator(debug)
    else:
        raise ValueError('Unsupported profile: %s'  % profile)

class Tiny12Validator(object):
    def __init__(self, debug=True):
        self.debug = debug
        self._init_data()

    def _init_data(self):
        """ Set validator-attributs depending on type of validator.
        """
        self.attributes = tiny12_attributes
        self.elements = tiny12_elements
        self.typechecker = Tiny12TypeChecker()

    def check_all_svg_attribute_values(self, elementname, attributes):
        """
        Check if attributes are valid for object 'elementname' and all svg
        attributes have valid types and values.

        Raises ValueError.
        """
        for attributename, value in attributes.iteritems():
            self.check_svg_attribute_value(elementname, attributename, value)

    def check_svg_attribute_value(self, elementname, attributename, value):
        """
        Check if 'attributename' is valid for object 'elementname' and 'value'
        is a valid svg type and value.

        Raises ValueError.
        """
        self._check_valid_svg_attribute_name(elementname, attributename)
        self._check_svg_value(elementname, attributename, value)

    def _check_svg_value(self, elementname, attributename, value):
        """
        Checks if 'value' is a valid svg-type for svg-attribute
        'attributename'. (elementname is not used for now)

        Raises TypeError.
        """
        # elementname is not used for now, but because some elements
        # have the same named attributs with a little bit different types
        # the elementname can be used later to distinguish these attributes.
        attribute = self.attributes[attributename]
        # check if 'value' match a valid datatype
        for typename in attribute.valid_types:
            if self.typechecker.check(typename, value):
                return
        # check if 'value' is a valid constant
        valuestr = str(value)
        if not valuestr in attribute.valid_const:
            raise TypeError("%s is not a valid value for '%s'." % (value, attributename))

    def _check_valid_svg_attribute_name(self, elementname, attributename):
        """ Check if 'attributename' is a valid svg-attribute for svg-element
        'elementname'.

        Raises ValueError.
        """
        if not self.is_valid_svg_attribute(elementname, attributename):
            raise ValueError("Invalid attribute '%s' for element '%s'." % (attributename, elementname))

    def check_svg_type(self, value, typename='string'):
        """
        Check if 'value' matches svg type 'typename'.

        Raises TypeError.
        """
        if self.typechecker.check(typename, value):
            return value
        else:
            raise TypeError("%s is not of type '%s'." % (value, typename))

    def is_valid_elementname(self, elementname):
        """ True if 'elementname' is a valid svg-element name. """
        return elementname in self.elements

    def is_valid_svg_attribute(self, elementname, attributename):
        """ True if 'attributename' is a valid svg-attribute for svg-element
        'elementname'.
        """
        element = self.elements[elementname]
        return attributename in element.valid_attributes

    def is_valid_children(self, elementname, childrenname):
        """ True if svg-element 'childrenname' is a valid children of
        svg-element 'elementname'.
        """
        element = self.elements[elementname]
        return childrenname in element.valid_children

    def check_valid_children(self, elementname, childrenname):
        """ Checks if svg-element 'childrenname' is a valid children of
        svg-element 'elementname'.

        Raises ValueError.
        """
        if not self.is_valid_children(elementname, childrenname):
            raise ValueError("Invalid children '%s' for element '%s'." % (childrenname, elementname))

    def get_coordinate(self, value):
        """ Split value in (number, unit) if value has an unit or (number, None).

        Raises ValueError.
        """

        if value is None:
            raise TypeError("Invalid type 'None'.")
        if isinstance(value, (int, float)):
            result = (value, None)
        else:
            result = pattern.coordinate.match(value.strip())
            if result:
                number, tmp, unit = result.groups()
                number = float(number)
            else:
                raise ValueError("'%s' is not a valid svg coordinate." % value)
            result = (number, unit)
        if self.typechecker.is_number(result[0]):
            return result
        else:
            version = "SVG %s %s" % self.typechecker.get_version()
            raise ValueError("%s is not a valid number for: %s." % (value, version))
    get_length = get_coordinate

class Full11Validator(Tiny12Validator):
    def _init_data(self):
        self.attributes = full11_attributes
        self.elements = full11_elements
        self.typechecker = Full11TypeChecker()

