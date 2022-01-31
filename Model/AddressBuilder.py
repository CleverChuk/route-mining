#!/usr/bin/python
#-*- coding: utf-8 -*-

from os import stat
import re

from Model.Address import Address


class AddressBuilder:
    def __init__(self):
        self._street_number = None
        self._street_name = None
        self._apt_number = None
        self._city = None
        self._state = None
        self._zip = None
        self._carrier_route = None

    
    def street_number(self, street_number):
        self._street_number = street_number
        return self

    def street_name(self, street_name):
        self._street_name = street_name
        return self

    def apt_number(self, apt_number):
        self._apt_number = apt_number
        return self

    def city(self, city):
        self._city = city
        return self

    def state(self, state):
        self._state = state
        return self

    def zip(self, zip):
        self._zip = zip
        return self

    def carrier_route(self, carrier_route):
        self._carrier_route = carrier_route
        return self

    def build(self):
        return Address(self._street_number, self._street_name, self._apt_number, self._city, self._state, self._zip, self._carrier_route)

