import sys
import glob
from csv import writer
import numpy as np
import copy
import matplotlib.pyplot as plt
import datetime

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


class DataPoint:
    def __init__(self, node = 0, server = 0, ipv = 0, iter = 0, seconds = 0, timestamp = 0):
        self.node = node
        self.server = server
        self.ipv = ipv
        self.iter = iter
        self.seconds = seconds
        self.timestamp = timestamp


def create_timestamp(time):
    result = time.split(":")
    final = TimeStamps(int(result[0]), int(result[1]), float(result[2]))
    return final


def deltaTimeStamp(time_a, time_b):
    total_a_seconds = time_a.to_seconds()
    total_b_seconds = time_b.to_seconds()

    # z = y - x
    return total_b_seconds - total_a_seconds


def get_filenames():
    #file_list = glob.glob("./1test/*.txt") # Include slash or it will search in the wrong directory

    all_files = glob.glob('./**/*.txt', 
                   recursive = True)

    return all_files


def get_file_parse(file):
    ipv = 0
    if "v4" in file:
        ipv = 4
    else:
        ipv = 6

    
    parts = file.split("/")

    node = parts[1]
    server = parts[2].split("-")[0]

    return node, server, ipv


def average_list(lister):
    return sum(lister) / len(lister)


def organize_data(serial_num):
    files = get_filenames()

    # create a list of datapoint objects (2d array)
    by_serial = {}
    first_time = 0
    for file in files:
        
        with open(file) as f:
            lines = f.readlines()

            if first_time == 0:
                for line in lines:
                    temp = line.split()
                    serial = temp[1]
                    by_serial[serial] = []
                first_time = -2
            
            for line in lines:
                temp = line.split()
                time = temp[0]
                serial = temp[1]
                time_stamp = create_timestamp(time)

                node, server, ipv = get_file_parse(file)

                by_serial[serial].append(DataPoint(node, server, ipv, -1, time_stamp.to_seconds(), time_stamp))

    return by_serial


def sort_data(data):
    for key in data:
        datapoints = data[key]
        datapoints.sort(key=lambda y: y.seconds)

        data[key] = datapoints

    return data


def seconds_to_time(time_list):
    times = []
    for i in time_list:
        times.append(str(datetime.timedelta(seconds=i)))

    return times



def print_spread(data):
    # data[key] contains the sorted spread, now to move it to the excel sheet
    with open('practice.csv', 'a+', newline='') as write_obj:
        csv_writer = writer(write_obj)

        # Add spaces
        blanks = ["", "", ""]
        csv_writer.writerow(blanks)

        spread_header = ["Spread by Serial", "", ""]
        csv_writer.writerow(spread_header)

    # this is where we can start to gather data for each serial of first, first_ipv4, ect
    first_ipv4_all = []
    first_all = []
    first_ipv6_all = []

    ipv4_mean = []
    ipv4_median = []
    ipv4_75 = []
    ipv4_90 = []
    ipv4_max = []

    ipv6_mean = []
    ipv6_median = []
    ipv6_75 = []
    ipv6_90 = []
    ipv6_max = []

    for key in data:
        datapoints = data[key]

        names = []
        time_stamps = []
        deltas = []

        # add percentiles by ipv
        ipv4_deltas = []
        ipv6_deltas = []

        first_in_order_seconds = datapoints[0].seconds

        for val in datapoints:
            
            name = val.node + "-" + val.server + "-" + str(val.ipv)
            names.append(name)
            time_stamps.append(val.timestamp.get_time())
            # deltas.append(val[1])

            if val.ipv == 4:
                ipv4_deltas.append(val.seconds - first_in_order_seconds)
            elif val.ipv == 6:
                ipv6_deltas.append(val.seconds - first_in_order_seconds)

            deltas.append(val.seconds - first_in_order_seconds)


        percentiles_v4 = ["ipv4"]
        if len(ipv4_deltas) > 0:
            percentiles_v4.append(average_list(ipv4_deltas))
            percentiles_v4.append(np.percentile(ipv4_deltas, 25))
            percentiles_v4.append(np.percentile(ipv4_deltas, 50))
            percentiles_v4.append(np.percentile(ipv4_deltas, 75))
            percentiles_v4.append(np.percentile(ipv4_deltas, 90))
            percentiles_v4.append(max(ipv4_deltas))

        percentiles_v6 = ["ipv6"]
        if len(ipv6_deltas) > 0:
            percentiles_v6.append(average_list(ipv6_deltas))
            percentiles_v6.append(np.percentile(ipv6_deltas, 25))
            percentiles_v6.append(np.percentile(ipv6_deltas, 50))
            percentiles_v6.append(np.percentile(ipv6_deltas, 75))
            percentiles_v6.append(np.percentile(ipv6_deltas, 90))
            percentiles_v6.append(max(ipv6_deltas))

        percentiles_both = ["ipv4/6"]
        if len(ipv6_deltas) > 0 and len(ipv6_deltas) > 0:
            percentiles_both.append(average_list(deltas))
            percentiles_both.append(np.percentile(deltas, 25))
            percentiles_both.append(np.percentile(deltas, 50))
            percentiles_both.append(np.percentile(deltas, 75))
            percentiles_both.append(np.percentile(deltas, 90))
            percentiles_both.append(max(ipv4_deltas))


        # adding for the nice graphs
        ipv4_mean.append(average_list(ipv4_deltas))
        ipv4_median.append(np.percentile(ipv4_deltas, 50))
        ipv4_75.append(np.percentile(ipv4_deltas, 75))
        ipv4_90.append(np.percentile(ipv4_deltas, 90))
        ipv4_max.append(max(ipv4_deltas))

        ipv6_mean.append(average_list(ipv6_deltas))
        ipv6_median.append(np.percentile(ipv6_deltas, 50))
        ipv6_75.append(np.percentile(ipv6_deltas, 75))
        ipv6_90.append(np.percentile(ipv6_deltas, 90))
        ipv6_max.append(max(ipv6_deltas))


        names.insert(0, "Name")
        time_stamps.insert(0, "Time")
        deltas.insert(0, "Lag Time")


        first_ipv4 = None
        for i in range(len(datapoints)):
            if datapoints[i].ipv == 4:
                first_ipv4 = datapoints[i]
                break

        first_ipv6 = None
        for i in range(len(datapoints)):
            if datapoints[i].ipv == 6:
                first_ipv6 = datapoints[i]
                break

        first = datapoints[0]

        first_info = ["First", first.node, first.server, first.ipv]

        first_ipv4_info = []
        if first_ipv4 != None:
            first_ipv4_info = ["First_ipv4", first_ipv4.node, first_ipv4.server, first_ipv4.ipv]
        
        first_ipv6_info = []
        if first_ipv6 != None:
            first_ipv6_info = ["First_ipv6", first_ipv6.node, first_ipv6.server, first_ipv6.ipv]

        # adding to the collection
        first_ipv4_all.append((key, first_ipv4))
        first_all.append((key, first))
        first_ipv6_all.append((key, first_ipv6))

        with open('practice.csv', 'a+', newline='') as write_obj:
            serial = [key]

            csv_writer = writer(write_obj)

            csv_writer.writerow(serial)
            csv_writer.writerow(names)
            csv_writer.writerow(time_stamps)
            csv_writer.writerow(deltas)

            csv_writer.writerow(first_info)
            csv_writer.writerow(first_ipv4_info)
            csv_writer.writerow(first_ipv6_info)

            csv_writer.writerow(["", "Average", "25%", "50%", "75%", "90%", "Max"])
            csv_writer.writerow(percentiles_v4)
            csv_writer.writerow(percentiles_v6)
            csv_writer.writerow(percentiles_both)

            blanks = ["", "", ""]
            csv_writer.writerow(blanks)

    # create a pad for the next one
    with open('practice.csv', 'a+', newline='') as write_obj:
        csv_writer = writer(write_obj)
        blanks = ["", "", ""]
        csv_writer.writerow(blanks)
        csv_writer.writerow(blanks)
        csv_writer.writerow(blanks)

    # make graphs with matplotlib
    serials = []
    ipv4_times = []
    first_times = []
    ipv6_times = []
    for i in first_ipv4_all:
        serials.append(int(i[0]))
        ipv4_times.append(i[1].seconds)

    for j in first_ipv6_all:
        # serials.append(int(j[0]))
        ipv6_times.append(j[1].seconds)
    
    for k in first_all:
        first_times.append(k[1].seconds)


    # create dictionary of key|[] to seperate by nodes
    nodes = []
    servers = []
    files = get_filenames()
    for file in files:
        node, server, ipv = get_file_parse(file)
        nodes.append(node)
        servers.append(server)

    # remove duplicates
    nodes = list(set(nodes))
    servers = list(set(servers)) # remove anything with .txt in it, then distinguish by ipv
    temp_servers = servers
    servers = []

    for t in temp_servers:
        if ".txt" not in t:
            servers.append(t)

    data_by_nodes = {}
    for n in nodes:
        for key in data: # key is the serial
            data_list = data[key]
            for d in data_list:
                if d.node == n:
                    if n not in data_by_nodes:
                        data_by_nodes[n] = []
                    else:
                        data_by_nodes[n].append((key, d))


    x = [str(x) for x in serials]

    # by nodes then graph by servers for each node
    # we will title each graph by its node, then the lines will be by server...
    for n in nodes:
        time_list_by_server_v4 = {}
        time_list_by_server_v6 = {}
        serials_ipv4 = {}
        serials_ipv6 = {}
        for i in data_by_nodes[n]:
            for j in servers:
                if j not in time_list_by_server_v4:
                    time_list_by_server_v4[j] = []
                    serials_ipv4[j] = []
                else:
                    if j == i[1].server and i[1].ipv == 4:
                        time_list_by_server_v4[j].append(i[1].seconds)
                        serials_ipv4[j].append(i[0])
                    
                if j not in time_list_by_server_v6:
                    time_list_by_server_v6[j] = []
                    serials_ipv6[j] = []
                else:
                    if j == i[1].server and i[1].ipv == 6:
                        time_list_by_server_v6[j].append(i[1].seconds)
                        serials_ipv6[j].append(i[0])
                    
        

        for j in servers:
            temp_x = []
            for k in serials_ipv4[j]:
                temp_x.append(int(k))
            temp_x.sort()

            serials_ipv4[j] = []
            for k in temp_x:
                serials_ipv4[j].append(str(k))

            plt.plot(serials_ipv4[j], time_list_by_server_v4[j], label = j + "-ipv4")
              
        plt.title(n + " ipv4")
        plt.ylabel('Time')
        plt.xlabel('Serial')
        plt.xticks(rotation=90)
        plt.legend()
        # plt.title("By Nodes")
        plt.tight_layout()
        plt.show()

        for j in servers:
            temp_x = []
            for k in serials_ipv6[j]:
                temp_x.append(int(k))
            temp_x.sort()

            serials_ipv6[j] = []
            for k in temp_x:
                serials_ipv6[j].append(str(k))

            plt.plot(serials_ipv6[j], time_list_by_server_v6[j], label = j + "-ipv6")

        plt.title(n + " ipv6")
        plt.ylabel('Time')
        plt.xlabel('Serial')
        plt.xticks(rotation=90)
        plt.legend()
        # plt.title("By Nodes")
        plt.tight_layout()
        plt.show()




    # serials = [str(x) for x in serials]
    # x = [str(x) for x in serials]

    plt.plot(x, ipv4_times, label = "ipv4")
    plt.plot(x, ipv6_times, label = "ipv6")
    plt.ylabel('')
    plt.xlabel('Serial')
    # plt.tick_params(axis='x', labelsize=5)
    plt.xticks(rotation=90)
    plt.legend()
    plt.title("First to Update")
    plt.tight_layout()
    plt.show()


    # for the mean, median, percentiles, etc
    # plt.plot(x, ipv4_mean, label = "ipv4 averages", linewidth = 1)
    # plt.plot(x, ipv4_median, label = "ipv4 medians", linewidth = 1)
    # plt.plot(x, ipv4_75, label = "ipv4 75%", linewidth = 1)
    # plt.plot(x, ipv4_90, label = "ipv4 90%", linewidth = 1)
    # plt.plot(x, ipv4_max, label = "ipv4 maxes", linewidth = 1)

    # plt.plot(x, ipv6_mean, label = "ipv6 averages", linewidth = 1)
    # plt.plot(x, ipv6_median, label = "ipv6 medians", linewidth = 1)
    # plt.plot(x, ipv6_75, label = "ipv6 75%", linewidth = 1)
    # plt.plot(x, ipv6_90, label = "ipv6 90%", linewidth = 1)
    # plt.plot(x, ipv6_max, label = "ipv6 maxes", linewidth = 1)


    # plt.ylabel('lag time')
    # plt.xlabel('serial update')
    # plt.tick_params(axis='x', labelsize=5)
    # plt.legend()
    # plt.title("Lag Time")
    # plt.show()






    plt.style.use('_mpl-gallery')

    
    # size and color:
    # sizes = np.random.uniform(15, 80, len(x))
    # colors = np.random.uniform(15, 80, len(x))

    # plot
    #fig, ax = plt.subplots()

    print(type(x[0]))
    print(type(ipv4_mean[0]))

    plt.scatter(x, ipv4_mean, label="ipv4_mean", s=100, alpha = 0.5)
    
    plt.scatter(x, ipv6_mean, label="ipv6_mean", marker="s", s=100, alpha = 0.5)
    plt.scatter(x, ipv4_median, label="ipv4_median", s=100, alpha = 0.5)
    plt.scatter(x, ipv6_median, label="ipv6_median", marker="s", s=100, alpha = 0.5)
    plt.scatter(x, ipv4_75, label="ipv4_75", s=100, alpha = 0.5)
    plt.scatter(x, ipv6_75, label="ipv6_75", marker="s", s=100, alpha = 0.5)
    plt.scatter(x, ipv4_90, label="ipv4_90", s=100, alpha = 0.5)
    plt.scatter(x, ipv6_90, label="ipv6_90", marker="s", s=100, alpha = 0.5)
    plt.scatter(x, ipv4_max, label="ipv4_max", s=100, alpha = 0.5)
    plt.scatter(x, ipv6_max, label="ipv6_max", marker="s", s=100, alpha = 0.5)

    plt.tight_layout()
    plt.ylabel('Lag Time (Seconds)')
    plt.xlabel('Serial')
    plt.xticks(rotation=90)
    plt.legend()
    plt.show()
    plt.close()



def process(serial_num):
    # we don't really need a neat n x m table
    # focus on flexibility of data points to use in spreads

    # get the rows by serial number (dictionary set up)
    organized = organize_data(serial_num)

    sorted = sort_data(organized)

    print_spread(sorted)
    
    
def main(argv):
    serial_num = 2022022500
    if len(argv) > 0:
        serial_num = int(argv[0])
    process(serial_num)


if __name__ == "__main__":
    main(sys.argv[1:])