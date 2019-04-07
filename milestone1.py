#!/usr/bin/env python3

import sys
import os
import argparse
import math
import re
import binascii

# CS3853 Computer Architecture Project
# Milestone 1
# Team 6: Rafael Rodriguez, David Brenner, James Solis


def determine_valid_file(string):
    if os.path.isfile(string):
        return string
    else:
        raise argparse.ArgumentTypeError('file ' + string + ' does not exist')


def cache_size_type(string, min=1, max=8192):
    value = int(string)
    if min <= value <= max:
        return value
    else:
        raise argparse.ArgumentTypeError('value not in range ' + str(min) + ' - ' + str(max))


def block_size_type(string, min=4, max=64):
    value = int(string)
    if min <= value <= max:
        return value
    else:
        raise argparse.ArgumentTypeError('value not in range ' + str(min) + ' - ' + str(max))


def determine_block_offset():
    return int(math.log(results.block_size, 2))


def determine_index_size():
    return int(math.log((results.cache_size * pow(2, 10)), 2) - (math.log(results.block_size, 2) + math.log(results.associativity, 2)))


def determine_indices():
    return int((results.cache_size * pow(2, 10))/(results.block_size * results.associativity))


def determine_number_of_blocks():
    return int(indices * results.associativity)


def determine_overhead():
    return int(results.associativity * (1 + tag_size) * (indices/8))


def determine_total_implementation_size():
    return int((results.cache_size * pow(2, 10)) + overhead)


def print_formatted_header():
    print('Cache Simulator CS 3853 Spring 2019 - Group #006')
    print()
    print('Cmd Line: ' + ' '.join(sys.argv))
    print('Trace File: ' + results.trace_file)
    print('Cache Size: ' + str(results.cache_size))
    print('Block Size: ' + str(results.block_size))
    print('Associativity: ' + str(results.associativity))
    print('R-Policy: ' + results.replacement_policy)
    print()


def print_generic_header():
    print('Generic:')
    print('Cache Size: ' + str(results.cache_size) + ' KB')
    print('Block Size: ' + str(results.block_size) + ' bytes')
    print('Associativity: ' + str(results.associativity))
    print('Policy: ' + results.replacement_policy)


def print_calculated_values():
    print('----- Calculated Values -----')
    print('Total #Blocks: ' + str(num_blocks) + ' bytes (or ' + str(int(num_blocks/1024)) + ' KB)')
    print('Tag Size: ' + str(tag_size) + ' bits')
    print('Index Size: ' + str(index_size) + ' bits, Total Indices: ' + str(indices) + ' bytes (or ' + str(
        int(indices/1024)) + ' KB)')
    print('Overhead Memory Size: ' + str(overhead) + ' bytes (or ' + str(int(overhead/1024)) + ' KB)')
    print('Implementation Memory Size: ' + str(total_size) + ' bytes (or ' + str(int(total_size/1024)) + ' KB)')


def print_results():
    print('----- Results -----')
    print('Cache Hit Rate: *** %')
    print()


def parse_file(file):
    try:
        with open(file, 'r') as f:
            print_count = 0
            for line in f:
                info = re.match(r'^.+\((\d{2})\).\s{1}(.{8}).+$', line)
                read_write = re.match(r'^.+:\s(\w{8}).*:\s(\w{8}).*$', line)
                if info and print_count <= 99:
                    print('0x' + info.group(2) + ': (' + str(int(info.group(1))) + ')')
                    print_count += 1
                if read_write and print_count <= 99:
                    print('Data write at: ' + read_write.group(1) + ' Data read at : ' + read_write.group(2))
                    test = (binascii.unhexlify(read_write.group(1)))
                    print('a')
    except FileNotFoundError:
        print('Error: File was not found')
        print('Please check that the file exists and try again')
        sys.exit(2)


# Verify the correct number of arguments
if len(sys.argv) < 11:
    print('Error: Invalid number of arguments')
    print('Usage: [python file] -f [trace file] -s [cache size] -b [block size] -a [associativity] '
          '-r [replacement policy]')
    sys.exit(3)

# Define the parser arguments
parser = argparse.ArgumentParser()
parser.add_argument('-f', action="store", dest="trace_file", type=determine_valid_file)
parser.add_argument('-s', action="store", dest="cache_size", type=cache_size_type)
parser.add_argument('-b', action="store", dest="block_size", type=block_size_type)
parser.add_argument('-a', action="store", dest="associativity", type=int, choices=[1, 2, 4, 8, 16])
parser.add_argument('-r', action="store", dest="replacement_policy", choices=['RR', 'RND', 'LRU'])
results = parser.parse_args()

# Calculate values
block_offset = determine_block_offset()
index_size = determine_index_size()
tag_size = 32 - index_size - block_offset
indices = determine_indices()
num_blocks = determine_number_of_blocks()
overhead = determine_overhead()
total_size = determine_total_implementation_size()

# Print the specified headers
print_formatted_header()
print_generic_header()
print_calculated_values()
print_results()

# Parse the file and print the required information
parse_file(results.trace_file)

#James Test Comment
