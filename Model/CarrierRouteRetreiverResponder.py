#!/usr/bin/python
#-*- coding: utf-8 -*-

from typing import List
from Model.Address import Address
from Responder import Responder

CARRIER_ROUTE_ENDPOINT = "https://tools.usps.com/tools/app/ziplookup/zipByAddress"

HEADERS = {
    "user-agent": "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.0.71 Safari/537.0"
}


class CarrierRouteRetreiverResponder(Responder):
    """
        A responder that retrieves the carrier route for each address
    """
    def __init__(self, api_client):
        self.api_client = api_client

    def respond(self, addresses: List[Address]):
        for address in addresses:
            # prepare data for API call
            data = {
                "address1": f"{address.street_number} {address.street_name}",
                "address2": f"{address.apt_number}",
                "city": f"{address.city}",
                "state": f"{address.state}",
                "urbanCode": "",
                "zip": f"{address.zip}"
            }
            # make API
            resp_json = self.api_client.post(CARRIER_ROUTE_ENDPOINT, headers=HEADERS, data=data).json()
            # extract the address list
            address_list = resp_json["addressList"]
            # grab the first address 
            address_json = address_list[0] if len(address_list) else ""
            # update carrier route
            address.carrier_route = address_json["carrierRoute"]

        return addresses

