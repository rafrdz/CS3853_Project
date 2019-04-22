#!/usr/bin/env python3

import sys
import argparse
import print_util
import util
from cache import Cache
from slice import Slice

# CS3853 Computer Architecture Project
# Team 6: Rafael Rodriguez, David Brenner, James Solis


def get_row_set_from_cache(access_list):
    cache_offset = cache.get_offset()
    cache_index_size = cache.get_index_size()
    for entry in access_list:
        split = entry.split(',')
        sliced_address = Slice(split[0], cache_offset, cache_index_size)
        cache_row_set = cache.read_cache(int(split[1]), util.bin_to_dec(sliced_address.get_offset()),
                                         sliced_address.get_index())
        access_the_cache(cache_row_set, util.bin_to_hex(sliced_address.get_tag()))


def access_the_cache(cache_rows, tag):
    global cache_accesses
    cache_accesses += len(cache_rows)

    for row in cache_rows:
        check_cache(row, tag)


def check_cache(row, tag):
    global compulsory_misses
    global cache_hits
    global conflict_misses

    for i in range(len(row)):
        block = row[i]
        if block.valid == 0:
            compulsory_misses += 1
            block.tag = tag
            block.valid = 1
            break
        else:
            if i == len(row) - 1 and block.tag != tag:
                conflict_misses += 1
                # Random Replace
                if results.replacement == 'RND':
                    random_num = util.calculate_random_number(0, (len(row) - 1))
                    row[random_num].tag = tag
                    break
                # Round Robin
                if results.replacement == 'RR':
                    round_robin_index = util.determine_round_robin(row)
                    row[round_robin_index].tag = tag
                    break
            elif block.tag == tag:
                cache_hits += 1
                break
            else:
                continue


# Global values
cache_accesses = 0
cache_hits = 0
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
parser.add_argument('-f', action="store", dest="trace_file", type=util.determine_valid_file)
parser.add_argument('-s', action="store", dest="cache_size", type=util.cache_size_type)
parser.add_argument('-b', action="store", dest="block_size", type=util.block_size_type)
parser.add_argument('-a', action="store", dest="associativity", type=int, choices=[1, 2, 4, 8, 16])
parser.add_argument('-r', action="store", dest="replacement", choices=['RR', 'RND'])
results = parser.parse_args()

# Parse the trace file
cache_access_list = util.parse_file(results.trace_file)

# Create the cache access list
cache = Cache(results.cache_size, results.block_size, results.associativity, results.replacement)

# Iterate through accesses
get_row_set_from_cache(cache_access_list)

# Print the specified results
print_util.print_formatted_header(results.trace_file)
print_util.print_generic_header(results.cache_size, results.block_size, results.associativity, results.replacement)
print_util.print_calculated_values(cache.get_num_blocks(), cache.get_tag_size(), cache.get_indices(),
                                   cache.get_index_size(), cache.get_overhead_size(), cache.get_total_size())
print_util.print_results(cache_accesses, cache_hits, conflict_misses, compulsory_misses)
