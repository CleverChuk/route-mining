#!/usr/b/python
#-*- codg: utf-8 -*-



class Address:
    def __init__(self, street_number,  street_name,  apt_number,  city,  state,  zip,  carrier_route):
        self.street_number = street_number
        self.street_name = street_name
        self.apt_number = apt_number
        self.city = city
        self.state = state
        self.zip = zip
        self.carrier_route = carrier_route

    def __hash__(self) -> int:
        return hash((self.street_number, self.street_name, self.apt_number, self.city, self.state, self.zip, self.carrier_route))

    def __eq__(self, __o: object) -> bool:
        if not isinstance(Address, __o):
            return False
        
        return hash(self) == hash(__o)