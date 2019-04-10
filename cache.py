from row import Row

class Cache:
    def __init__(self, indices, associativity):
        if associativity == 1:
            self._rows = [Row() for i in range(indices)]
        else:
            rows = []
            for a in range(associativity):
                rows.append(Row())
            self._rows = [rows for i in range(indices)]
