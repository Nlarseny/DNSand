import sys
import glob
from csv import writer
import numpy as np
import copy



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


def make_rows(serial_num):
    files = get_filenames()

    # do while there are lines, all files should have the same number of lines after being cleaned
    line_num = 0
    with open(files[0]) as f:
        lines = f.readlines()
        line_num = len(lines)

    rows = []
    for i in range(0, line_num):
        # get ith element for each file
        row = []
        # get serial for the row
        with open(files[0]) as f:
            lines = f.readlines()
            temp = lines[i].split()
            row.append(temp[1])

        for file in files:
            with open(file) as f:
                lines = f.readlines()
                
                tupled = []
                for line in lines:
                    tupled.append(line.split())
                row.append(tupled[i][0])
        
        # where we can sync up the serials
        if int(row[0]) >= serial_num:
            rows.append(row)

    return rows
            

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


    


         
def get_spread(rows):
    # need a winner by row
    files = get_filenames()

    all_vals = []
    # smallest_list = []
    # this converts the rows to rows of timestamp objects
    for i in range(0, len(rows)):
        smallest_list = []

        # NOTE: this is where we can create the objects of the data points
        for j in range (1, len(rows[i])):
            result = rows[i][j].split(":")
            #print(rows[i][j])
            
            final = TimeStamps(int(result[0]), int(result[1]), float(result[2]))
            rows[i][j] = (final, files[j - 1])

            # smallest_list.append((final.to_seconds(), j, final))

            # need to get node, server, and ipv
            node, server, ipv = get_file_parse(files[j - 1])


            data_point = DataPoint(node, server, ipv, j, final.to_seconds(), final)
            smallest_list.append(data_point)

        smallest_list.sort(key=lambda y: y.seconds)

        order_list = []
        for k in range(0, len(rows[i]) - 1):
            index_file = smallest_list[k].iter
            order_list.append((smallest_list[k].seconds, files[index_file - 1], smallest_list[k].timestamp))
            # print(order_list)

        smallest = order_list[0][2]
        smallest_val = order_list[0][0]
        smallest_iter = order_list[0][1] # tag info
        node, server, ipv = get_file_parse(smallest_iter)


        vals = []
        temp = ((smallest, smallest_iter), 0, DataPoint(node, server, ipv, -1, smallest.to_seconds(), smallest))
        vals.append(temp)
        #print(temp[0][0].get_time(), temp[1])
        #vals.append(temp)
        for j in range (0, len(rows[i]) - 1):
            if files[j] != smallest_iter:
                delta = deltaTimeStamp(smallest, rows[i][j+1][0])
                node, server, ipv = get_file_parse(files[j])
                next_temp = ((rows[i][j+1][0], files[j]), delta, DataPoint(node, server, ipv, -1, rows[i][j+1][0].to_seconds(), rows[i][j+1][0]))
                #print(next_temp[0].get_time(), ":", next_temp[1])
                vals.append(next_temp)
            else:
                next_temp = ((smallest, smallest_iter), 0)
                #print(next_temp[0].get_time(), ":", next_temp[1])
                #vals.append(next_temp)

        vals.sort(key=lambda y: y[1])

        all_vals.append(vals)

    return all_vals


def average_list(lister):
    return sum(lister) / len(lister)


def print_spread(all_vals, rows):
    # vals contains the sorted spread, now to move it to the excel sheet
    with open('practice.csv', 'a+', newline='') as write_obj:
        csv_writer = writer(write_obj)

        # Add spaces
        blanks = ["", "", ""]
        csv_writer.writerow(blanks)

        spread_header = ["Spread by Serial", "", ""]
        csv_writer.writerow(spread_header)


    counter = 0
    for vals in all_vals:
        # what if we get a list of each of the three things in vals?
        names = []
        time_stamps = []
        deltas = []

        # add percentiles by ipv
        ipv4_deltas = []
        ipv6_deltas = []

        for v in vals:
            names.append(v[0][1])
            time_stamps.append(v[0][0].get_time())
            deltas.append(v[1])

            if v[2].ipv == 4:
                ipv4_deltas.append(v[1])
            elif v[2].ipv == 6:
                ipv6_deltas.append(v[1])




        copy_deltas = copy.deepcopy(deltas)
        # add delta averages
        pad = ["", "Average", "", "25%", "50%", "75%", "90%"]
        time_stamps.extend(pad)

        pad = ["", average_list(copy_deltas)]
        deltas.extend(pad)


        


        percentiles_v4 = ["ipv4"]
        if len(ipv4_deltas) > 0:
            percentiles_v4.append(average_list(ipv4_deltas))
            percentiles_v4.append(np.percentile(ipv4_deltas, 25))
            percentiles_v4.append(np.percentile(ipv4_deltas, 50))
            percentiles_v4.append(np.percentile(ipv4_deltas, 75))
            percentiles_v4.append(np.percentile(ipv4_deltas, 90))

        percentiles_v6 = ["ipv6"]
        if len(ipv6_deltas) > 0:
            percentiles_v6.append(average_list(ipv6_deltas))
            percentiles_v6.append(np.percentile(ipv6_deltas, 25))
            percentiles_v6.append(np.percentile(ipv6_deltas, 50))
            percentiles_v6.append(np.percentile(ipv6_deltas, 75))
            percentiles_v6.append(np.percentile(ipv6_deltas, 90))

        # copy deltas has both...

        # deltas.extend(add_percentiles)
        


        names.insert(0, "Name")
        time_stamps.insert(0, "Time")
        deltas.insert(0, "Lag Time")


        first_ipv4 = None
        for i in range(len(vals)):
            if vals[i][2].ipv == 4:
                first_ipv4 = vals[i][2]
                break

        first_ipv6 = None
        for i in range(len(vals)):
            if vals[i][2].ipv == "ipv6":
                first_ipv6 = vals[i][2]
                break

        first = vals[0][2]

        first_info = ["First", first.node, first.server, first.ipv]

        first_ipv4_info = []
        if first_ipv4 != None:
            first_ipv4_info = ["First_ipv4", first_ipv4.node, first_ipv4.server, first_ipv4.ipv]
        
        first_ipv6_info = []
        if first_ipv6 != None:
            first_ipv6_info = ["First_ipv6", first_ipv6.node, first_ipv6.server, first_ipv6.ipv]


        with open('practice.csv', 'a+', newline='') as write_obj:
            serial = [rows[counter][0]]
            counter += 1

            csv_writer = writer(write_obj)

            csv_writer.writerow(serial)
            csv_writer.writerow(names)
            csv_writer.writerow(time_stamps)
            csv_writer.writerow(deltas)

            csv_writer.writerow(first_info)
            csv_writer.writerow(first_ipv4_info)
            csv_writer.writerow(first_ipv6_info)

            csv_writer.writerow(["", "Average", "25%", "50%", "75%", "90%"])
            csv_writer.writerow(percentiles_v4)
            csv_writer.writerow(percentiles_v6)

            blanks = ["", "", ""]
            csv_writer.writerow(blanks)

    # create a pad for the next one
    with open('practice.csv', 'a+', newline='') as write_obj:
        csv_writer = writer(write_obj)
        blanks = ["", "", ""]
        csv_writer.writerow(blanks)
        csv_writer.writerow(blanks)
        csv_writer.writerow(blanks)

    


def create_table(serial_num):
    # list_of_headers = ["SERIALS", "verisign(a)", "USC", "CogentCom",
    # "UM", "NASA", "ISC", "US DD", "Army", "Netnod", "verisign(j)", "RIPE", "ICANN", "WIDE"]

    list_of_headers = ["SERIALS"]
    files = get_filenames()
    for file in files:
        temp = file.split('.')
        file_name = temp[1]
        list_of_headers.append(file_name)


    # Open file in append mode
    with open('practice.csv', 'a', newline='') as write_obj:
        csv_writer = writer(write_obj)

        # Add headers
        csv_writer.writerow(list_of_headers)

        rows = make_rows(serial_num)
        for row in rows:
            csv_writer.writerow(row)

        # get the spread for each row
        all_vals = get_spread(rows)

    print_spread(all_vals, rows)
    

def main(argv):
    serial_num = 0
    if len(argv) > 0:
        serial_num = int(argv[0])
    create_table(serial_num)



if __name__ == "__main__":
    main(sys.argv[1:])

    # root changes seem to consistently be between 22:00 and 23:00, as well as between 10:00 and 11:00 (MST)
