import sys
import glob
from csv import writer
import numpy as np
import copy
import matplotlib.pyplot as plt
import datetime
from datetime import time
import matplotlib.dates as mdates
import pandas as pd

server_translation = {"WIDE" : "m", "verisign(a)" : "a", "USC" : "b", "ISC" : "f", "NASA" : "e", "UM" : "d",
"Netnod" : "i", "RIPE" : "k", "Army" : "h", "CogentCom" : "c", "US_DD(NIC)" : "g", "verisign(j)" : "j", "ICANN" : "l"}


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
        self.delta = -1


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
                   recursive = True) # to split into two groups, have two folders, best and worst case scenarios

    return all_files


def get_worst_filenames():
    #file_list = glob.glob("./1test/*.txt") # Include slash or it will search in the wrong directory

    all_files = glob.glob('./worst_case/**/*.txt', 
                   recursive = True) # to split into two groups, have two folders, best and worst case scenarios

    return all_files


def get_best_filenames():
    #file_list = glob.glob("./1test/*.txt") # Include slash or it will search in the wrong directory

    all_files = glob.glob('./best_case/**/*.txt', 
                   recursive = True) # to split into two groups, have two folders, best and worst case scenarios

    return all_files


def get_file_parse(file):
    ipv = 0
    if "v4" in file:
        ipv = 4
    else:
        ipv = 6

    
    parts = file.split("/")

    case = parts[1]
    node = parts[2]
    server = parts[3].split("-")[0]

    return node, server, ipv


def average_list(lister):
    return sum(lister) / len(lister)


def organize_data_worst(serial_num):
    files = get_worst_filenames()

    # create a list of datapoint objects (2d array)
    by_serial = {}
    first_time = 0
    for file in files:
        
        with open(file) as f:
            lines = f.readlines() # perhaps find the file with most lines to do this...

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

                # added
                if serial not in by_serial:
                    by_serial[serial] = []

                by_serial[serial].append(DataPoint(node, server, ipv, -1, time_stamp.to_seconds(), time_stamp))

    return by_serial


def organize_data_best(serial_num):
    files = get_best_filenames()

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

                # added
                if serial not in by_serial:
                    by_serial[serial] = []

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


def pre_print_spread(data):
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
    files = get_worst_filenames()
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

    data_by_servers = {}
    for n in servers:
        for key in data: # key is the serial
            data_list = data[key]
            for d in data_list:
                if d.server == n:
                    if n not in data_by_servers:
                        data_by_servers[n] = []
                    else:
                        data_by_servers[n].append((key, d))


    x = [str(x) for x in serials]


    return nodes, data_by_nodes, servers, data_by_servers # serials


def seconds_to_timestamps(times):
    new_times = []
    for t in times:
        m, s = divmod(t, 60)
        h, m = divmod(m, 60)

        my_day = datetime.date(2014, 7, 15)

        if h >= 24:
            h -= 24

        my_time = time(int(h), int(m), int(s))

        new_times.append(datetime.datetime.combine(my_day, my_time))

    return new_times


def create_graphs(nodes, data_by_nodes_worst, data_by_nodes_best, servers, all_deltas, all_names, 
all_nodes, all_servers, all_ipv, all_serials):
    # key accessed (node name is the key)
    # [0] is worst case, [1] is best case
    # by nodes then graph by servers for each node
    # we will title each graph by its node, then the lines will be by server...
    for n in nodes:
        time_list_by_server_v4_worst = {}
        time_list_by_server_v6_worst = {}
        serials_ipv4_worst = {}
        serials_ipv6_worst = {}

        time_list_by_server_v4_best = {}
        time_list_by_server_v6_best = {}
        serials_ipv4_best = {}
        serials_ipv6_best = {}

        for i in range(len(data_by_nodes_worst[n])):
            for j in servers:
                if j not in time_list_by_server_v4_worst:
                    time_list_by_server_v4_worst[j] = []
                    serials_ipv4_worst[j] = []

                if j not in time_list_by_server_v4_best:
                    time_list_by_server_v4_best[j] = []
                    serials_ipv4_best[j] = []

                if j == data_by_nodes_worst[n][i][1].server and data_by_nodes_worst[n][i][1].ipv == 4:
                        time_list_by_server_v4_worst[j].append(data_by_nodes_worst[n][i][1].seconds)
                        serials_ipv4_worst[j].append(data_by_nodes_worst[n][i][0])
                if j == data_by_nodes_best[n][i][1].server and data_by_nodes_best[n][i][1].ipv == 4:
                        time_list_by_server_v4_best[j].append(data_by_nodes_best[n][i][1].seconds)
                        serials_ipv4_best[j].append(data_by_nodes_best[n][i][0])
                    
                if j not in time_list_by_server_v6_worst:
                    time_list_by_server_v6_worst[j] = []
                    serials_ipv6_worst[j] = []
                if j not in time_list_by_server_v6_best:
                    time_list_by_server_v6_best[j] = []
                    serials_ipv6_best[j] = []

                if j == data_by_nodes_worst[n][i][1].server and data_by_nodes_worst[n][i][1].ipv == 6:
                    time_list_by_server_v6_worst[j].append(data_by_nodes_worst[n][i][1].seconds)
                    serials_ipv6_worst[j].append(data_by_nodes_worst[n][i][0])
                if j == data_by_nodes_best[n][i][1].server and data_by_nodes_best[n][i][1].ipv == 6:
                    time_list_by_server_v6_best[j].append(data_by_nodes_best[n][i][1].seconds)
                    serials_ipv6_best[j].append(data_by_nodes_best[n][i][0])


        lag_list_by_server_v4_worst = {}
        lag_list_by_server_v6_worst = {}
        lag_serials_ipv4_worst = {}
        lag_serials_ipv6_worst = {} 

        lag_list_by_server_v4_best = {}
        lag_list_by_server_v6_best = {}
        lag_serials_ipv4_best = {}
        lag_serials_ipv6_best = {} 

        for key in all_deltas[0]:
            for i in range(len(all_deltas[0][key])):
                for j in servers:
                    if j not in lag_list_by_server_v4_worst:
                        lag_list_by_server_v4_worst[j] = []
                        lag_serials_ipv4_worst[j] = []

                    if j == all_servers[0][key][i] and all_ipv[0][key][i] == 4 and all_nodes[0][key][i] == n:
                        lag_list_by_server_v4_worst[j].append(all_deltas[0][key][i])
                        lag_serials_ipv4_worst[j].append(key) #serials

                    if j not in lag_list_by_server_v6_worst:
                        lag_list_by_server_v6_worst[j] = []
                        lag_serials_ipv6_worst[j] = []

                    if j == all_servers[0][key][i] and all_ipv[0][key][i] == 6 and all_nodes[0][key][i] == n:
                        lag_list_by_server_v6_worst[j].append(all_deltas[0][key][i])
                        lag_serials_ipv6_worst[j].append(key) #serials


                    if j not in lag_list_by_server_v4_best:
                        lag_list_by_server_v4_best[j] = []
                        lag_serials_ipv4_best[j] = []

                    if j == all_servers[1][key][i] and all_ipv[1][key][i] == 4 and all_nodes[1][key][i] == n:
                        lag_list_by_server_v4_best[j].append(all_deltas[1][key][i])
                        lag_serials_ipv4_best[j].append(key) #serials

                    if j not in lag_list_by_server_v6_best:
                        lag_list_by_server_v6_best[j] = []
                        lag_serials_ipv6_best[j] = []

                    if j == all_servers[1][key][i] and all_ipv[1][key][i] == 6 and all_nodes[1][key][i] == n:
                        lag_list_by_server_v6_best[j].append(all_deltas[1][key][i])
                        lag_serials_ipv6_best[j].append(key) #serials

                    

                    
        
        # move to new function- needs servers, serials_ipv4/6, time_list_by_server_v4/6
        # the actual plot function needs to take best and worst case for both

        # call in this indentation
        fig, axs = plt.subplots(2, 2)
        counter = 0
        for j in servers:
            style = 'dashdot'
            temp_x = []
            for k in serials_ipv4_worst[j]: # bug?
                temp_x.append(int(k))
            temp_x.sort()

            if len(temp_x) > 0 and temp_x[-1] == 2022022500: # NOTE: debugging only
                print("ooooooooooof")

            serials_ipv4_worst[j] = []
            for k in temp_x:
                serials_ipv4_worst[j].append(str(k))
            

            # time_list_servers have the times
            # create time stamps from seconds and add it to new array, which will be fed in to replace just seconds
            worst_times = seconds_to_timestamps(time_list_by_server_v4_worst[j])
            counter += 1
            
            if counter > 10:
                axs[0, 0].plot(serials_ipv4_worst[j], worst_times, label = j + "-ipv4", linestyle = style)
            else:
                axs[0, 0].plot(serials_ipv4_worst[j], worst_times, label = j + "-ipv4")
            
            for tick in axs[0, 0].get_xticklabels():
                tick.set_rotation(90)
                tick.set_fontsize(5)

            myFmt = mdates.DateFormatter('%H:%M:%S')
            axs[0, 0].yaxis.set_major_formatter(myFmt)

            axs[0, 0].set_ylabel('Time')
            axs[0, 0].set_xlabel('Serial')
            axs[0, 0].set_title(n + " ipv4" + " (Worst Case)")
            # ax1.tight_layout()

            
            best_times = seconds_to_timestamps(time_list_by_server_v4_best[j])

            # ax2.plot(serials_ipv4_best[j], best_times, label = j + "-ipv4")
            if counter > 10:
                axs[0, 1].plot(serials_ipv4_worst[j], best_times, label = j + "-ipv4", linestyle = style)
            else:
                axs[0, 1].plot(serials_ipv4_worst[j], best_times, label = j + "-ipv4")
            for tick in axs[0, 1].get_xticklabels():
                tick.set_rotation(90)
                tick.set_fontsize(5)

            myFmt = mdates.DateFormatter('%H:%M:%S')
            axs[0, 1].yaxis.set_major_formatter(myFmt)

            axs[0, 1].set_ylabel('Time')
            axs[0, 1].set_xlabel('Serial')
            axs[0, 1].set_title(n + " ipv4" + " (Best Case)")


            # lag times for worst case scenario
            if counter > 10:
                axs[1, 0].plot(lag_serials_ipv4_worst[j], lag_list_by_server_v4_worst[j], label = j + "-ipv4", linestyle = style)
            else:
                axs[1, 0].plot(lag_serials_ipv4_worst[j], lag_list_by_server_v4_worst[j], label = j + "-ipv4")
            for tick in axs[1, 0].get_xticklabels():
                tick.set_rotation(90)
                tick.set_fontsize(5)

            axs[1, 0].set_ylabel('Lag Time (seconds)')
            axs[1, 0].set_xlabel('Serial')
            axs[1, 0].set_title(n + " ipv4" + " (Worst Case)")


            # lag times for best case scenario
            if counter > 10:
                axs[1, 1].plot(lag_serials_ipv4_best[j], lag_list_by_server_v4_best[j], label = j + "-ipv4", linestyle = style)
            else:
                axs[1, 1].plot(lag_serials_ipv4_best[j], lag_list_by_server_v4_best[j], label = j + "-ipv4")
            for tick in axs[1, 1].get_xticklabels():
                tick.set_rotation(90)
                tick.set_fontsize(5)


            axs[1, 1].set_ylabel('Lag Time (seconds)')
            axs[1, 1].set_xlabel('Serial')
            axs[1, 1].set_title(n + " ipv4" + " (Best Case)")
            # axs.set_xticks(5) #!!!!!!!
            

        # axs[1, 0].get_shared_y_axes().join(axs[1, 0], axs[1, 1]) # joins the bottom two's axes
        plt.tight_layout()
        plt.legend(bbox_to_anchor=(-1.68, 0.78))
        # plt.locator_params(axis='x', nbins=5)
        plt.show()
        


        fig, axs = plt.subplots(2, 2)
        counter = 0
        for j in servers:
            style = 'dashdot'
            temp_x = []
            for k in serials_ipv6_worst[j]: # bug?
                temp_x.append(int(k))
            temp_x.sort()

            if len(temp_x) > 0 and temp_x[-1] == 2022022500: # NOTE: debugging only
                print("ooooooooooof")

            serials_ipv6_worst[j] = []
            for k in temp_x:
                serials_ipv6_worst[j].append(str(k))
            

            # time_list_servers have the times
            # create time stamps from seconds and add it to new array, which will be fed in to replace just seconds
            worst_times = seconds_to_timestamps(time_list_by_server_v6_worst[j])
            counter += 1
            
            if counter > 10:
                axs[0, 0].plot(serials_ipv6_worst[j], worst_times, label = j + "-ipv6", linestyle = style)
            else:
                axs[0, 0].plot(serials_ipv6_worst[j], worst_times, label = j + "-ipv6")
            
            for tick in axs[0, 0].get_xticklabels():
                tick.set_rotation(90)
                tick.set_fontsize(5)

            myFmt = mdates.DateFormatter('%H:%M:%S')
            axs[0, 0].yaxis.set_major_formatter(myFmt)

            axs[0, 0].set_ylabel('Time')
            axs[0, 0].set_xlabel('Serial')
            axs[0, 0].set_title(n + " ipv6" + " (Worst Case)")
            # ax1.tight_layout()

            
            best_times = seconds_to_timestamps(time_list_by_server_v6_best[j])

            # ax2.plot(serials_ipv6_best[j], best_times, label = j + "-ipv6")
            if counter > 10:
                axs[0, 1].plot(serials_ipv6_worst[j], best_times, label = j + "-ipv6", linestyle = style)
            else:
                axs[0, 1].plot(serials_ipv6_worst[j], best_times, label = j + "-ipv6")
            for tick in axs[0, 1].get_xticklabels():
                tick.set_rotation(90)
                tick.set_fontsize(5)

            myFmt = mdates.DateFormatter('%H:%M:%S')
            axs[0, 1].yaxis.set_major_formatter(myFmt)

            axs[0, 1].set_ylabel('Time')
            axs[0, 1].set_xlabel('Serial')
            axs[0, 1].set_title(n + " ipv6" + " (Best Case)")


            # lag times for worst case scenario
            if counter > 10:
                axs[1, 0].plot(lag_serials_ipv6_worst[j], lag_list_by_server_v6_worst[j], label = j + "-ipv6", linestyle = style)
            else:
                axs[1, 0].plot(lag_serials_ipv6_worst[j], lag_list_by_server_v6_worst[j], label = j + "-ipv6")
            for tick in axs[1, 0].get_xticklabels():
                tick.set_rotation(90)
                tick.set_fontsize(5)

            axs[1, 0].set_ylabel('Lag Time (seconds)')
            axs[1, 0].set_xlabel('Serial')
            axs[1, 0].set_title(n + " ipv6" + " (Worst Case)")


            # lag times for best case scenario
            if counter > 10:
                axs[1, 1].plot(lag_serials_ipv6_best[j], lag_list_by_server_v6_best[j], label = j + "-ipv6", linestyle = style)
            else:
                axs[1, 1].plot(lag_serials_ipv6_best[j], lag_list_by_server_v6_best[j], label = j + "-ipv6")
            for tick in axs[1, 1].get_xticklabels():
                tick.set_rotation(90)
                tick.set_fontsize(5)


            axs[1, 1].set_ylabel('Lag Time (seconds)')
            axs[1, 1].set_xlabel('Serial')
            axs[1, 1].set_title(n + " ipv6" + " (Best Case)")
            

        plt.tight_layout()
        plt.legend(bbox_to_anchor=(-1.68, 0.78))
        plt.show()


def create_graphs_by_server(nodes, data_by_nodes_worstest, data_by_nodes_bestest, servers, all_deltas, all_names, 
all_nodes, all_servers, all_ipv, all_serials, data_by_servers_worst, data_by_servers_best):
    # for this change, all server <-> node
    for n in servers:
        time_list_by_node_v4_worst = {}
        time_list_by_node_v6_worst = {}
        serials_ipv4_worst = {}
        serials_ipv6_worst = {}

        time_list_by_node_v4_best = {}
        time_list_by_node_v6_best = {}
        serials_ipv4_best = {}
        serials_ipv6_best = {}

        for i in range(len(data_by_servers_worst[n])):
            for j in nodes:
                if j not in time_list_by_node_v4_worst:
                    time_list_by_node_v4_worst[j] = []
                    serials_ipv4_worst[j] = []

                if j not in time_list_by_node_v4_best:
                    time_list_by_node_v4_best[j] = []
                    serials_ipv4_best[j] = []

                if j == data_by_servers_worst[n][i][1].node and data_by_servers_worst[n][i][1].ipv == 4:
                        time_list_by_node_v4_worst[j].append(data_by_servers_worst[n][i][1].seconds)
                        serials_ipv4_worst[j].append(data_by_servers_worst[n][i][0])
                if j == data_by_servers_best[n][i][1].node and data_by_servers_best[n][i][1].ipv == 4:
                        time_list_by_node_v4_best[j].append(data_by_servers_best[n][i][1].seconds)
                        serials_ipv4_best[j].append(data_by_servers_best[n][i][0])
                    
                if j not in time_list_by_node_v6_worst:
                    time_list_by_node_v6_worst[j] = []
                    serials_ipv6_worst[j] = []
                if j not in time_list_by_node_v6_best:
                    time_list_by_node_v6_best[j] = []
                    serials_ipv6_best[j] = []

                if j == data_by_servers_worst[n][i][1].node and data_by_servers_worst[n][i][1].ipv == 6:
                    time_list_by_node_v6_worst[j].append(data_by_servers_worst[n][i][1].seconds)
                    serials_ipv6_worst[j].append(data_by_servers_worst[n][i][0])
                if j == data_by_servers_best[n][i][1].node and data_by_servers_best[n][i][1].ipv == 6:
                    time_list_by_node_v6_best[j].append(data_by_servers_best[n][i][1].seconds)
                    serials_ipv6_best[j].append(data_by_servers_best[n][i][0])


        lag_list_by_node_v4_worst = {}
        lag_list_by_node_v6_worst = {}
        lag_serials_ipv4_worst = {}
        lag_serials_ipv6_worst = {} 

        lag_list_by_node_v4_best = {}
        lag_list_by_node_v6_best = {}
        lag_serials_ipv4_best = {}
        lag_serials_ipv6_best = {} 

        for key in all_deltas[0]:
            for i in range(len(all_deltas[0][key])):
                for j in nodes:
                    if j not in lag_list_by_node_v4_worst:
                        lag_list_by_node_v4_worst[j] = []
                        lag_serials_ipv4_worst[j] = []

                    if j == all_nodes[0][key][i] and all_ipv[0][key][i] == 4 and all_servers[0][key][i] == n:
                        lag_list_by_node_v4_worst[j].append(all_deltas[0][key][i])
                        lag_serials_ipv4_worst[j].append(key) #serials

                    if j not in lag_list_by_node_v6_worst:
                        lag_list_by_node_v6_worst[j] = []
                        lag_serials_ipv6_worst[j] = []

                    if j == all_nodes[0][key][i] and all_ipv[0][key][i] == 6 and all_servers[0][key][i] == n:
                        lag_list_by_node_v6_worst[j].append(all_deltas[0][key][i])
                        lag_serials_ipv6_worst[j].append(key) #serials


                    if j not in lag_list_by_node_v4_best:
                        lag_list_by_node_v4_best[j] = []
                        lag_serials_ipv4_best[j] = []

                    if j == all_nodes[1][key][i] and all_ipv[1][key][i] == 4 and all_servers[1][key][i] == n:
                        lag_list_by_node_v4_best[j].append(all_deltas[1][key][i])
                        lag_serials_ipv4_best[j].append(key) #serials

                    if j not in lag_list_by_node_v6_best:
                        lag_list_by_node_v6_best[j] = []
                        lag_serials_ipv6_best[j] = []

                    if j == all_nodes[1][key][i] and all_ipv[1][key][i] == 6 and all_servers[1][key][i] == n:
                        lag_list_by_node_v6_best[j].append(all_deltas[1][key][i])
                        lag_serials_ipv6_best[j].append(key) #serials

                    

                    
        
        # move to new function- needs servers, serials_ipv4/6, time_list_by_server_v4/6
        # the actual plot function needs to take best and worst case for both

        # call in this indentation
        fig, axs = plt.subplots(2, 2)
        counter = 0
        for j in nodes:
            style = 'dashdot'
            temp_x = []
            for k in serials_ipv4_worst[j]: # bug?
                temp_x.append(int(k))
            temp_x.sort()

            if len(temp_x) > 0 and temp_x[-1] == 2022022500: # NOTE: debugging only
                print("ooooooooooof")

            serials_ipv4_worst[j] = []
            for k in temp_x:
                serials_ipv4_worst[j].append(str(k))
            

            # time_list_servers have the times
            # create time stamps from seconds and add it to new array, which will be fed in to replace just seconds
            worst_times = seconds_to_timestamps(time_list_by_node_v4_worst[j])
            counter += 1
            
            if counter > 10:
                axs[0, 0].plot(serials_ipv4_worst[j], worst_times, label = j + "-ipv4", linestyle = style)
            else:
                axs[0, 0].plot(serials_ipv4_worst[j], worst_times, label = j + "-ipv4")
            
            for tick in axs[0, 0].get_xticklabels():
                tick.set_rotation(90)
                tick.set_fontsize(5)

            myFmt = mdates.DateFormatter('%H:%M:%S')
            axs[0, 0].yaxis.set_major_formatter(myFmt)

            axs[0, 0].set_ylabel('Time')
            axs[0, 0].set_xlabel('Serial')
            axs[0, 0].set_title(server_translation[n] + " ipv4" + " (Worst Case)")
            # ax1.tight_layout()

            
            best_times = seconds_to_timestamps(time_list_by_node_v4_best[j])

            # ax2.plot(serials_ipv4_best[j], best_times, label = j + "-ipv4")
            if counter > 10:
                axs[0, 1].plot(serials_ipv4_worst[j], best_times, label = j + "-ipv4", linestyle = style)
            else:
                axs[0, 1].plot(serials_ipv4_worst[j], best_times, label = j + "-ipv4")
            for tick in axs[0, 1].get_xticklabels():
                tick.set_rotation(90)
                tick.set_fontsize(5)

            myFmt = mdates.DateFormatter('%H:%M:%S')
            axs[0, 1].yaxis.set_major_formatter(myFmt)

            axs[0, 1].set_ylabel('Time')
            axs[0, 1].set_xlabel('Serial')
            axs[0, 1].set_title(server_translation[n] + " ipv4" + " (Best Case)")


            # lag times for worst case scenario
            if counter > 10:
                axs[1, 0].plot(lag_serials_ipv4_worst[j], lag_list_by_node_v4_worst[j], label = j + "-ipv4", linestyle = style)
            else:
                axs[1, 0].plot(lag_serials_ipv4_worst[j], lag_list_by_node_v4_worst[j], label = j + "-ipv4")
            for tick in axs[1, 0].get_xticklabels():
                tick.set_rotation(90)
                tick.set_fontsize(5)

            axs[1, 0].set_ylabel('Lag Time (seconds)')
            axs[1, 0].set_xlabel('Serial')
            axs[1, 0].set_title(server_translation[n] + " ipv4" + " (Worst Case)")


            # lag times for best case scenario
            if counter > 10:
                axs[1, 1].plot(lag_serials_ipv4_best[j], lag_list_by_node_v4_best[j], label = j + "-ipv4", linestyle = style)
            else:
                axs[1, 1].plot(lag_serials_ipv4_best[j], lag_list_by_node_v4_best[j], label = j + "-ipv4")
            for tick in axs[1, 1].get_xticklabels():
                tick.set_rotation(90)
                tick.set_fontsize(5)


            axs[1, 1].set_ylabel('Lag Time (seconds)')
            axs[1, 1].set_xlabel('Serial')
            axs[1, 1].set_title(server_translation[n] + " ipv4" + " (Best Case)")
            # axs.set_xticks(5) #!!!!!!!
            

        # axs[1, 0].get_shared_y_axes().join(axs[1, 0], axs[1, 1]) # joins the bottom two's axes
        plt.tight_layout()
        plt.legend(bbox_to_anchor=(-1.68, 0.78))
        # plt.locator_params(axis='x', nbins=5)
        plt.show()
        


        fig, axs = plt.subplots(2, 2)
        counter = 0
        for j in nodes:
            style = 'dashdot'
            temp_x = []
            for k in serials_ipv6_worst[j]: # bug?
                temp_x.append(int(k))
            temp_x.sort()

            if len(temp_x) > 0 and temp_x[-1] == 2022022500: # NOTE: debugging only
                print("ooooooooooof")

            serials_ipv6_worst[j] = []
            for k in temp_x:
                serials_ipv6_worst[j].append(str(k))
            

            # time_list_servers have the times
            # create time stamps from seconds and add it to new array, which will be fed in to replace just seconds
            worst_times = seconds_to_timestamps(time_list_by_node_v6_worst[j])
            counter += 1
            
            if counter > 10:
                axs[0, 0].plot(serials_ipv6_worst[j], worst_times, label = j + "-ipv6", linestyle = style)
            else:
                axs[0, 0].plot(serials_ipv6_worst[j], worst_times, label = j + "-ipv6")
            
            for tick in axs[0, 0].get_xticklabels():
                tick.set_rotation(90)
                tick.set_fontsize(5)

            myFmt = mdates.DateFormatter('%H:%M:%S')
            axs[0, 0].yaxis.set_major_formatter(myFmt)

            axs[0, 0].set_ylabel('Time')
            axs[0, 0].set_xlabel('Serial')
            axs[0, 0].set_title(server_translation[n] + " ipv6" + " (Worst Case)")
            # ax1.tight_layout()

            
            best_times = seconds_to_timestamps(time_list_by_node_v6_best[j])

            # ax2.plot(serials_ipv6_best[j], best_times, label = j + "-ipv6")
            if counter > 10:
                axs[0, 1].plot(serials_ipv6_worst[j], best_times, label = j + "-ipv6", linestyle = style)
            else:
                axs[0, 1].plot(serials_ipv6_worst[j], best_times, label = j + "-ipv6")
            for tick in axs[0, 1].get_xticklabels():
                tick.set_rotation(90)
                tick.set_fontsize(5)

            myFmt = mdates.DateFormatter('%H:%M:%S')
            axs[0, 1].yaxis.set_major_formatter(myFmt)

            axs[0, 1].set_ylabel('Time')
            axs[0, 1].set_xlabel('Serial')
            axs[0, 1].set_title(server_translation[n] + " ipv6" + " (Best Case)")


            # lag times for worst case scenario
            if counter > 10:
                axs[1, 0].plot(lag_serials_ipv6_worst[j], lag_list_by_node_v6_worst[j], label = j + "-ipv6", linestyle = style)
            else:
                axs[1, 0].plot(lag_serials_ipv6_worst[j], lag_list_by_node_v6_worst[j], label = j + "-ipv6")
            for tick in axs[1, 0].get_xticklabels():
                tick.set_rotation(90)
                tick.set_fontsize(5)

            axs[1, 0].set_ylabel('Lag Time (seconds)')
            axs[1, 0].set_xlabel('Serial')
            axs[1, 0].set_title(server_translation[n] + " ipv6" + " (Worst Case)")


            # lag times for best case scenario
            if counter > 10:
                axs[1, 1].plot(lag_serials_ipv6_best[j], lag_list_by_node_v6_best[j], label = j + "-ipv6", linestyle = style)
            else:
                axs[1, 1].plot(lag_serials_ipv6_best[j], lag_list_by_node_v6_best[j], label = j + "-ipv6")
            for tick in axs[1, 1].get_xticklabels():
                tick.set_rotation(90)
                tick.set_fontsize(5)


            axs[1, 1].set_ylabel('Lag Time (seconds)')
            axs[1, 1].set_xlabel('Serial')
            axs[1, 1].set_title(server_translation[n] + " ipv6" + " (Best Case)")
            

        plt.tight_layout()
        plt.legend(bbox_to_anchor=(-1.68, 0.78))
        plt.show()


def graph_lag(data):
    all_deltas = {}
    all_names = {}
    all_nodes = {}
    all_servers = {}
    all_ipv = {}
    all_serials = {}

    for key in data:
        datapoints = data[key] # key is serial

        names = []
        time_stamps = []
        deltas = []
        nodes = []
        servers = []
        ipvs = []
        serials = []

        # add percentiles by ipv
        ipv4_deltas = []
        ipv6_deltas = []

        

        first_in_order_seconds = datapoints[0].seconds # we need to get first of each serial

        for val in datapoints:
            
            name = val.node + "-" + val.server + "-" + str(val.ipv)
            names.append(name)
            time_stamps.append(val.timestamp.get_time())
            servers.append(val.server)
            ipvs.append(val.ipv)
            serials.append(key)
            nodes.append(val.node)
            # deltas.append(val[1])

            if val.ipv == 4:
                ipv4_deltas.append(val.seconds - first_in_order_seconds)
            elif val.ipv == 6:
                ipv6_deltas.append(val.seconds - first_in_order_seconds)

            deltas.append(val.seconds - first_in_order_seconds)
        
        all_deltas[key] = deltas
        all_names[key] = names
        all_nodes[key] = nodes
        all_servers[key] = servers
        all_ipv[key] = ipvs
        all_serials[key] = serials


    return all_deltas, all_names, all_nodes, all_servers, all_ipv, all_serials


def subtract_array(array_a, array_b):
    temp = []
    for i in range(len(array_b)):
        temp.append(array_b[i] - array_a[i])

    return temp


def create_bar_chart(serials, overall_a, overall_b, overall_c, overall_one, overall_two, overall_three, overall_four, title):
    N = len(serials)
    ind = np.arange(N) 

    width = 0.35

    array_40 = subtract_array(overall_a, overall_b)
    array_50 = subtract_array(overall_b, overall_c)
    array_60 = subtract_array(overall_c, overall_one)
    array_300 = subtract_array(overall_one, overall_two)
    array_3600 = subtract_array(overall_two, overall_three)
    array_18000 = subtract_array(overall_three, overall_four)

    plt.bar(ind, overall_a, width, label='Update within 30 seconds')
    plt.bar(ind, array_40, width, label='Update within 40 seconds', bottom=np.array(overall_a))
    plt.bar(ind, array_50, width, label='Update within 50 seconds', bottom=np.array(overall_a)+np.array(array_40))
    plt.bar(ind, array_60, width, label='Update within 60 seconds', bottom=np.array(overall_a)+np.array(array_40)+np.array(array_50))
    plt.bar(ind, array_300, width,label='Update within 300 seconds', bottom=np.array(overall_a)+np.array(array_40)+np.array(array_50)+np.array(array_60))
    plt.bar(ind, array_3600, width, label='Update within 3600 seconds', bottom=np.array(overall_a)+np.array(array_40)+np.array(array_50)+np.array(array_60)+np.array(array_300))
    plt.bar(ind, array_18000, width, label='Update within 3600 seconds', bottom=np.array(overall_a)+np.array(array_40)+np.array(array_50)+np.array(array_60)+np.array(array_300)+np.array(array_3600))
    

    plt.ylabel('Fraction')
    plt.title(title)

    plt.xticks(ind, serials)
    plt.xticks(rotation = 90)
    plt.tight_layout()
    plt.legend(loc='lower right')
    plt.show()


# can be used to get specific info from a node
def spread_by_node(data, node, serials):
    less_than_a = {}
    less_than_b = {}
    less_than_c = {}
    less_than_first = {}
    less_than_second = {}
    less_than_third = {}
    less_than_fourth = {}

    points_for_node = {}

    overall_results_30 = [] # a
    overall_results_40 = [] # b
    overall_results_50 = [] # c
    overall_results_60 = [] # 1
    overall_results_300 = [] # 2
    overall_results_3600 = [] # 3
    overall_results_18000 = [] # 4

    print("----", node, "----")

    for s in serials:
        less_than_a[s] = []
        less_than_b[s] = []
        less_than_c[s] = []
        less_than_first[s] = []
        less_than_second[s] = []
        less_than_third[s] = []
        less_than_fourth[s] = []
        points_for_node[s] = []

        deltas = []
        first_in_order_seconds = data[s][0].seconds

        for x in data[s]:
            deltas.append(x.seconds - first_in_order_seconds)
            x.delta = x.seconds - first_in_order_seconds

        # now we need to start with the stats (n with delta < 60 for example)
        for x in data[s]:
            if x.node == node:
                points_for_node[s].append(x)
            if x.delta <= 30 and x.node == node:
                less_than_a[s].append(x)
            if x.delta <= 40 and x.node == node:
                less_than_b[s].append(x)
            if x.delta <= 50 and x.node == node:
                less_than_c[s].append(x)
            if x.delta <= 60 and x.node == node:
                less_than_first[s].append(x)
            if x.delta <= 300 and x.node == node:
                less_than_second[s].append(x)
            if x.delta <= 3600 and x.node == node:
                less_than_third[s].append(x)
            if x.delta <= 18000 and x.node == node:
                less_than_fourth[s].append(x)

        
        print("serial:", s)
        print("less than 60:", len(less_than_first[s]), "/", len(points_for_node[s]), len(less_than_first[s]) / len(points_for_node[s]))
        print("less than 500:", len(less_than_second[s]), "/", len(points_for_node[s]), len(less_than_second[s]) / len(points_for_node[s]))
        print("less than 3600:", len(less_than_third[s]), "/", len(points_for_node[s]), len(less_than_third[s]) / len(points_for_node[s]))
        print()

        overall_results_30.append(len(less_than_a[s]) / len(points_for_node[s]))
        overall_results_40.append(len(less_than_b[s]) / len(points_for_node[s]))
        overall_results_50.append(len(less_than_c[s]) / len(points_for_node[s]))
        overall_results_60.append(len(less_than_first[s]) / len(points_for_node[s]))
        overall_results_300.append(len(less_than_second[s]) / len(points_for_node[s]))
        overall_results_3600.append(len(less_than_third[s]) / len(points_for_node[s]))
        overall_results_3600.append(len(less_than_fourth[s]) / len(points_for_node[s]))

    create_bar_chart(serials, overall_results_30, overall_results_40, overall_results_50,
     overall_results_60, overall_results_300, overall_results_3600, overall_results_18000, node)      


def spread_by_server(data, server, serials):
    less_than_a = {}
    less_than_b = {}
    less_than_c = {}
    less_than_first = {}
    less_than_second = {}
    less_than_third = {}
    less_than_fourth = {}

    points_for_server = {}

    overall_results_30 = [] # a
    overall_results_40 = [] # b
    overall_results_50 = [] # c
    overall_results_60 = [] # 1
    overall_results_300 = [] # 2
    overall_results_3600 = [] # 3
    overall_results_18000 = [] # 4

    print("----", server_translation[server], "----")

    for s in serials:
        less_than_a[s] = []
        less_than_b[s] = []
        less_than_c[s] = []
        less_than_first[s] = []
        less_than_second[s] = []
        less_than_third[s] = []
        less_than_fourth[s] = []
        points_for_server[s] = []

        deltas = []
        first_in_order_seconds = data[s][0].seconds

        for x in data[s]:
            deltas.append(x.seconds - first_in_order_seconds)
            x.delta = x.seconds - first_in_order_seconds

        # now we need to start with the stats (n with delta < 60 for example)
        for x in data[s]:
            if x.server == server:
                points_for_server[s].append(x)
            if x.delta <= 30 and x.server == server:
                less_than_a[s].append(x)
            if x.delta <= 40 and x.server == server:
                less_than_b[s].append(x)
            if x.delta <= 50 and x.server == server:
                less_than_c[s].append(x)
            if x.delta <= 60 and x.server == server:
                less_than_first[s].append(x)
            if x.delta <= 300 and x.server == server:
                less_than_second[s].append(x)
            if x.delta <= 3600 and x.server == server:
                less_than_third[s].append(x)
            if x.delta <= 18000 and x.server == server:
                less_than_fourth[s].append(x)

        
        print("serial:", s)
        print("less than 60:", len(less_than_first[s]), "/", len(points_for_server[s]), len(less_than_first[s]) / len(points_for_server[s]))
        print("less than 500:", len(less_than_second[s]), "/", len(points_for_server[s]), len(less_than_second[s]) / len(points_for_server[s]))
        print("less than 3600:", len(less_than_third[s]), "/", len(points_for_server[s]), len(less_than_third[s]) / len(points_for_server[s]))
        print()

        overall_results_30.append(len(less_than_a[s]) / len(points_for_server[s]))
        overall_results_40.append(len(less_than_b[s]) / len(points_for_server[s]))
        overall_results_50.append(len(less_than_c[s]) / len(points_for_server[s]))
        overall_results_60.append(len(less_than_first[s]) / len(points_for_server[s]))
        overall_results_300.append(len(less_than_second[s]) / len(points_for_server[s]))
        overall_results_3600.append(len(less_than_third[s]) / len(points_for_server[s]))
        overall_results_18000.append(len(less_than_fourth[s]) / len(points_for_server[s]))

    title = "Server: " + server_translation[server]

    create_bar_chart(serials, overall_results_30, overall_results_40, overall_results_50,
     overall_results_60, overall_results_300, overall_results_3600, overall_results_18000, title)      


def spread_analysis(data, nodes):
    start = 2022022500
    stop = 2022030400

    print("START OF ANALYSIS")
    print("FROM:", start, "TO:", stop)

    all_serials = list(data.keys())

    serials = []
    for i in all_serials:
        if int(i) >= start and int(i) <= stop:
            serials.append(i)

    less_than_first = {}
    less_than_second = {}
    less_than_third = {}
    less_than_a = {}
    less_than_b = {}
    less_than_c = {}


    overall_results_30 = [] # a
    overall_results_40 = [] # b
    overall_results_50 = [] # c
    overall_results_60 = []
    overall_results_300 = []
    overall_results_3600 = []

    for s in serials:
        less_than_a[s] = []
        less_than_b[s] = []
        less_than_c[s] = []
        less_than_first[s] = []
        less_than_second[s] = []
        less_than_third[s] = []

        deltas = []
        first_in_order_seconds = data[s][0].seconds

        for x in data[s]:
            deltas.append(x.seconds - first_in_order_seconds)
            x.delta = x.seconds - first_in_order_seconds

        # now we need to start with the stats (n with delta < 60 for example)
        for x in data[s]:
            if x.delta <= 30:
                less_than_a[s].append(x)
            if x.delta <= 40:
                less_than_b[s].append(x)
            if x.delta <= 50:
                less_than_c[s].append(x)
            if x.delta <= 60:
                less_than_first[s].append(x)
            if x.delta <= 300:
                less_than_second[s].append(x)
            if x.delta <= 3600:
                less_than_third[s].append(x)

        # this is overall
        print("---------------")
        print("serial:", s)
        print("less than 60:", len(less_than_first[s]), "/", len(data[s]), len(less_than_first[s]) / len(data[s]))
        print("less than 500:", len(less_than_second[s]), "/", len(data[s]), len(less_than_second[s]) / len(data[s]))
        print("less than 3600:", len(less_than_third[s]), "/", len(data[s]), len(less_than_third[s]) / len(data[s]))
        print()

        overall_results_30.append(len(less_than_a[s]) / len(data[s]))
        overall_results_40.append(len(less_than_b[s]) / len(data[s]))
        overall_results_50.append(len(less_than_c[s]) / len(data[s]))
        overall_results_60.append(len(less_than_first[s]) / len(data[s]))
        overall_results_300.append(len(less_than_second[s]) / len(data[s]))
        overall_results_3600.append(len(less_than_third[s]) / len(data[s]))

    # graph results in matplotlib; needs serials, overalls
    create_bar_chart(serials, overall_results_30, overall_results_40, overall_results_50,
     overall_results_60, overall_results_300, overall_results_3600, "Overall")

    for n in nodes:
        spread_by_node(data, n, serials)


def spread_analysis_servers(data, servers):
    start = 2022022500
    stop = 2022030400

    print("START OF ANALYSIS")
    print("FROM:", start, "TO:", stop)

    all_serials = list(data.keys())

    serials = []
    for i in all_serials:
        if int(i) >= start and int(i) <= stop:
            serials.append(i)

    less_than_first = {}
    less_than_second = {}
    less_than_third = {}
    less_than_fourth = {}
    less_than_a = {}
    less_than_b = {}
    less_than_c = {}


    overall_results_30 = [] # a
    overall_results_40 = [] # b
    overall_results_50 = [] # c
    overall_results_60 = []
    overall_results_300 = []
    overall_results_3600 = []
    overall_results_18000 = []

    for s in serials:
        less_than_a[s] = []
        less_than_b[s] = []
        less_than_c[s] = []
        less_than_first[s] = []
        less_than_second[s] = []
        less_than_third[s] = []
        less_than_fourth[s] = []

        deltas = []
        first_in_order_seconds = data[s][0].seconds

        for x in data[s]:
            deltas.append(x.seconds - first_in_order_seconds)
            x.delta = x.seconds - first_in_order_seconds

        # now we need to start with the stats (n with delta < 60 for example)
        for x in data[s]:
            if x.delta <= 30:
                less_than_a[s].append(x)
            if x.delta <= 40:
                less_than_b[s].append(x)
            if x.delta <= 50:
                less_than_c[s].append(x)
            if x.delta <= 60:
                less_than_first[s].append(x)
            if x.delta <= 300:
                less_than_second[s].append(x)
            if x.delta <= 3600:
                less_than_third[s].append(x)
            if x.delta <= 18000:
                less_than_fourth[s].append(x)


        overall_results_30.append(len(less_than_a[s]) / len(data[s]))
        overall_results_40.append(len(less_than_b[s]) / len(data[s]))
        overall_results_50.append(len(less_than_c[s]) / len(data[s]))
        overall_results_60.append(len(less_than_first[s]) / len(data[s]))
        overall_results_300.append(len(less_than_second[s]) / len(data[s]))
        overall_results_3600.append(len(less_than_third[s]) / len(data[s]))
        overall_results_18000.append(len(less_than_fourth[s]) / len(data[s]))

    # graph results in matplotlib; needs serials, overalls
    create_bar_chart(serials, overall_results_30, overall_results_40, overall_results_50,
     overall_results_60, overall_results_300, overall_results_3600, overall_results_18000, "Overall")

    for s in servers:
        spread_by_server(data, s, serials)


def process(serial_num):
    # we don't really need a neat n x m table
    # focus on flexibility of data points to use in spreads

    # get the rows by serial number (dictionary set up)
    organized_worst = organize_data_worst(serial_num)
    organized_best = organize_data_best(serial_num)

    sorted_worst = sort_data(organized_worst)
    sorted_best = sort_data(organized_best)

    nodes, data_by_nodes_worst, servers, data_by_servers_worst = pre_print_spread(sorted_worst)
    nodes, data_by_nodes_best, servers, data_by_servers_best = pre_print_spread(sorted_best)

    # user sorted_worst/best for the model
    spread_analysis_servers(sorted_worst, servers)
    spread_analysis(sorted_worst, nodes)
    

    all_deltas, all_names, all_nodes, all_servers, all_ipv, all_serials = graph_lag(sorted_worst)
    all_deltas_best, all_names_best, all_nodes_best, all_servers_best, all_ipv_best, all_serials_best = graph_lag(sorted_best)

    data_deltas = (all_deltas, all_deltas_best)
    data_names = (all_names, all_names_best)
    data_nodes = (all_nodes, all_nodes_best)
    data_servers = (all_servers, all_servers_best)
    data_ipvs = (all_ipv, all_ipv_best)
    data_serials = (all_serials, all_serials_best)

    # graph by server instead of node
    create_graphs_by_server(nodes, data_by_nodes_worst, data_by_nodes_best, servers, data_deltas, data_names, 
    data_nodes, data_servers, data_ipvs, data_serials, data_by_servers_worst, data_by_servers_best)

    # create_graphs(nodes, data_by_nodes_worst, data_by_nodes_best, servers, data_deltas, data_names, 
    # data_nodes, data_servers, data_ipvs, data_serials)
    
    
def main(argv):
    serial_num = 2022022500
    if len(argv) > 0:
        serial_num = int(argv[0])
    process(serial_num)


if __name__ == "__main__":
    main(sys.argv[1:])