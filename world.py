class World:
    def __init__(self):
        self.interchange_stations = []
        self.stations = []
        self.lines = []
        self.trains = []

    def add_interchange_station(self, interchange_station):
        self.interchange_stations.append(interchange_station)
        self.add_station(interchange_station)

    def add_station(self, station):
        self.stations.append(station)

    def add_line(self, line):
        self.lines.append(line)

    def add_train(self, train):
        self.trains.append(train)
        train.line.trains.append(train)

    def update(self, dt):
        for station in self.stations:
            station.update(dt)
        for line in self.lines:
            line.update(dt)

    def draw(self, screen):
        for line in self.lines:
            line.draw(screen)
        for station in self.stations:
            station.draw(screen)