import requests
HOST_ENDPOINT = "https://tools.usps.com/tools/app/ziplookup/zipByAddress"
ADDRESS_LOOKUP = "https://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/findAddressCandidates"

HEADERS = {
    "user-agent": "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.0.71 Safari/537.0"
}

data = {
    "address1": "500 110th Ave N",
    "address2": "apt# 1204",
    "city": "St Petersburg",
    "state": "FL",
}

params = {
    "SingleLine": "500 110th Ave N, apt# 1204, St Petersburg, Fl",
    "f": "json",
    "outFields": "*",
    "countryCode": "US"
}

resp = requests.post(HOST_ENDPOINT, headers=HEADERS, data=data)

# print(resp.json(), end="\n\n")

# resp = requests.get(ADDRESS_LOOKUP, headers=HEADERS, params=params)

print(resp.json())

