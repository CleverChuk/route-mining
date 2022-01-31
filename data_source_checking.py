import requests
HOST_ENDPOINT = "https://tools.usps.com/tools/app/ziplookup/zipByAddress"
ADDRESS_LOOKUP = "https://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/findAddressCandidates"

headers = {
    "user-agent": "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
}

data = {
    "companyName": "JP Morgan Chase",
    "address1": "4915 Independence Pkwy",
    "address2": "",
    "city": "Tampa",
    "state": "FL",
    "urbanCode": "",
    "zip": 33634
}

params = {
    "SingleLine": "500 110th Ave N, apt 1204, St Petersburg, Fl",
    "f": "json",
    "outFields": "*",
    "countryCode": "US"
}

resp = requests.post(HOST_ENDPOINT, headers=HEADERS, data=data)

# print(resp.json(), end="\n\n")

# resp = requests.get(ADDRESS_LOOKUP, headers=HEADERS, params=params)

print(resp.json())

