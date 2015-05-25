import research.BaseResearch
from research.impl.DBResearch import DBResearch
from research.impl.TVGResearch import TVGResearch
from graphs.impl.TVG import TVG
from utils import DataImport as di
import networkx as nx

if __name__ == "__main__":
    # network_type = "CHVG"
    # network_research = research.BaseResearch.BaseResearch(network_type)
    # network_research.make_all_db_graph("clustering", "assortativity")

    # network_research.create_networks_from_data()
    # print "1"
    # network_research.calculate_networks_params()
    # print "2"
    # network_research.plot_network_param_ranked()

    network_type = "TVG"
    network_research = TVGResearch()
    # network_research.PHYSIO_NET_DBS = ["nsr2db"]
    # network_research.PHYSIO_NET_DBS = ["afdb", "nsr2db", "mitdb"]
    # network_research.PHYSIO_NET_DBS = ["chfdb", "ltafdb", "chf2db"]
    # network_research.create_networks_from_data()
    # network_research.CALCULATING_PARAMS = ["short_path"]
    # network_research.calculate_networks_params()
    network_research.make_all_db_graph("short_path", "assortativity")
