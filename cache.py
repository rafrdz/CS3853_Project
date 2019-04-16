import math
import util
from row import Row
from slice import Slice


class Cache:
    def __init__(self, cache_size, block_size, associativity, replacement):
        self._size = cache_size
        self._block_size = block_size
        self._associativity = associativity
        self._replacement = replacement

        self._indices = int((self._size * pow(2, 10))/(self._block_size * self._associativity))
        self._blocks = int(self._indices * self._associativity)

        if associativity == 1:
            self._rows = [Row() for i in range(self._indices)]
        else:
            temp_rows = []
            for i in range(self._indices):
                rows = []
                for a in range(associativity):
                    rows.append(Row())
                temp_rows.append(rows)
            self._rows = temp_rows

        self._index_size = int(math.log((self._size * pow(2, 10)), 2) - (math.log(self._block_size, 2) +
                                                                         math.log(self._associativity, 2)))
        self._offset = int(math.log(self._block_size, 2))
        self._tag_size = 32 - self._index_size - self._offset
        self._num_blocks = int(self._indices * self._associativity)
        self._overhead_size = int(self._associativity * (1 + self._tag_size) * (self._indices/8))
        self._total_size = int((self._size * pow(2, 10)) + self._overhead_size)

    def get_num_blocks(self):
        return self._num_blocks

    def get_tag_size(self):
        return self._tag_size

    def get_indices(self):
        return self._indices

    def get_index_size(self):
        return self._index_size

    def get_overhead_size(self):
        return self._overhead_size

    def get_total_size(self):
        return self._total_size

    def get_offset(self):
        return self._offset

    def get_row_by_index(self, index):
        return self._rows[index - 1]

    def read_cache(self, access_length, offset_bin, index_bin):
        num_rows = math.ceil((int(access_length) + util.bin_to_dec(offset_bin))/self._block_size)
        return self._get_cache_rows(util.bin_to_dec(index_bin) - 1, num_rows)

    def _get_cache_rows(self, index, num_rows):
        return self._rows[index:(index + (num_rows - 1))]
