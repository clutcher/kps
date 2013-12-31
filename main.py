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
 
    def import_amosov_data(self, fileName):
        import xlrd

        book = xlrd.open_workbook(fileName)
        sheet = book.sheet_by_name('RR_1')

        # colums = (2, 5, 8)
        # for rr_row in colums:
        self.RRIntervals.extend(sheet.col_values(2)[5:])

        self.RRIntervals = map(int, self.RRIntervals)

        return 1

    def make_network_with_static_probability(self, probability):
        """Making network from list of R-R Intervals
        probability - probability of graph tunneling"""
        import random

        EdgeList = []
        NumberOfIntervals = len(self.RRIntervals)
        for i in xrange(NumberOfIntervals):
            delta = self.RRIntervals[i]
            j = i + 1
            TunnelingFlag = False
            while (j < NumberOfIntervals):
                if self.RRIntervals[i] > self.RRIntervals[j]:
                    if 0 < (self.RRIntervals[i] - self.RRIntervals[j]) <= delta:
                        delta = self.RRIntervals[i] - self.RRIntervals[j]
                        edge = (i,j)
                        EdgeList.append(edge)
                else:
                    edge = (i,j)
                    EdgeList.append(edge)
                    if not TunnelingFlag and (random.random() <= probability):
                        TunnelingFlag = True
                    else:
                        TunnelingFlag = False
                        break

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


    def make_network_graph(self, GraphName):
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


    def make_parametr_plot(self, xi, param, fileName, log=0):
        import matplotlib.pyplot as plt
        import os

        if log:
            plt.yscale('log')
            plt.xscale('log')
        plt.plot(xi, param, 'ro')

        try:
            os.makedirs('Graphics/params')
        except OSError:
            pass

        fname = "Graphics/params/" + fileName + ".png"
        plt.savefig(fname)
        plt.close('all')
        return 1


    def make_research_static_probability(self):
        import numpy
        params = []
        # self.generate_poisson_random_data(10, 1000)
        # self.generate_simple321_random_data(100)
        xiRange = numpy.arange(0., 1., 0.1)
        for probability in xiRange:
            self.make_network_with_static_probability(probability)
            params.append(self.calculate_graph_parametrs())
            # self.make_network_graph(str(probability))

        self.make_parametr_plot(xiRange, [d['clustering'] for d in params], "clustering")
        self.make_parametr_plot(xiRange, [d['shortpath'] for d in params], "shortpath")
        self.make_parametr_plot(xiRange, [d['assorativity'] for d in params], "assorativity")
        self.make_parametr_plot(xiRange, [d['edges'] for d in params], "edges")
        self.make_parametr_plot(xiRange, [d['average_degree'] for d in params], "average_degree")
        self.make_parametr_plot(xiRange, [d['diametr'] for d in params], "diametr")
        self.make_parametr_plot(xiRange, [d['nodes'] for d in params], "nodes")

        return params

Test = TVG()
Test.import_amosov_data('input.xls')
Test.make_network_with_static_probability(0.0)

print Test.make_research_static_probability()

# Test.generate_simple321_random_data(10)
# Test.generate_poisson_random_data(10, 100)
# print Test.RRIntervals
# Test.make_network_with_static_probability(1)
# Test.make_graphic("123")
# print Test.calculate_graph_parametrs()
# print Test.calculate_average_degree()
