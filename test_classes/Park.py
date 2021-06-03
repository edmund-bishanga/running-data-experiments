#!usr/bin/python

"""
This Class describes The Park: Athletics Training Space
Environmental Characteristics: Static and Dynamic
Weather:
  + Temperature: frozen|cold|warm|hot
  + Precipitation: snow|rain|drizzle|dry 
Terrain:
  + Surface: mud|grass|gravel|tarmac
  + Inclination: mountane|hilly|undulating|flat
"""


class Park(object):
    # Properties:
    # + sensible defaults.
    # + can be provided by user: not static.
    def __init__(self, venue, temperature, precipitation, surface, inclination):
        self.venue = venue
        self.temperature = temperature
        self.precipitation = precipitation
        self.surface = surface
        self.inclination = inclination
        self.location = None

    def get_location(self):
        if not self.location:
            self.location = 'MyNeighbourHood'
        return self.location

    def get_temperature(self):
        if not self.temperature:
            self.temperature = 10 # deg Celcius
        return self.temperature


class TarRoad(Park):
    def __init__(self, venue, temperature, precipitation, surface, inclination):
        super().__init__(venue, temperature, precipitation, surface, inclination)
        self.surface = 'tarmac'



