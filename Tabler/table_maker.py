import sys
import glob
import subprocess
import os
import csv
from csv import writer


def get_filenames():
    file_list = glob.glob("./test/*.txt") # Include slash or it will search in the wrong directory

    # print(file_list)

    return file_list


def make_row():
    files = get_filenames()

    rows = []
    flag = 0
    row_iter = 0
    for file in files:
        with open(file) as f:
            lines = f.readlines()
            
            tupled = []
            for line in lines:
                tupled.append(line.split())
                
            row = []
            for tup in tupled: 
                if flag == 0:
                    row.append(tup[1])
                    flag = 1
                row.append(tup[0])
            
            


def create_table(file_list):
    list_of_headers = ["", "verisign(a)", "USC", "CogentCom",
    "UM", "NASA", "ISC", "US DD", "Army", "Netnod", "verisign(j)", "RIPE", "ICANN", "WIDE"]

    make_row()

    # Open file in append mode
    with open('practice.csv', 'a+', newline='') as write_obj:
        csv_writer = writer(write_obj)

        # Add headers
        csv_writer.writerow(list_of_headers)

    # with open("practice.csv", 'a') as csv_file:
    #     first = str(datetime.now().time()) + " " + str(current_serial) + "\n"
    #     csv_file.write(first)
    

def main(argv):
    create_table([])



if __name__ == "__main__":
    main(sys.argv[1:])

    # root changes seem to consistently be between 22:00 and 23:00, as well as between 10:00 and 11:00 (MST)
