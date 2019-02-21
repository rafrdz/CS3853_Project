#!/usr/bin/env python3

import sys
import os

# CS3853 Computer Architecture Project
# Milestone 1
# Team 6: Rafael Rodriguez,


def get_all_files(directory):
    file_list = []
    for file in os.listdir(directory):
        if file.endswith('.trc'):
            file_list.append(file)
    return file_list


def parse_files(files_list):
    for file in files_list:
        try:
            with open(sys.argv[1] + '/' + file, 'r') as f:
                line_count = 0
                for line in f:
                    line_count += 1
                print('Number of lines in ' + file + ' is: ' + str(line_count))
        except FileNotFoundError:
            print('Error: File was not found')
            print('Please check that the file exists and try again')
            sys.exit(2)


# Verify the number of arguments
if len(sys.argv) != 3:
    print('Error: Not enough arguments')
    print('Usage: [python file] [data directory] [output directory]')
    sys.exit(1)

# Create the output directory if it does not exist
if not os.path.exists(sys.argv[2]):
    os.mkdir(sys.argv[2])

# Get all files in the data directory and send files to parsing function
parse_files(get_all_files(sys.argv[1]))
