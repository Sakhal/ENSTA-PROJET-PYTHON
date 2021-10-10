import numpy as np
from shapely.geometry import MultiPolygon
from descartes import PolygonPatch

# Fonction iterate_callsign qui renvoie les données groupées par "callsign"


def iterate_callsign(data):
    for _, chunk in data.groupby("callsign"):
        yield chunk


# Fonction iterate_icao24_callsign qui renvoie les données groupées par
# "callsign" et "icao24" pour identifier les avions et leur numéro de mission
def iterate_icao24_callsign(data):
    for _, chunk in data.groupby(["icao24", "callsign"]):
        yield chunk


def iterate_time(data, threshold):
    idx = np.where(data.timestamp.diff().dt.total_seconds() > threshold)[0]
    start = 0
    for stop in idx:
        yield data.iloc[start:stop]
        start = stop
    yield data.iloc[start:]


def iterate_all(data, threshold):
    for group in iterate_icao24_callsign(data):
        for elt in iterate_time(group, 20000):
            yield elt


# Fonction permettant de récupérer les autoroutes ainsi que leur géométrie
def autoroute_geom(data):
    typeroute = [p for p in data["VOCATION"]]
    routegeometry = [p for p in data["geometry"]]

    nbr_autoroute = 0
    autoroutegeometry = []

    for i in range(0, len(typeroute) - 1):
        if typeroute[i] == "Type autoroutier":
            nbr_autoroute = nbr_autoroute + 1
            autoroutegeometry.append(routegeometry[i])
    return autoroutegeometry


# Fonction permettant de tracer les autoroutes
def carte_route(data, ax):
    for i in range(0, len(data) - 1):
        auto_x = [p[0] for p in list(data[i].coords)]
        auto_y = [p[1] for p in list(data[i].coords)]
        ax.plot(auto_x, auto_y, "y")


# Fonction permettant de tracer les fleuves
def carte_fleuve(data, ax):
    for i in range(0, len(data) - 1):
        fleuve_x = [p[0] for p in list(data[i].coords)]
        fleuve_y = [p[1] for p in list(data[i].coords)]
        ax.plot(fleuve_x, fleuve_y, "b")


# Fonction permettant de tracer les communes
def carte_commune(data, ax):
    for s in data:
        if s.geom_type == "Polygon":
            s = MultiPolygon([s])
            for idx, p in enumerate(s):
                ax.add_patch(
                    PolygonPatch(
                        p, fc="#6699cc", ec="#6699cc", alpha=0.5, zorder=2
                    )
                )
