from graphs.impl.CHVG import CHVG
from graphs.impl.CWG import CWG
from graphs.impl.HVG import HVG
from graphs.impl.LEG import LEG
from graphs.impl.TVG import TVG

def get_graph(name, series=None):
    if name == "LEG":
        graph = LEG()
    elif name == "CWG":
        graph = CWG()
    elif name == "HVG":
        graph = HVG()
    elif name == "CHVG":
        graph = CHVG()
    elif name == "TVG":
        graph = TVG()
    else:
        raise Exception("Bad network type!")
    if series is not None:
        graph.set_series(series)
        graph.create_network_from_series()

    return graph