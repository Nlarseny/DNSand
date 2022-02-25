import sys
import glob
from csv import writer
import numpy as np
import copy








def get_filenames():
    #file_list = glob.glob("./1test/*.txt") # Include slash or it will search in the wrong directory

    all_files = glob.glob('./**/*.txt', 
                   recursive = True)

    return all_files


def check_if_string_in_file(file_name, string_to_search):
    iter = 0
    with open(file_name, 'r') as read_obj:
        for line in read_obj:
            if string_to_search in line:
                iter += 1
    return iter

def create_table(serial_num):
    # list_of_headers = ["SERIALS", "verisign(a)", "USC", "CogentCom",
    # "UM", "NASA", "ISC", "US DD", "Army", "Netnod", "verisign(j)", "RIPE", "ICANN", "WIDE"]

    list_of_headers = {}
    files = get_filenames()
    for file in files:
        temp = file.split('.')
        file_name = temp[1]
        list_of_headers[file_name] = check_if_string_in_file(file, "TIMED OUT")


    print(list_of_headers)




    



    

def main(argv):
    serial_num = 0
    if len(argv) > 0:
        serial_num = int(argv[0])

    create_table(serial_num)



if __name__ == "__main__":
    main(sys.argv[1:])

    # root changes seem to consistently be between 22:00 and 23:00, as well as between 10:00 and 11:00 (MST)
