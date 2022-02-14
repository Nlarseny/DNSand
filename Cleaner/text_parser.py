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
                   recursive = True)

    return all_files


def parse_file():
    text_files = get_filenames()

    for f in text_files:
        file = open(f, "r")
        lines = file.readlines()
        file.close()

        file = open(f, "w")
        for line in lines:
            if "TIMED OUT" not in line:
                file.write(line)

    file.close()
        

    

def main(argv):
    parse_file()



if __name__ == "__main__":
    main(sys.argv[1:])

    # root changes seem to consistently be between 22:00 and 23:00, as well as between 10:00 and 11:00 (MST)
