import collections
import statistics

class SensorValue:
    def __init__(self, value, time):
        self.value = value
        self.time = time

class Datastore:
    def __init__(self, max_size):
        self.data = collections.deque(maxlen=max_size)

    def addValue(self, sv):
        self.data.append(sv)
    
    def getAverage(self):
        return statistics.mean((o.value for o in self.data))

    def getMax(self):
        return max(self.temp_data, key=lambda x: x.value)
    
    def getMin(self):
        return min(self.temp_data, key=lambda x: x.value)
    
    def printValue(self):
        print("==========================")
        print("Average:", self.getAverage())
        print("Max:", self.getMax())
        print("Min:", self.getMin())
        

class CollectorGuard(Collector):
    def __init__(self, max_size, threshold):
        super().__init__(max_size)
        self.threshold = threshold
        
    def addValue(self, temp, time):
        if temp > self.threshold:
            raise Exception("Value is too high")
        super().addValue(temp, time)

if __name__ == '__main__':
    #c = CollectorGuard(5, 25)
    c = Collector(5)

    c.addValue(10, "20:00")
    c.printValue()
    c.addValue(15, "20:01")
    c.printValue()
    c.addValue(20, "20:02")
    c.printValue()
    c.addValue(21, "20:03")
    c.printValue()
    c.addValue(22, "20:04")
    c.printValue()
    c.addValue(23, "20:05")
    c.printValue()
    c.addValue(24, "20:06")
    c.printValue()
    c.addValue(25, "20:07")
    c.printValue()
    c.addValue(26, "20:08")
    c.printValue()
