import networkx as nx
import graphs.GraphFactory as GF

import utils.PlotParameters as PP
import utils.TimeSeriesGenerator as TS


number_of_nodes = 1000


def calculate_network_parameters(series, name):
    graph = GF.get_graph("CWG")
    graph.set_series(series)
    graph.create_network_from_series()
    graph.name = name

    PP.make_weighted_degree_distribution(graph)

    # print nx.average_clustering(graph)
    # print nx.degree_assortativity_coefficient(graph)
    # print graph.average_degree()

    # try:
    #     print nx.average_clustering(graph, weight="weight")
    # except:
    #     print "Clustering calc error"
    # try:
    #     print nx.degree_assortativity_coefficient(graph, weight="weight")
    # except:
    #     print "Assortativity calc error"
    # try:
    #     print graph.weighted_average_degree()
    # except:
    #     print "Average degree calc error"
    # try:
    #     print nx.info(graph)
    # except:
    #     print "nx.info calc error"
    # print nx.average_shortest_path_length(graph)


if __name__ == "__main__":
    print "AFDB"
    time_series = TS.import_from_file("fast/afdb.rr.qrs.08455.txt")
    calculate_network_parameters(time_series, "afdb_w")

    print "CHF2DB"
    time_series = TS.import_from_file("fast/chf2db.rr.atr.chf226.txt")
    calculate_network_parameters(time_series, "chf2db_w")

    print "LTAFDB"
    time_series = TS.import_from_file("fast/ltafdb.rr.atr.75.txt")
    calculate_network_parameters(time_series, "ltafdb_w")

    print "MITDB"
    time_series = TS.import_from_file("fast/mitdb.rr.atr.117.txt")
    calculate_network_parameters(time_series, "mitdb_w")

    print "NSR2DB"
    time_series = TS.import_from_file("fast/nsr2db.rr.atr.nsr053.txt")
    calculate_network_parameters(time_series, "nsr2db_w")
