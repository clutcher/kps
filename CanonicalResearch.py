import networkx as nx
import igraph
import graphs.GraphFactory as GF

import utils.PlotParameters as PP
import utils.TimeSeriesGenerator as TS
import utils.DataImport as DI

number_of_nodes = 2000


def calculate_network_parameters(series, name):
    graph = GF.get_graph("TVG")
    graph.set_series(series)
    graph.create_network_from_series()
    graph.name = name
    graph.get_params()
    PP.make_xy_plot()

    # PP.make_degree_distribution(graph)

    # print nx.average_clustering(graph)
    # print nx.degree_assortativity_coefficient(graph)
    # print graph.average_degree()

    # print nx.degree_assortativity_coefficient(graph, weight="weight")
    # print nx.average_clustering(graph, weight="weight")
    # print graph.weighted_average_degree()
    #
    # print nx.info(graph)
    # print nx.average_shortest_path_length(graph)


if __name__ == "__main__":
    # print "PERIODIC"
    # time_series = TS.generate_periodic(number_of_nodes)
    # calculate_network_parameters(time_series, "per")

    # print "POISSON"
    # time_series = TS.generate_poisson(number_of_nodes)
    # calculate_network_parameters(time_series, "poi")
    #
    # print "RANDOM"
    # time_series = TS.generate_random(number_of_nodes)
    # calculate_network_parameters(time_series, "ran")

    # print "STATIC"
    # time_series = TS.generate_static(number_of_nodes)
    # calculate_network_parameters(time_series, "stat")

    # print "SINUSOID"
    # time_series = DI.import_from_file("/home/clutcher/projects/vgr/1.txt")
    # x = xrange(len(time_series))
    # PP.make_xy_plot(x, time_series)

    graph = GF.get_graph("TVG")
    time_series = TS.generate_periodic(number_of_nodes)
    graph.set_series(time_series)
    graph.create_network_from_series()

    tmpGraph = igraph.Graph()
    tmpGraph.add_vertices(graph.nodes())
    tmpGraph.add_edges(graph.edges())
    # result["short_path"] = nx.average_shortest_path_length(self, weight=weight)
    print len(graph.nodes())
    a = tmpGraph.average_path_length()
    print nx.average_shortest_path_length(graph)
    print a
    # print len(a)
    # print sum(a)
    # print sum(a)/float(len(a))
