import collections
import statistics


class Seriesadder:
    def __init__(self, n):
        self.size = n
        self.values = collections.deque(maxlen=n)

    def add(self, value):
        if value % 2 == 0:
            self.values.append(value)

    def sum(self):
        return sum(self.values)

    def avg(self):
        return statistics.mean(self.values)

    def clear(self):
        self.values = collections.deque(maxlen=self.size)


adder = Seriesadder(3)

adder.add(10)
adder.add(12)
adder.add(14)
assert (adder.sum() == 36)
assert(adder.avg() == 12)
adder.add(16)
assert (adder.sum() == 42)
assert (adder.avg() == 14)
adder.add(11)
assert (adder.sum() == 42)
assert (adder.avg() == 14)
