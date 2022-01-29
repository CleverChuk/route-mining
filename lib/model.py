
from json import JSONEncoder
from typing import Any


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
        if not isinstance(__o, Address):
            return False
        
        return hash(self) == hash(__o)

    def __repr__(self) -> str:
        return f"{self.street_number} {self.street_name} {self.apt_number} {self.city} {self.state} {self.zip} {self.carrier_route}"
        
class AddressBuilder:
    """
        Builder for creating an address object
    """
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


class AddressEncoder(JSONEncoder):
    def default(self, address: Address) -> Any:
        return address.__dict__
