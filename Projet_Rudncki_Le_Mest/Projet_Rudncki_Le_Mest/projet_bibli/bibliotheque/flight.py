from cartopy.crs import PlateCarree

# Création de la classe Flight


class Flight:
    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return (
            f"Flight {self.callsign} with aircraft {self.icao24} "
            f"on {self.min('timestamp'):%Y-%m-%d} "
        )

    def __lt__(self, other):
        return self.min("timestamp") <= other.min("timestamp")

    def max(self, feature):
        return self.data[feature].max()

    def min(self, feature):
        return self.data[feature].min()

    @property
    def callsign(self):
        return self.min("callsign")

    @property
    def icao24(self):
        return self.min("icao24")

    def plot(self, ax, **kwargs):
        self.data.query("latitude == latitude").plot(
            ax=ax,
            x="longitude",
            y="latitude",
            legend=False,
            transform=PlateCarree(),
            **kwargs,
        )

    # Attribut permettant de différentier les avions qui décollent de ceux qui atterrissent
    def decol_atter(self):
        if self.data.vertical_rate.mean() > 1000:
            return "décollage"
        elif self.data.vertical_rate.mean() < -500:
            return "atterissage"
        else:
            return "autre"
