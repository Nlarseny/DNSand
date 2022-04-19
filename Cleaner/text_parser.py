import sys
import glob


# Get all filenames in the folders
def get_filenames():
    all_files = glob.glob('./**/**/*.txt', 
                   recursive = False)

    return all_files


# parses the files line by line to clean out the file
# the argument is the baseline, or in otherwords the earliest you want the serial to be
def parse_file(baseline):
    text_files = get_filenames()

    for f in text_files:
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

        lines_to_write = {}
        with open(f, 'w') as write_obj:
            for line in lines:
                if "TIMED OUT" not in line and "None" not in line:
                    serial = line.split()[1]
                    

                    if serial != None and int(serial) >= baseline: # gets worst case
                        
                        if len(serial_times[int(serial)]) > 1 and serial_times[int(serial)][0] > serial_times[int(serial)][-1]:
                            time = line.split()[0]
                            hour = int(time.split(':')[0]) + 24
                            lines_to_write[serial] = str(hour) + ":" + time.split(':')[1] + ":" + time.split(':')[2] + " " + line.split()[1] + "\n"
                        else:
                            lines_to_write[serial] = line

            for key in lines_to_write:
                write_obj.write(lines_to_write[key])
        

# Worst case version of the cleaner
# the argument is the baseline, or in otherwords the earliest you want the serial to be
def main(argv):
    baseline = 2022022500
    parse_file(baseline)


if __name__ == "__main__":
    main(sys.argv[1:])