#!/usr/bin/python
# -*- coding: utf-8 -*-

from audioop import add
from typing import List
from Model.Address import Address
from Model.AddressBuilder import AddressBuilder
from Responder import Responder
import requests
ADDRESS_LOOKUP = "https://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/findAddressCandidates"

HEADERS = {
    "user-agent": "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.0.71 Safari/537.0"
}


class AddressValidationResponder(Responder):
    def __init__(self): # noop constructor
        pass

    def respond(self, addresses: List[Address]):
        for idx in range(len(addresses)):
            address = addresses[idx]
            # prepare params for API call
            params = {
                "SingleLine": f"{address.street_number} {address.street_name} {address.apt_number} {address.city} {address.state} {address.zip}",
                "f": "json",
                "outFields": "*",
                "countryCode": "US"
            }
            # make API
            resp_json = requests.get(
                ADDRESS_LOOKUP, headers=HEADERS, params=params).json()
            # extract candidate addresses
            candidates = resp_json["candidates"]
            # grab the address with the best score
            address_json = candidates[0] if len(candidates) else ""
            # validate address
            verdict, new_address = self.validate(address_json)

            if not verdict: # update the address if they don't match
                addresses[idx] = new_address

        return addresses

    def validate(self, address: Address, address_json):
        if not address_json: # if there's no data, we assume the provided address is correct since there's nothing we can do about it other filtering the address out
            return (True, address)

        # extract relevant information from the response from the API call
        address_attributes = address_json["attributes"]
        street_number = address_attributes["AddNum"]
        street_name = f"{address_attributes['StName']} {address_attributes['StType']}"
        apt_number = address_attributes["SubAddr"]
        city = address_attributes["City"]
        state = address_attributes["RegionAbbr"]
        zip = address_attributes["Postal"]

        # create new address from the information and compare with the given address
        received_address = AddressBuilder().street_number(street_number).street_name(
            street_name).apt_number(apt_number).city(city).state(state).zip(zip).build()

        return (address == received_address, received_address)
