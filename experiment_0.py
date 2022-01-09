import dns.resolver
from datetime import datetime
import time


class TimeStamps:
    def __init__(self, hour = 0, min = 0, sec = 0):
        self.hour = hour
        self.min = min
        self.sec = sec

    def print_time(self):
        line = str(self.hour) + ":" + str(self.min) + ":" + str(self.sec)
        print(line)

    def to_seconds(self):
        return (self.hour * 3600) + (self.min * 60) + self.sec



def createTimeStamp():
    x = datetime.now().time()

    hour = x.strftime("%H")
    minute = x.strftime("%M")
    second = x.strftime("%S")

    result = TimeStamps(int(hour), int(minute), int(second))

    return result


#delta time: multiply and add and then subtract to return delta in seconds
def deltaTimeStamp(time_a, time_b):
    total_a_seconds = time_a.to_seconds()
    total_b_seconds = time_b.to_seconds()

    # z = y - x
    return total_b_seconds - total_a_seconds


def checkIfTime(time_a, time_b, flex_max, flex_min):
    delta = deltaTimeStamp(time_a, time_b)

    if delta >= flex_min and delta <= flex_max:
        return True
    else:
        return False



# main
while True:
    list_times = [1, 2, 3, 4, 5]

    current_time = createTimeStamp()
    t1 = TimeStamps(10, 43, 1)

    for x in list_times:
        if checkIfTime(current_time, t1, 60, -60):
            print("boom")
        else:
            print("ka")

    time.sleep(1)
    break






# answer=dns.resolver.resolve("199.7.91.13", "SOA")
# for data in answer:
#     # data type == int
#     # print(data.serial)
#     print(data)
# print("hi")


import dns.name
import dns.message
import dns.query
import dns.flags

domain = '199.7.91.13'
name_server = '8.8.8.8' # @ part of dig
ADDITIONAL_RDCLASS = 65535

domain = dns.name.from_text(domain)
if not domain.is_absolute():
    domain = domain.concatenate(dns.name.root)

request = dns.message.make_query(domain, dns.rdatatype.ANY)
request.flags |= dns.flags.AD
request.find_rrset(request.additional, dns.name.root, ADDITIONAL_RDCLASS,
                   dns.rdatatype.OPT, create=True, force_unique=True)
response = dns.query.udp(request, name_server)


#print(response.answer)
# for data in response.answer:
#     print(data)
#print(response.additional)
for rrset in response.authority:
        if rrset.rdtype == dns.rdatatype.SOA:
            print(int(rrset[0].serial))

