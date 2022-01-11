import sys, getopt
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
        print(iter)
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

    request = dns.message.make_query(domain, dns.rdatatype.ANY)
    request.flags |= dns.flags.AD
    request.find_rrset(request.additional, dns.name.root, ADDITIONAL_RDCLASS,
                    dns.rdatatype.OPT, create=True, force_unique=True)
    response = dns.query.udp(request, server_root)


    for rrset in response.authority:
        if rrset.rdtype == dns.rdatatype.SOA:
            return int(rrset[0].serial)

    return -1


def main(argv):
    opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])

    # get list of times from file
    #ip_addr = args[1]
    # exampel: dig @127.0.0.1 example.com121223 SOA
    list_of_times = get_list_times(args[0])
    

    iter = 0
    target = "example.com" + str(iter)
    # previous_serial = get_serial(target, "8.8.8.8")
    

    while 1:
        # where we need to feed difference between times
        current_time = createTimeStamp()
        
        # create next target time
        target_time = next_target(list_of_times, current_time)
        target_time.print_time()

        timer_list = [300, 180, 120, 90, 60, 45, 30, 15, 10, 5, 1]
        for x in timer_list:
            result_check = checkIfTime(current_time, target_time, x, 0)
            while not result_check:
                time.sleep(1)
                print("waiting...")
                # checks to see how close the current time is to the target
                result_check = checkIfTime(current_time, target_time, x, 0)
                current_time = createTimeStamp()

            if result_check:
                current_serial = get_serial(target, "8.8.8.8")
                results = current_time.get_time() + " " + str(current_serial) + '\n'

                with open('somefile.txt', 'a') as the_file:
                    the_file.write(results)

        prev_time = 0
        for x in reversed(timer_list):
            result_check = checkIfTime(current_time, target_time, prev_time, -1 * x)
            while not result_check:
                time.sleep(1)
                print("waiting... (post target)")
                # checks to see how close the current time is to the target
                result_check = checkIfTime(current_time, target_time, prev_time, -1 * x)
                current_time = createTimeStamp()

            if result_check:
                prev_time = -1 * x
                current_serial = get_serial(target, "8.8.8.8")
                results = current_time.get_time() + " " + str(current_serial) + '\n'
                with open('somefile.txt', 'a') as the_file:
                    the_file.write(results)



if __name__ == "__main__":
    main(sys.argv[1:])
