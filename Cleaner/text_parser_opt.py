import sys
import glob


def get_filenames():
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

        lines_to_write = {}
        with open(f, 'w') as write_obj:
            for line in lines:
                if "TIMED OUT" not in line and "None" not in line:
                    serial = line.split()[1]
                    if serial != None and int(serial) >= baseline and serial not in lines_to_write: # gets best case
                        lines_to_write[serial] = line

            for key in lines_to_write:
                write_obj.write(lines_to_write[key])
        

def main(argv):
    baseline = 2022022500
    parse_file(baseline)


if __name__ == "__main__":
    main(sys.argv[1:])
