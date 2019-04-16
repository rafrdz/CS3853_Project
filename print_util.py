def print_formatted_header(trace_file):
    print('Cache Simulator - CS3853 - Spring 2019 - Group #006')
    print()
    print('Trace File: ' + trace_file)
    print()


def print_generic_header(cache_size, block_size, associativity, replacement_policy):
    print('***** Cache Input Parameters *****')
    print()
    print('Cache Size: ' + str(cache_size) + ' KB')
    print('Block Size: ' + str(block_size) + ' bytes')
    print('Associativity: ' + str(associativity))
    print('Replacement Policy: ' + replacement_policy)
    print()


def print_calculated_values(num_blocks, tag_size, indices, index_size, overhead, total_size):
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


def print_results(cache_accesses, cache_hits, conflict_misses, compulsory_misses):
    print('***** Cache Simulation Results *****')
    print()
    print('Total Cache Accesses: ' + str(cache_accesses))
    print('Cache Hits: ' + str(cache_hits))
    print('Cache Misses: ' + str(conflict_misses + compulsory_misses))
    print('--- Compulsory Misses: ' + str(compulsory_misses))
    print('--- Conflict Misses: ' + str(conflict_misses))
    print()
    print()
    print('***** ***** CACHE MISS RATE: ***** *****')
    miss_rate = (conflict_misses + compulsory_misses)/cache_accesses * 100
    miss_rate_string = 'Cache Miss Rate: %.4f' % miss_rate
    print(miss_rate_string + '%')
    print()
