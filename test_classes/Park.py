#!usr/bin/python

# The Park
# Weather:
#   + Temperature: frozen|cold|warm|hot
#   + Precipitation: snow|rain|drizzle|dry 
# Terrain:
#   + Surface: mud|grass|gravel|road
#   + Inclination: mountane|hilly|undulating|flat

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
