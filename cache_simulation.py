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


def check_cache(row, tag):
    global compulsory_misses
    global cache_hits
    global conflict_misses

    if results.associativity == 1:
        if row.valid == 0:
            compulsory_misses += 1
            row.tag = tag
            row.valid = 1
        else:
            if row.tag != tag:
                conflict_misses += 1
                row.tag = tag
            else:
                cache_hits += 1
    else:
        for i in range(len(row)):
            block = range[i]
            if block.valid == 0:
                compulsory_misses += 1
                block.tag = tag
                block.valid = 1
            else:
                if i == len(row) - 1 and i > 0 and block.tag != tag:
                    conflict_misses += 1
                    # Random Replace
                    if results.replacement == 'RND':
                        random_num = util.calculate_random_number(0, (len(block) - 1))
                        block[random_num].tag = tag
                        break
                    # Round Robin
                    if results.replacement == 'RR':
                        round_robin_index = util.determine_round_robin(block)
                        block[round_robin_index].tag = tag
                        break
                elif block.tag == tag:
                    cache_hits += 1


def access_the_cache(cache_rows, tag):
    #global compulsory_misses
    #global cache_hits
    global cache_accesses
    #global conflict_misses
    cache_accesses += len(cache_rows)

    for row in cache_rows:
        check_cache(row, tag)

    # # There is only a single row to access and a single column
    # if len(cache_rows) == 1 and results.associativity == 1:
    #     # Check for valid bit of 0, compulsory miss
    #     if cache_rows[0].valid == 0:
    #         compulsory_misses += 1
    #         cache_rows[0].tag = tag
    #         cache_rows[0].valid = 1
    #     else:
    #         # Valid bit is 1, check tag for match or set tag
    #         if cache_rows[0].tag == tag:
    #             cache_hits += 1
    #         else:
    #             conflict_misses += 1
    #             cache_rows[0].tag = tag
    # # There is only a single row but multiple blocks per row
    # elif len(cache_rows) == 1 and results.associativity > 1:
    #     for i in range(len(cache_rows[0])):
    #         block = cache_rows[0][i]
    #         # Check for valid bit of first block being 0
    #         # If so, compulsory miss and set tag and valid bit
    #         if block.valid == 0:
    #             compulsory_misses += 1
    #             block.tag = tag
    #             block.valid = 1
    #             break
    #         if block.valid == 1:
    #             # If tag of valid block matches address tag, hit
    #             if block.tag == tag:
    #                 cache_hits += 1
    #                 break
    #             # If tag of valid block does not match address tag,
    #             # check for current position in row
    #             else:
    #                 # If true, we're at the end of the row, need to replace
    #                 if i == (len(cache_rows[0]) - 1):
    #                     conflict_misses += 1
    #                     # Random Replace
    #                     if results.replacement == 'RND':
    #                         random_num = util.calculate_random_number(0, (len(cache_rows[0]) - 1))
    #                         cache_rows[0][random_num].tag = tag
    #                     # Round Robin
    #                     if results.replacement == 'RR':
    #                         round_robin_index = util.determine_round_robin(cache_rows[0])
    #                         cache_rows[0][round_robin_index].tag = tag
    #                     break
    #                 # We're not at the end, keep searching
    #                 else:
    #                     continue
    # # There are multiple row but only one block per row
    # elif len(cache_rows) > 1 and results.associativity == 1:
    #     for i in range(len(cache_rows)):
    #         block = cache_rows[i]
    #         # Check for valid bit of first block being 0
    #         # If so, compulsory miss and set tag and valid bit
    #         if block.valid == 0:
    #             compulsory_misses += 1
    #             block.tag = tag
    #             block.valid = 1
    #         else:
    #             # Valid bit is 1, check tag for match or set tag
    #             if cache_rows[0].tag == tag:
    #                 cache_hits += 1
    #             else:
    #                 conflict_misses += 1
    #                 cache_rows[0].tag = tag
    # # There are multiple rows
    # elif len(cache_rows) > 1:
    #     for i in range(len(cache_rows)):
    #         current_row = cache_rows[i]
    #         for j in range(len(current_row)):
    #             block = current_row[j]
    #             # Check for valid bit of first block being 0
    #             # If so, compulsory miss and set tag and valid bit
    #             if block.valid == 0:
    #                 compulsory_misses += 1
    #                 block.tag = tag
    #                 block.valid = 1
    #                 break
    #             if block.valid == 1:
    #                 # If tag of valid block matches address tag, hit
    #                 if block.tag == tag:
    #                     cache_hits += 1
    #                     break
    #                 # If tag of valid block does not match address tag,
    #                 # check for current position in row
    #                 else:
    #                     # If true, we're at the end of the row, need to replace
    #                     if j == (len(cache_rows[0]) - 1):
    #                         conflict_misses += 1
    #                         # Random Replace
    #                         if results.replacement == 'RND':
    #                             random_num = util.calculate_random_number(0, (len(cache_rows[0]) - 1))
    #                             cache_rows[0][random_num].tag = tag
    #                         # Round Robin
    #                         if results.replacement == 'RR':
    #                             round_robin_index = util.determine_round_robin(cache_rows[0])
    #                             cache_rows[0][round_robin_index].tag = tag
    #                         break
    #                     # We're not at the end, keep searching
    #                     else:
    #                         continue


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
parser.add_argument('-r', action="store", dest="replacement", choices=['RR', 'RND', 'LRU'])
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
