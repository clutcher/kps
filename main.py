"""Tunneling Visibility Graph"""
import networkx as nx


class TVG(object):

    """Tunneling Visibility Graph Class"""

    def __init__(self, RRIntervals=[]):
        self.RRIntervals = RRIntervals
        self.graph = None

    def generate_simple321_random_data(self, NumberOfSeries):
        """Making series 3-2-1"""
        for i in xrange(NumberOfSeries):
            self.RRIntervals.extend([3, 2, 1])
        return 1

    def generate_poisson_random_data(self, Plambda, NumberOfData):
        import numpy as np

        self.RRIntervals = np.random.poisson(Plambda, NumberOfData)
        return 1

    def make_network_with_static_probability(self, probability):
        """Making network from list of R-R Intervals
        probability - probability of graph tunneling"""
        import random

        EdgeList = []
        NumberOfIntervals = len(self.RRIntervals)
        for i in xrange(NumberOfIntervals):
            j = i + 1
            flag = True
            while flag and j < NumberOfIntervals:
                flag = False
                if self.RRIntervals[i] > self.RRIntervals[j]:
                    edge = (i, j)
                    EdgeList.append(edge)
                    flag = True
                elif random.random() <= probability:
                    edge = (i, j)
                    EdgeList.append(edge)
                    flag = True
                j = j + 1
        self.graph = nx.from_edgelist(EdgeList)
        return 1

    def calculate_average_degree(self):
        NumberOfNodes = self.graph.number_of_nodes()
        SummOfDegree = sum(self.graph.degree().values())
        AverageDegree = float(SummOfDegree) / float(NumberOfNodes)
        return AverageDegree

    def calculate_graph_parametrs(self):
        parameters = {}
        parameters["clustering"] = nx.average_clustering(self.graph)
        parameters["assorativity"] = nx.degree_assortativity_coefficient(self.graph)
        parameters["nodes"] = self.graph.number_of_nodes()
        parameters["edges"] = self.graph.number_of_edges()
        parameters["average_degree"] = self.calculate_average_degree()
        if nx.is_connected(self.graph):
            parameters["shortpath"] = nx.average_shortest_path_length(self.graph)
            parameters["diametr"] = nx.diameter(self.graph)
        else:
            shortpath = []
            diameter = []
            for g in nx.connected_component_subgraphs(self.graph):
                shortpath.append(nx.average_shortest_path_length(g))  
                diameter.append(nx.diameter(g))
            parameters["shortpath"] = shortpath   
            parameters["diameter"] = diameter
        return parameters    


    def make_graphic(self, GraphName):
        """Make graph of network"""
        import matplotlib.pyplot as plt
        import os

        plt.title("Network graph")
        pos = nx.graphviz_layout(self.graph, prog="circo", root=0)
        nx.draw(self.graph, pos, with_labels=False, alpha=0.5,
                node_size=[30 * float(self.graph.degree(v)) for v in self.graph],
                node_color=[float(self.graph.degree(v)) for v in self.graph])
        try:
            os.makedirs('Graphics/graph')
        except OSError:
            pass
        fname = "Graphics/graph/"+str(GraphName)+".png"
        plt.savefig(fname)
        plt.close('all')


    def make_research_static_probability(self):
        import numpy
        params = []
        self.generate_poisson_random_data(10, 1000)
        # self.generate_simple321_random_data(100)
        for probability in numpy.arange(0., 1., 0.1):
            self.make_network_with_static_probability(probability)
            params.append(self.calculate_graph_parametrs())
            # self.make_graphic(str(probability))
        return params

Test = TVG()
print Test.make_research_static_probability()

# Test.generate_random_data(10)
# Test.generate_poisson_random_data(10, 100)
# print Test.RRIntervals
# Test.make_network_with_static_probability(0.1)
# Test.make_graphic()
# print Test.calculate_graph_parametrs()
# print Test.calculate_average_degree()
