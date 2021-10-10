import pandas as pd
from .fonctions import iterate_icao24_callsign
from .fonctions import iterate_time
from .flight import Flight

# Création de la classe FlightCollection


class FlightCollection:
    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"FlightCollection with {self.data.shape[0]} records"

    @classmethod
    def read_pickle(cls, filename):
        return cls(pd.read_pickle(filename))

    def __iter__(self):
        for group in iterate_icao24_callsign(self.data):
            for elt in iterate_time(group, 20000):
                yield Flight(elt)

    def __len__(self):
        return sum(1 for _ in self)

    def __getitem__(self, key):
        result = FlightCollection(
            self.data.query(f"callsign == '{key}' or icao24 == '{key}'")
        )

        if len(result) == 1:
            return Flight(result.data)
        else:
            return result
