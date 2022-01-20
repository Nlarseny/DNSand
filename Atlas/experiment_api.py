import requests

# GOAL: call atlas api to get info on if serial has changed 
# The probes will be selected around the world to see how long it takes for the root servers to update

# https://atlas.ripe.net:443/api/v2/measurements/{measurement_id}/results/?probe_ids=8756
x = {'amount':'33', 'recipient':'larsen.d.nathan@gmail.com', }
requests.post("https://atlas.ripe.net:443/api/v2/credits/transfers", data=x)
# /api/v2/measurements/34861161/results/?format=json
response = requests.get("https://atlas.ripe.net:443/api/v2/measurements/dns/")
#print(response.content()) # Return the raw bytes of the data payload
# print(response.text()) # Return a string representation of the data payload
print(response.json()) # This method is convenient when the API returns JSON
print(response)