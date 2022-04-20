import sys
import glob


# Returns list with all files from all the folders
def get_filenames():
    all_files = glob.glob('./**/*.txt', 
                   recursive = True)

    return all_files


# check if string is in the file
def check_if_string_in_file(file_name, string_to_search):
    iter = 0
    with open(file_name, 'r') as read_obj:
        for line in read_obj:
            if string_to_search in line:
                iter += 1
    return iter


# prints the table of results
def create_table():
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