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


    x = [str(x) for x in serials]


    return nodes, data_by_nodes, servers # serials


    # size and color:
    # sizes = np.random.uniform(15, 80, len(x))
    # colors = np.random.uniform(15, 80, len(x))

    # plot
    #fig, ax = plt.subplots()

    # print(type(x[0]))
    # print(type(ipv4_mean[0]))

    # plt.scatter(x, ipv4_mean, label="ipv4_mean", s=100, alpha = 0.5)
    
    # plt.scatter(x, ipv6_mean, label="ipv6_mean", marker="s", s=100, alpha = 0.5)
    # plt.scatter(x, ipv4_median, label="ipv4_median", s=100, alpha = 0.5)
    # plt.scatter(x, ipv6_median, label="ipv6_median", marker="s", s=100, alpha = 0.5)
    # plt.scatter(x, ipv4_75, label="ipv4_75", s=100, alpha = 0.5)
    # plt.scatter(x, ipv6_75, label="ipv6_75", marker="s", s=100, alpha = 0.5)
    # plt.scatter(x, ipv4_90, label="ipv4_90", s=100, alpha = 0.5)
    # plt.scatter(x, ipv6_90, label="ipv6_90", marker="s", s=100, alpha = 0.5)
    # plt.scatter(x, ipv4_max, label="ipv4_max", s=100, alpha = 0.5)
    # plt.scatter(x, ipv6_max, label="ipv6_max", marker="s", s=100, alpha = 0.5)

    # plt.tight_layout()
    # plt.ylabel('Lag Time (Seconds)')
    # plt.xlabel('Serial')
    # plt.xticks(rotation=90)
    # plt.legend()
    # plt.show()
    # plt.close()


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
        plt.legend(bbox_to_anchor=(-1.68, 0.75))
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
        plt.legend(bbox_to_anchor=(-1.68, 0.75))
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



def process(serial_num):
    # we don't really need a neat n x m table
    # focus on flexibility of data points to use in spreads

    # get the rows by serial number (dictionary set up)
    organized_worst = organize_data_worst(serial_num)
    organized_best = organize_data_best(serial_num)

    sorted_worst = sort_data(organized_worst)
    sorted_best = sort_data(organized_best)

    nodes, data_by_nodes_worst, servers = pre_print_spread(sorted_worst)
    nodes, data_by_nodes_best, servers = pre_print_spread(sorted_best)

    all_deltas, all_names, all_nodes, all_servers, all_ipv, all_serials = graph_lag(sorted_worst)
    all_deltas_best, all_names_best, all_nodes_best, all_servers_best, all_ipv_best, all_serials_best = graph_lag(sorted_best)

    data_deltas = (all_deltas, all_deltas_best)
    data_names = (all_names, all_names_best)
    data_nodes = (all_nodes, all_nodes_best)
    data_servers = (all_servers, all_servers_best)
    data_ipvs = (all_ipv, all_ipv_best)
    data_serials = (all_serials, all_serials_best)

    create_graphs(nodes, data_by_nodes_worst, data_by_nodes_best, servers, data_deltas, data_names, 
    data_nodes, data_servers, data_ipvs, data_serials)
    
    
def main(argv):
    serial_num = 2022022500
    if len(argv) > 0:
        serial_num = int(argv[0])
    process(serial_num)


if __name__ == "__main__":
    main(sys.argv[1:])