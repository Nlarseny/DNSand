import sys
from optparse import OptionParser
from datetime import datetime
import time
import dns.name
import dns.message
import dns.query
import dns.flags


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

    def get_time(self):
        line = str(self.hour) + ":" + str(self.min) + ":" + str(self.sec)
        return line


def createTimeStamp():
    x = datetime.now().time()

    hour = x.strftime("%H")
    minute = x.strftime("%M")
    second = x.strftime("%S")

    result = TimeStamps(int(hour), int(minute), int(second))

    return result


# current, target to get time till
def deltaTimeStamp(time_a, time_b):
    total_a_seconds = time_a.to_seconds()
    total_b_seconds = time_b.to_seconds()

    # z = y - x
    return total_b_seconds - total_a_seconds


def checkIfTime(time_a, time_b, flex_max, flex_min):
    delta = deltaTimeStamp(time_a, time_b)
    print(delta)
    if delta >= flex_min and delta <= flex_max:
        print("hit")
        return True
    else:
        return False


def negCheckIfTime(time_a, time_b, flex_min):
    delta = deltaTimeStamp(time_a, time_b)
    if delta <= flex_min:
        print("hit (neg)")
        return True
    else:
        return False


def get_list_times(file_name):
    my_file = open(file_name, "r")
    content = my_file.readlines()
    return content


def next_target(time_list, current_time):
    # print(time_list)
    times = []
    for i in time_list:
        x = str(i)
        x = x.strip()
        #print(x)
        result = x.split(":")
        final = TimeStamps(int(result[0]), int(result[1]), float(result[2]))

        times.append(final)

    # current_time.print_time()
    time_till = []
    for t in times:
        delta = deltaTimeStamp(current_time, t)
        # t.print_time()
        # print(delta, "!!!")
        time_till.append(delta)

    smallest = 99999999999999
    iter = -1
    small_iter = -1
    for t in time_till:
        iter += 1
        # print(iter)
        if t >= 0:
            if t < smallest:
                smallest = t
                small_iter = iter

    # print(small_iter, smallest, time_till[small_iter])
    #times[small_iter].print_time()
    return times[small_iter]


def get_serial(target, server_root):
    #domain = '199.7.91.13' aka the target
    #name_server = '8.8.8.8' aka server_root # @ part of dig
    ADDITIONAL_RDCLASS = 65535

    domain = dns.name.from_text(target)
    if not domain.is_absolute():
        domain = domain.concatenate(dns.name.root)

    request = dns.message.make_query(domain, dns.rdatatype.A, use_edns=0) # use_edns = 0? for below code

    response = dns.query.udp(request, server_root, timeout=2.0) # timeout 2 seconds, throws timeout exception (try around it), .4

    for rrset in response.authority:
        if rrset.rdtype == dns.rdatatype.SOA and rrset.name == dns.name.root: # makes sure its the root that owns the record
            return int(rrset[0].serial)
        else:
            print("error explanation")

    return -1


def create_time_range(range, increments):
    # range being time till target, the script will test after as well
    sec_range = 60 * range

    list_time = []
    list_time.append(sec_range)

    continue_loop = True
    while sec_range > 0:
        sec_range -= increments
        list_time.append(sec_range)

    return list_time



TIME_LIST = [600, 500, 400, 300, 180, 120, 90, 60, 45, 30, 15, 10, 5, 1]

def main(argv):
    # opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    parser = OptionParser()
    parser.add_option("-f", "--file", dest = "filename",
                  help = "write report to FILE (default.txt will be the output file if argument is left empty)", metavar = "FILE")

    parser.add_option("-l", "--time_list", dest = "time_list",
                  help = "(required) list of times to target", metavar = "LIST")

    parser.add_option("-r", "--range", dest = "range",
                  help = "time till (in minutes) target, during which program will be testing target address", metavar = "RANGE")

    parser.add_option("-i", "--increment", dest = "increment",
                  help = "time between each test while testing", metavar = "INC")

    (options, args) = parser.parse_args()

    if options.filename is not None:
        file_name = options.filename
    else:
        file_name = "default.txt"

    if options.time_list is None:
        parser.print_help()
        return

    range = options.range
    if options.range is None:
        range = 10

    increment = options.increment
    if options.increment is None:
        increment = 10


    # get list of times from file
    #ip_addr = args[1]
    # exampel: dig @127.0.0.1 example.com121223 SOA
    list_of_times = get_list_times(options.time_list)

    iter = 0
    target_address = "example.com" + str(iter)
    # previous_serial = get_serial(target, "8.8.8.8")
    
    while 1:
        iter += 1
        target_address = "example.com" + str(iter)

        # where we need to feed difference between times
        current_time = createTimeStamp()
        
        # create next target time
        target_time = next_target(list_of_times, current_time)
        target_time.print_time()

        with open(file_name, 'a') as the_file:
                first = "Target: " + target_time.get_time() + "\n\n"
                the_file.write(first)


        timer_list = TIME_LIST
        # timer_list = create_time_range()
        for x in timer_list:
            iter += 1
            target_address = "example.com" + str(iter)

            result_check = checkIfTime(current_time, target_time, x, 0)
            while not result_check:
                time.sleep(1)
                print("waiting...")
                # checks to see how close the current time is to the target
                result_check = checkIfTime(current_time, target_time, x, 0)
                current_time = createTimeStamp()

            if result_check:
                current_serial = get_serial(target_address, "127.0.0.1") # double check this is what I need to feed in
                results = current_time.get_time() + " " + str(current_serial) + '\n'

                with open(file_name, 'a') as the_file:
                    the_file.write(results)


        for x in reversed(timer_list):
            iter += 1
            target_address = "example.com" + str(iter)

            result_check = negCheckIfTime(current_time, target_time, -1 * x)
            while not result_check:
                time.sleep(1)
                print("waiting... (post target)")
                # checks to see how close the current time is to the target
                result_check = negCheckIfTime(current_time, target_time, -1 * x)
                current_time = createTimeStamp()

            if result_check:
                current_serial = get_serial(target_address, "127.0.0.1")
                results = current_time.get_time() + " " + str(current_serial) + '\n'
                with open(file_name, 'a') as the_file:
                    the_file.write(results)
        with open(file_name, 'a') as the_file:
            the_file.write("\n\n\n")


if __name__ == "__main__":
    main(sys.argv[1:])

    # root changes seem to consistently be between 22:00 and 23:00, as well as between 10:00 and 11:00 (MST)
