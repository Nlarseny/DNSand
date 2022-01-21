import requests
from ripe.atlas.sagan import DnsResult

# GOAL: call atlas api to get info on if serial has changed 
# The probes will be selected around the world to see how long it takes for the root servers to update

# https://atlas.ripe.net:443/api/v2/measurements/{measurement_id}/results/?probe_ids=8756
# x = {'amount':'33', 'recipient':'larsen.d.nathan@gmail.com', }
# requests.post("https://atlas.ripe.net:443/api/v2/credits/transfers", data=x)
# /api/v2/measurements/34861161/results/?format=json
# response = requests.get("https://atlas.ripe.net:443/api/v2/measurements/dns/")
#print(response.content()) # Return the raw bytes of the data payload
# print(response.text()) # Return a string representation of the data payload
# print(response.json()) # This method is convenient when the API returns JSON
# print(response)


# get credits via api
# a = {"amount":33, "recipient":"larsen.d.nathan@gmail.com"}
# https://atlas.ripe.net:443/api/v2/credits/transfers/?key=YOUR_API_KEY   auth=("casey@byu.edu", "aa3acbc0-f98d-45a2-be1f-1135c7bf5718")
# https://atlas.ripe.net/api/v2/credits/transfer/    "key": "aa3acbc0-f98d-45a2-be1f-1135c7bf5718"

# post_creds = requests.post("https://atlas.ripe.net:443/api/v2/credits/transfers/?key=aa3acbc0-f98d-45a2-be1f-1135c7bf5718", data=a)
# print(post_creds)


# https://atlas.ripe.net:443/api/v2/measurements/{measurement_id}/results/?probe_ids=8756


# https://atlas.ripe.net/api/v2/measurements/10006/results/ gives the serial, need to figure out how to get it from my measurement

response = requests.get("https://atlas.ripe.net:443/api/v2/measurements/34898354/results/")
# print(response.json())
# /api/v2/measurements/34872856/results/?start=1642725790&stop=1642726246&format=json
# curl --dump-header - -H "Content-Type: application/json" -H "Accept: application/json" -X POST -d '{"definitions":[{"target":"192.203.230.10","af":4,"query_class":"IN","query_type":"SOA","query_argument":"www.example.com12344321","use_macros":false,"description":"DNS measurement to 192.203.230.10 (NASA)","interval":30,"use_probe_resolver":false,"resolve_on_probe":false,"set_nsid_bit":false,"protocol":"UDP","udp_payload_size":512,"retry":0,"skip_dns_check":false,"include_qbuf":false,"include_abuf":true,"prepend_probe_id":false,"set_rd_bit":false,"set_do_bit":false,"set_cd_bit":false,"timeout":5000,"type":"dns"}],"probes":[{"value":"2803,4842","type":"probes","requested":2}],"is_oneoff":false,"bill_to":"casey@byu.edu","stop_time":1642701046}' https://atlas.ripe.net/api/v2/measurements//?key=YOUR_KEY_HERE

my_dns_result = DnsResult(response.json())

# print(my_dns_result.responses[0].abuf)  # The entire string
print(my_dns_result.responses[0].abuf.answers)  # Decoded from the abuf