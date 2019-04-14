#!/usr/bin/env python3

import sys
import os
import argparse
import math
import re
from cache import Cache
from random import randint

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
    print('Cache Simulator - CS3853 - Spring 2019 - Group #006')
    print()
    #print('Cmd Line: ' + ' '.join(sys.argv))
    print('Trace File: ' + results.trace_file)
    #print('Cache Size: ' + str(results.cache_size))
    #print('Block Size: ' + str(results.block_size))
    #print('Associativity: ' + str(results.associativity))
    #print('R-Policy: ' + results.replacement_policy)
    print()


def print_generic_header():
    print('***** Cache Input Parameters *****')
    print()
    print('Cache Size: ' + str(results.cache_size) + ' KB')
    print('Block Size: ' + str(results.block_size) + ' bytes')
    print('Associativity: ' + str(results.associativity))
    print('Replacement Policy: ' + results.replacement_policy)
    print()


def print_calculated_values():
    print('***** Cache Calculated Parameters *****')
    print()
    print('Total #Blocks: ' + str(num_blocks))
    print('Tag Size: ' + str(tag_size) + ' bits')
    print('Total # Rows: ' + str(indices))
    print('Index Size: ' + str(index_size) + ' bits')
    print('Overhead Memory Size: ' + str(int(overhead/1024)) + ' KB')
    print('Implementation Memory Size: ' + str(int(total_size/1024)) + ' KB')
    print()
    print()


def print_results():
    print('***** Cache Simulation Results *****')
    print()
    print('Total Cache Accesses: ' + str(len(cache_accesses)))
    print('Cache Hits: ' + str(cache_hits))
    print('Cache Misses: ' + str(cache_misses))
    print('--- Compulsory Misses: ' + str(compulsory_misses))
    print('--- Conflict Misses: ' + str(conflict_misses))
    print()
    print()
    print('***** ***** CACHE MISS RATE: ***** *****')
    miss_rate = cache_misses/len(cache_accesses) * 100
    miss_rate_string = 'Cache Miss Rate: %.4f' % miss_rate
    print(miss_rate_string + '%')
    print()


def parse_file(file):
    empty = '0x00000000'
    try:
        with open(file, 'r') as f:
            for line in f:
                info = re.match(r'^.+\((\d{2})\).\s(.{8}).+$', line)
                read_write = re.match(r'^.+:\s(\w{8}).*:\s(\w{8}).*$', line)
                if info:
                    address = '0x' + info.group(2)
                    length = int(info.group(1))
                    cache_accesses.append(address + ',' + str(length))
                if read_write:
                    write_address = '0x' + str(read_write.group(1))
                    read_address = '0x' + str(read_write.group(2))
                    if write_address != empty:
                        cache_accesses.append(write_address + ',4')
                    if read_address != empty:
                        cache_accesses.append(read_address + ',4')
    except FileNotFoundError:
        print('Error: File was not found')
        print('Please check that the file exists and try again')
        sys.exit(2)


def determine_number_indices_to_access(access_length, offset_decimal):
    return math.ceil((int(access_length) + int(offset_decimal))/results.block_size)


def calculate_random_number(min_param, max_param):
    return randint(min_param, max_param)


def cache_access(access_list):
    for entry in access_list:
        split = entry.split(',')
        binary_address = bin(int(split[0], 16))[2:].zfill(32)
        calculate_values(binary_address, split[1])


def calculate_values(binary_string, access_length):
    # Calculate bit slices
    offset_start = 32 - block_offset
    index_start = offset_start - index_size

    # Divide the binary string into the tag, index, and offset pieces
    tag_bin = binary_string[0:index_start]
    index_bin = binary_string[index_start:offset_start]
    offset_bin = binary_string[offset_start:32]

    # Convert bit pieces into hex
    tag_hex = hex(int(tag_bin, 2))
    index_hex = hex(int(index_bin, 2))
    offset_hex = hex(int(offset_bin, 2))

    # Calculate index decimal number
    index_decimal = str(int(index_bin, 2))
    offset_decimal = str(int(offset_bin, 2))

    check_cache(index_decimal, tag_hex, access_length, offset_decimal)


def get_rows_from_cache(index_decimal, number_to_access):
    rows = []
    for i in range(number_to_access):
        rows.append(cache.get_row_by_index(int(index_decimal) + i))
    return rows


def check_cache(index, tag, access_length, offset_decimal):
    global compulsory_misses
    global cache_hits
    global cache_misses
    number_of_rows_to_get = determine_number_indices_to_access(access_length, offset_decimal)
    rows = get_rows_from_cache(index, number_of_rows_to_get)

    for current_row in rows:
        if results.associativity == 1:
            # Check for compulsory miss
            if current_row.valid == 0:
                compulsory_misses += 1
                cache_misses += 1
                current_row.tag = tag
                current_row.valid = 1
                break
            else:
                # Row has a valid bit of 1, check the tag
                if current_row.tag == tag:
                    cache_hits += 1
                    break
                else:
                    cache_misses += 1
                    current_row.tag = tag
                    break
        else:
            # Check for compulsory miss
            if current_row[0].valid == 0:
                compulsory_misses += 1
                cache_misses += 1
                current_row[0].tag = tag
                current_row[0].valid = 1
                break
            else:
                # Check all rows for open block or tag match
                for i in len(current_row):
                    if current_row[i].valid == 0:
                        cache_misses += 1
                        current_row[i].tag = tag
                        current_row[i].valid = 1
                        break
                    elif current_row[i].valid == 1 and current_row[i].tag == tag:
                        cache_hits += 1
                        break
                    elif current_row[i].valid == 1 and current_row[i].tag != tag:
                        cache_misses += 1
                        break
                    elif current_row[i].valid == 1 and current_row[i].tag != tag and i == len(current_row):
                        # Random Replace
                        if results.associativity == 'Random':
                            random_num = calculate_random_number(0, len(current_row))
                            current_row[random_num].tag = tag
                        # Round Robin


# Global values
cache_accesses = []
cache_hits = 0
cache_misses = 0
compulsory_misses = 0
conflict_misses = 0

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

# Parse the trace file
parse_file(results.trace_file)

# Create the cache
cache = Cache(indices, results.associativity)

# Iterate through cache accesses list
cache_access(cache_accesses)

# Print the specified results
print_formatted_header()
print_generic_header()
print_calculated_values()
print_results()
