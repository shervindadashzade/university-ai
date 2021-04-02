class Unit:
    def __init__(self,number,capacity,maintenance_interval):
        self.number = number
        self.capacity = capacity
        self.maintenance_interval = maintenance_interval
        
class Interval:
    def __init__(self,number,min_load):
        self.number = number
        self.min_load = min_load


class ReadInputs:
    def __init__(self):
        self.units = []
        self.intervals = []
    def load(self):
        ## load units
        file = open("units.txt")
        lines = file.readlines();
        n = int(lines[0])
        for i in range(1,n+1):
            unit = Unit(i,int(lines[i*3-1]),int(lines[i*3]))
            self.units.append(unit)
        file = open("intervals.txt")
        lines = file.readlines()
        n = int(lines[0])
        for i in range(1,n+1):
            interval = Interval(i,int(lines[i*2]))
            self.intervals.append(interval)
    def showUnits(self):
        print("number\tcapacity\tmaintenance intervals")
        for unit in self.units:
            print('%d\t%d\t%d' % (unit.number,unit.capacity,unit.maintenance_interval))
    def showIntervals(self):
        print("number\tmin_load")
        for interval in self.intervals:
            print("%d\t%d" % (interval.number,interval.min_load))