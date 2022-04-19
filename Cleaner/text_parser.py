from asyncore import write
import sys
import glob
import subprocess
import os


# def get_filenames():
#     # Get the current working directory
#     cwd = os.getcwd()
#     file_list = glob.glob("*.txt") # Include slash or it will search in the wrong directory!!

#     return file_list


def get_filenames():
    #file_list = glob.glob("./1test/*.txt") # Include slash or it will search in the wrong directory

    all_files = glob.glob('./**/**/*.txt', 
                   recursive = False)

    return all_files


def parse_file(baseline):
    text_files = get_filenames()

    for f in text_files:
        no_doubles = {}

        file = open(f, "r")
        lines = file.readlines()
        file.close()

        serial_times = {}
        for line in lines:
            if "TIMED OUT" not in line and "None" not in line:
                serial = line.split()[1]
                if int(serial) not in serial_times:
                    serial_times[int(serial)] = []
                
                flag = 0

                time = line.split()[0]
                serial_times[int(serial)].append(int(time.split(':')[0])) # store the hour

        # file = open(f, "w")
        lines_to_write = {}
        with open(f, 'w') as write_obj:
            for line in lines:
                if "TIMED OUT" not in line and "None" not in line:
                    serial = line.split()[1]
                    

                    if serial != None and int(serial) >= baseline: # gets worst case
                        
                        if len(serial_times[int(serial)]) > 1 and serial_times[int(serial)][0] > serial_times[int(serial)][-1]:
                            time = line.split()[0]
                            hour = int(time.split(':')[0]) + 24 # fix: only need to do this if last is less than first
                            lines_to_write[serial] = str(hour) + ":" + time.split(':')[1] + ":" + time.split(':')[2] + " " + line.split()[1] + "\n"
                        else:
                            lines_to_write[serial] = line


            # have a latest serial var to see if we need to add 24 hours to the time stamp
            # add in a scrubber to subtract anything over 24 in tabler.py

            for key in lines_to_write:
                write_obj.write(lines_to_write[key])

        # NOTE: need to get the worst case bouncers
        # maybe make an array to be written, update no_doubles to have the latest time?

    # file.close()
        

    

def main(argv):
    baseline = 2022022500
    parse_file(baseline)



if __name__ == "__main__":
    main(sys.argv[1:])

    # root changes seem to consistently be between 22:00 and 23:00, as well as between 10:00 and 11:00 (MST)
