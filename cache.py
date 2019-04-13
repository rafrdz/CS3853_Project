from row import Row


class Cache:
    def __init__(self, indices, associativity):
        if associativity == 1:
            self._rows = [Row() for i in range(indices)]
        else:
            temp_rows = []
            for i in range(indices):
                rows = []
                for a in range(associativity):
                    rows.append(Row())
                temp_rows.append(rows)
            self._rows = temp_rows

    def get_row_by_index(self, index):
        return self._rows[index - 1]

