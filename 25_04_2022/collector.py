import collections

class Collector:
    def __init__(self, max_size):
        self.temp_data = collections.deque(maxlen=max_size)
        self.time_data = collections.deque(maxlen=max_size)

    def addValue(self, temp, time):
        self.temp_data.append(temp)
        self.time_data.append(time)
    
    def getAverage(self):
        return sum(self.temp_data) / len(self.temp_data)

    def getMax(self):
        m = max(self.temp_data)
        return [m, self.time_data[self.temp_data.index(m)]]
    
    def getMin(self):
        m = min(self.temp_data)
        return [m, self.time_data[self.temp_data.index(m)]]
    
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