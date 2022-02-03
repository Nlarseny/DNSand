import sys
import glob
import subprocess
import os


def get_filenames():
    # Get the current working directory
    cwd = os.getcwd()
    file_list = glob.glob("*.txt") # Include slash or it will search in the wrong directory!!

    return file_list


def parse_file():
    text_files = get_filenames()

    for f in text_files:
        new_file = os.getcwd() + "/test/edit_" + str(f)
        print(new_file)
        current_file = os.getcwd() + "/" + f
        # os.system(["sed", "/TIMED/d", current_file, ">", new_file])
        args = "sed /TIMED/d " + current_file + " > " + new_file
        # print(args)
        os.system(args)

        args = "sed /TIMED/d " + current_file + " > " + new_file
        # print(args)
        os.system(args)

        args = "sed 1d " + new_file
        # print(args)
        os.system(args)

    

def main(argv):
    parse_file()



if __name__ == "__main__":
    main(sys.argv[1:])

    # root changes seem to consistently be between 22:00 and 23:00, as well as between 10:00 and 11:00 (MST)
