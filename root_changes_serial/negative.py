import sys, getopt
from datetime import datetime
import time
import threading
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
    

def ask_root(root_name, server_root):
    #opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])

    iter = 0
    previous_serial = 0
    target = "example.com" + str(iter)

    file_name = str(root_name) + ".txt"
    
    while 1:
        # print(root_name)
        # print(f'{iter}) Running dig SOA...')
        iter += 1
        
        serial = str(get_serial(target, server_root))
        time.sleep(1)

        if serial != previous_serial:
            # ct = datetime.now()
            ct = str(datetime.now())
            output = ct + " " + serial +" \n"
            f = open(file_name, "a")
            f.write(output)
            f.close()

            print(ct, serial)
            previous_serial = serial
        
        target = "example.com" + str(iter)
        # print(target)
        # time.sleep(1)


def main(argv):
    opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])

    # roots = [("verisign(a)", "198.41.0.4"),
    # ("USC", "199.9.14.201"),
    # ("Cogent Com", "192.33.4.12"),
    # ("UM", "199.7.91.13"),
    # ("NASA", "192.203.230.10"),
    # ("ISC", "192.5.5.241"),
    # ("US DD (NIC)", "192.112.36.4"),
    # ("Army", "198.97.190.53"),
    # ("Netnod", "192.36.148.17"),
    # ("verisign (j)", "192.58.128.30"),
    # ("RIPE", "193.0.14.129"),
    # ("ICANN", "199.7.83.42"),
    # ("WIDE", "202.12.27.33")]

    roots = [("NASA_3", "192.203.230.10")]

    # threading should start here
    for r in roots:
        
        # x = threading.Thread(target=ask_root, args=(r[0], r[1]))
        # x.start()
        # print(r)
        


        print(r)
        ask_root(r[0], r[1])
        # time.sleep(3)


if __name__ == "__main__":
    main(sys.argv[1:])
