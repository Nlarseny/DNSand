import sys, getopt
from datetime import datetime
import time
import dns.name
import dns.message
import dns.query
import dns.flags


def get_serial(target, server_root):
    #domain = '199.7.91.13'
    #name_server = '8.8.8.8' # @ part of dig
    ADDITIONAL_RDCLASS = 65535

    domain = dns.name.from_text(target)
    if not domain.is_absolute():
        domain = domain.concatenate(dns.name.root)

    request = dns.message.make_query(domain, dns.rdatatype.ANY)
    request.flags |= dns.flags.AD
    request.find_rrset(request.additional, dns.name.root, ADDITIONAL_RDCLASS,
                    dns.rdatatype.OPT, create=True, force_unique=True)
    response = dns.query.udp(request, server_root)


    for rrset in response.authority:
        if rrset.rdtype == dns.rdatatype.SOA:
            return int(rrset[0].serial)

    return -1


def get_list_times(file_name):
    my_file = open(file_name, "r")
    content = my_file.read()
    return content


def main(argv):
    opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])

    # get list of times from file
    list_of_times = get_list_times(args[0])
    

    iter = 0
    target = "example.com" + str(iter)
    previous_serial = 0
    

    while 1:
        # where we need to feed difference between times

        results = stamp_parser("22:17:44.262345")
        
        target_time = datetime.now().time()
        temp = datetime.strptime("21:34:01", "%H:%M:%S").time()
        print(type(target_time))
        
        target_time = target_time.replace(hour = temp.hour, minute = temp.minute, second = temp.second)
        
        print("target time", target_time)
        timer_call(target, target_time, 0, 1, 5)
        time.sleep(1)



if __name__ == "__main__":
    main(sys.argv[1:])
