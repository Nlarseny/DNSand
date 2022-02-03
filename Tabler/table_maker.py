import sys
import glob
import subprocess
import os
import csv
from csv import writer


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


def deltaTimeStamp(time_a, time_b):
    total_a_seconds = time_a.to_seconds()
    total_b_seconds = time_b.to_seconds()

    # z = y - x
    return total_b_seconds - total_a_seconds


def get_filenames():
    file_list = glob.glob("./test/*.txt") # Include slash or it will search in the wrong directory

    # print(file_list)

    return file_list


def make_rows():
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
        
        rows.append(row)

    return rows
            
            
def get_spread(rows):
    # need a winner by row

    # this converts the rows to rows of timestamp objects
    for i in range(0, len(rows)):
        for j in range (1, len(rows[i])):
            result = rows[i][j].split(":")
            print(rows[i][j])
            final = TimeStamps(int(result[0]), int(result[1]), float(result[2]))
            rows[i][j] = final
        for j in range (1, len(rows[i])):
            x=0
        


    


def create_table(file_list):
    # list_of_headers = ["SERIALS", "verisign(a)", "USC", "CogentCom",
    # "UM", "NASA", "ISC", "US DD", "Army", "Netnod", "verisign(j)", "RIPE", "ICANN", "WIDE"]

    list_of_headers = ["SERIALS"]
    files = get_filenames()
    for file in files:
        temp = file.split('.')
        file_name = temp[1]
        list_of_headers.append(file_name)


    # Open file in append mode
    with open('practice.csv', 'a+', newline='') as write_obj:
        csv_writer = writer(write_obj)

        # Add headers
        csv_writer.writerow(list_of_headers)

        rows = make_rows()
        for row in rows:
            csv_writer.writerow(row)

        # get the spread for each row
        get_spread(rows)
    

def main(argv):
    create_table([])



if __name__ == "__main__":
    main(sys.argv[1:])

    # root changes seem to consistently be between 22:00 and 23:00, as well as between 10:00 and 11:00 (MST)
