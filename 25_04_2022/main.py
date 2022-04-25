from collector import CollectorGuard
from collector import Collector
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
