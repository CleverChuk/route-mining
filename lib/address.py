
from __future__ import annotations
from json import JSONEncoder
from typing import Any

class Address:
    def __init__(self, street_number: str,  street_name: str,  apt_number: str,  city: str,  state: str,  zip: str,  carrier_route: str):
        self.street_number: str = street_number
        self.street_name: str = street_name
        self.apt_number: str = apt_number
        self.city: str = city
        self.state: str = state
        self.zip: str = zip
        self.carrier_route: str = carrier_route

    def __hash__(self) -> int:
        """
            Computes the hash for an address object
        """
        return hash((self.street_number, self.street_name, self.apt_number, self.city, self.state, self.zip, self.carrier_route))

    def __eq__(self, __o: object) -> bool:
        """
            Compares two address objects
        """
        if not isinstance(__o, Address):
            return False
        
        return hash(self) == hash(__o)

    def __repr__(self) -> str:
        """
            Return the string representation of the object
        """
        return f"{self.street_number} {self.street_name} {self.apt_number} {self.city} {self.state} {self.zip} {self.carrier_route}"
        
class AddressBuilder:
    """
        Builder for creating an address object
    """
    def __init__(self):
        self._street_number: str = None
        self._street_name: str = None
        self._apt_number: str = None
        self._city: str = None
        self._state: str = None
        self._zip: str = None
        self._carrier_route: str = None

    
    def street_number(self, street_number: str) -> AddressBuilder:
        self._street_number = street_number
        return self

    def street_name(self, street_name: str) -> AddressBuilder:
        self._street_name = street_name
        return self

    def apt_number(self, apt_number: str) -> AddressBuilder:
        self._apt_number = apt_number
        return self

    def city(self, city: str) -> AddressBuilder:
        self._city = city
        return self

    def state(self, state: str) -> AddressBuilder:
        self._state = state
        return self

    def zip(self, zip: str) -> AddressBuilder:
        self._zip = zip
        return self

    def carrier_route(self, carrier_route: str) -> AddressBuilder:
        self._carrier_route = carrier_route
        return self

    def build(self):
        return Address(self._street_number, self._street_name, self._apt_number, self._city, self._state, self._zip, self._carrier_route)


class AddressEncoder(JSONEncoder):
    """
        Json Serializer for Address
    """
    def default(self, address: Address) -> Any:
        return address.__dict__
