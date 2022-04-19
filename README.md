# DNSand

This repository consists of 3 main parts: Tabler, Cleaner, and Defunct


Cleaner:
This folder serves as a way to clean raw data from the Ark nodes. One simply needs to load the folders of data into the cleaner_file directory and then run either text_parser_opt.py or text_parser.py to get the data cleaned. Those loaded files will then be edited by the program. The program text_parser_opt.py gets the best case scenarios for each serial number update. The program text_parse.py simply gets the worst case scenaio for each update. 

The file called timeout_counter.py simply totals and prints how many TIMEOUT lines there were by node and root server.


Tabler:
This folder contains everything needed to parse cleaned data. It works on a similar principle as the cleaner program does. Once the data has been cleaned by by the selected cleaner file, load it into the correct directory (self explanatory on which goes where). Once the files are loaded you can run tabler.py to organize the data and present it. 
There are several options for presenting. See the comments in the code to see which functions to uncomment to get desired graphs and then run the program.