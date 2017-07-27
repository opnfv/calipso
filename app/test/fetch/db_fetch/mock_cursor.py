class MockCursor:

    def __init__(self, result):
        self.result = result
        self.current = 0

    def __next__(self):
        if self.current < len(self.result):
            next = self.result[self.current]
            self.current += 1
            return next
        else:
            raise StopIteration

    def __iter__(self):
        return self
