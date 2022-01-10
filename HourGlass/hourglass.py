import subprocess, sys, getopt
from datetime import datetime, timedelta
import time
from threading import Timer
import math


def find_line_num(lines):
    string_to_find = 'AUTHORITY SECTION:'
    for i in range(len(lines)):
        if lines[i].find('AUTHORITY SECTION:') > -1:
            return i + 1
    
    return -1

def decode_to_strings(lines):
    new_lines = []
    for x in lines:
        new_lines.append(x.decode("utf-8"))

    return new_lines


def get_serial(target):
    # dig 199.7.91.13 @127.0.0.1 SOA
    
    old_lines = subprocess.run(["dig", target, "@h.root-servers.net", "SOA"], stdout=subprocess.PIPE).stdout.splitlines()
    # ls_lines = subprocess.run(['ls', '-l'], stdout=subprocess.PIPE).stdout.splitlines()

    lines = decode_to_strings(old_lines)
    
    line_num = find_line_num(lines)
    if line_num > -1:
        serial_line = lines[line_num]
        serial_list = serial_line.split()
        #return serial_list[6]

        ct = datetime.now()
        print(ct, serial_list[6])
    else:
        print("ERROR: Could not find the correct line number for the serial.")
        exit()


def timer_call(target, target_time, hour_delta = 0, minute_delta = 0, second_delta = 1):
    # target_time = datetime.today()
    

    edited_sec = target_time.second + second_delta
    if edited_sec >= 60:
        add_min = math.floor(edited_sec / 60)
        edited_sec = edited_sec % 60
        minute_delta += add_min

    # x = target_time.replace(hour = x.hour + hour_delta, minute = x.minute + minute_delta, second = edited_sec, microsecond = 0)
    #delta_t = y - target_time



    x = datetime.now().time()
    print("x", type(x))

    target_datetime = datetime.combine(datetime.now(), target_time)
    x_datetime = datetime.combine(datetime.now(), x)

    delta_t = target_datetime - x_datetime

    print("y day", target_time.day)
    print("delta_t", delta_t)

    # secs = delta_t.total_seconds()
    
    if 11 < 10:
        print("success")
        t = Timer(secs, get_serial, [target]) # timer is a thread subclass
        t.start()


def stamp_parser(stamp):
    # 22:17:44.262345
    split_results = stamp.split(":")
    hour = split_results[0]
    minute = split_results[1]
    second = split_results[2]

    return int(hour), int(minute), int(math.floor(float(second)))


def main(argv):
    opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])

    iter = 0
    previous_serial = 0
    target = "example.com" + str(iter)

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
