import collections
import math
import statistics


class SensorValue:
    def __init__(self, value, time):
        self.value = value
        self.time = time

    def __repr__(self):
        return f"SensorValue({self.value}, {self.time})"


class Datastore:
    def __init__(self, max_size):
        self.data = collections.deque(maxlen=max_size)

    def addValue(self, sv):
        self.data.append(sv)

    def getAverage(self):
        return statistics.mean((sv.value for sv in self.data))

    def getMax(self):
        return max(self.data, key=lambda sv: sv.value)

    def getMin(self):
        return min(self.data, key=lambda sv: sv.value)

    def printValue(self):
        print("==========================")
        print("Average:", self.getAverage())
        print("Max:", self.getMax())
        print("Min:", self.getMin())


class ControlSystem(Datastore):
    def __init__(self, max_size, min_threshold=-math.inf, max_threshold=math.inf):
        super().__init__(max_size)
        self.min_threshold = min_threshold
        self.max_threshold = max_threshold

    def addValue(self, sv):
        if not self.min_threshold <= sv.value <= self.max_threshold:
            raise Exception(
                f"Value: {sv.value} is outside of thresholds min: {self.min_threshold} and max: {self.max_threshold}")
        super().addValue(sv)


if __name__ == '__main__':
    c = ControlSystem(5, min_threshold=5, max_threshold=25)
    # c = Datastore(5)
    c.addValue(SensorValue(10, "20:00"))
    c.printValue()
    c.addValue(SensorValue(15, "20:01"))
    c.printValue()
    c.addValue(SensorValue(20, "20:02"))
    c.printValue()
    c.addValue(SensorValue(21, "20:03"))
    c.printValue()
    c.addValue(SensorValue(22, "20:04"))
    c.printValue()
    c.addValue(SensorValue(23, "20:05"))
    c.printValue()
    c.addValue(SensorValue(24, "20:06"))
    c.printValue()
    c.addValue(SensorValue(25, "20:07"))
    c.printValue()
    c.addValue(SensorValue(26, "20:08"))
    c.printValue()
