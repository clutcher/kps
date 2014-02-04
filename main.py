# -*- coding: utf-8 -*-

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

    def generate_random_data(self, NumberOfData):
        import random
        for i in xrange(NumberOfData):
            self.RRIntervals.append(random.random())
        return 1

    def import_amosov_data(self, fileName, type='all'):
        import xlrd

        book = xlrd.open_workbook(fileName)
        sheet = book.sheet_by_name('RR_1')

        if type == 'all':
            colums = (2, 5, 8)
            for rr_row in colums:
                try:
                    self.RRIntervals.extend(sheet.col_values(rr_row)[5:])
                except:
                    print 'Import column error'
        else:
            self.RRIntervals.extend(sheet.col_values(2)[5:])

        self.RRIntervals = map(int, self.RRIntervals)

        flagZero = True
        while flagZero:
            if (self.RRIntervals[-1] == 0):
                del self.RRIntervals[-1]
            else:
                flagZero = False
                break
        return 1

    def filter_intervals(self, zero=1, height=1):
        if zero:
            self.RRIntervals = filter(lambda a: a != 0, self.RRIntervals)
        if height:
            average = sum(self.RRIntervals) / float(len(self.RRIntervals))
            self.RRIntervals = filter(
                lambda a: a < average * 2, self.RRIntervals)

        return 1

    def export_intervals(self, fileName='intervals'):
        import os

        try:
            os.makedirs('data')
        except OSError:
            pass
        fname = "data/" + str(fileName) + ".txt"

        f = open(fname, 'w')
        for item in self.RRIntervals:
            f.write("%s\n" % item)

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
                        edge = (i, j)
                        EdgeList.append(edge)
                else:
                    edge = (i, j)
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

    def calculate_graph_parametrs(self, fileName=0):
        parameters = {}
        parameters["clustering"] = nx.average_clustering(self.graph)
        parameters["assorativity"] = nx.degree_assortativity_coefficient(
            self.graph)
        parameters["nodes"] = self.graph.number_of_nodes()
        parameters["edges"] = self.graph.number_of_edges()
        parameters["average_degree"] = self.calculate_average_degree()
        if nx.is_connected(self.graph):
            parameters[
                "shortpath"] = nx.average_shortest_path_length(self.graph)
            parameters["diametr"] = nx.diameter(self.graph)
        else:
            g = nx.connected_component_subgraphs(self.graph)
            parameters["shortpath"] = nx.average_shortest_path_length(g[0])
            parameters["diameter"] = nx.diameter(g[0])
            parameters[
                "number_of_components"] = nx.number_connected_components(self.graph)

        if fileName:
            import os

            try:
                os.makedirs('data')
            except OSError:
                pass
            fname = "data/" + str(fileName) + "-params.txt"

            f = open(fname, 'w')
            f.write(str(parameters))

        return parameters

    def make_network_graph(self, GraphName):
        """Make graph of network"""
        import matplotlib.pyplot as plt
        import os

        plt.title("Network graph")
        pos = nx.graphviz_layout(self.graph, prog="circo", root=0)
        nx.draw(self.graph, pos, with_labels=False, alpha=0.5,
                node_size=[30 * float(self.graph.degree(v))
                           for v in self.graph],
                node_color=[float(self.graph.degree(v)) for v in self.graph])
        try:
            os.makedirs('Graphics/graph')
        except OSError:
            pass
        fname = "Graphics/graph/" + str(GraphName) + ".png"
        plt.savefig(fname)
        plt.close('all')

    def make_distribution_histogram(self, fileName):
        import matplotlib.pyplot as plt
        import os

        xi = []
        yi = []
        for interval in sorted(set(self.RRIntervals)):
            xi.append(interval)
            yi.append(self.RRIntervals.count(interval))
        for i in xrange(len(yi)):
            yi[i] = float(yi[i]) / len(self.RRIntervals)

        plt.plot(xi, yi)
        try:
            os.makedirs('Graphics/params')
        except OSError:
            pass

        fname = "Graphics/params/" + fileName + ".png"
        plt.savefig(fname)
        plt.close('all')
        return 1

    def make_intervals_plot(self, fileName):
        import matplotlib.pyplot as plt
        import os

        plt.plot(self.RRIntervals)

        try:
            os.makedirs('Graphics/params')
        except OSError:
            pass

        fname = "Graphics/params/" + fileName + ".png"
        plt.savefig(fname)
        plt.close('all')
        return 1

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

    def make_research_static_probability(self, step=0.1, prefix="", fileName="data-fallback.txt"):
        params = []
        xiRange = []

        probability = 0.
        xiRange.append(probability)

        while probability < 1:
            self.make_network_with_static_probability(probability)
            params.append(self.calculate_graph_parametrs())
            # self.make_network_graph(str(probability))
            probability = probability + step
            xiRange.append(probability)

        try:
            self.make_parametr_plot(
                xiRange, [d['clustering'] for d in params], prefix + "clustering")
            self.make_parametr_plot(
                xiRange, [d['shortpath'] for d in params], prefix + "shortpath")
            self.make_parametr_plot(
                xiRange, [d['assorativity'] for d in params], prefix + "assorativity")
            self.make_parametr_plot(
                xiRange, [d['edges'] for d in params], prefix + "edges")
            self.make_parametr_plot(
                xiRange, [d['average_degree'] for d in params], prefix + "average_degree")
            self.make_parametr_plot(
                xiRange, [d['diametr'] for d in params], prefix + "diametr")
            self.make_parametr_plot(
                xiRange, [d['nodes'] for d in params], prefix + "nodes")
            self.make_parametr_plot(
                xiRange, [d['number_of_components'] for d in params], prefix + "number_of_components")
        except:
            print "Plot error. Maybe server without display!"
            print params
            f = open(fileName, 'w')
            f.write(str(params))
        return params

    def complex_research(self):
        self.RRIntervals = []
        self.generate_simple321_random_data(350)
        self.make_research_static_probability("simple321.txt")
        self.RRIntervals = []
        self.generate_poisson_random_data(5, 1000)
        self.make_research_static_probability("poisson.txt")
        self.RRIntervals = []
        self.generate_random_data(1000)
        self.make_research_static_probability("random.txt")

    def amosov_research(self, prefix=''):
        print 'Importing...'
        self.import_amosov_data('input.xls')
        print 'Exporting intervls...'
        self.export_intervals()
        print 'Making interval plot...'
        self.make_intervals_plot(prefix + 'intervals')
        print 'Making distribution histogram...'
        self.make_distribution_histogram(prefix + 'histogram')

    def amosov_all_data_research(self):
        import os

        for fileName in os.listdir('./amosov'):
            self.RRIntervals = []
            self.import_amosov_data('./amosov/' + fileName)
            self.filter_intervals()
            # self.export_intervals(fileName[:-4])
            # self.make_intervals_plot(fileName[:-4] + 'intervals')
            # self.make_distribution_histogram(fileName[:-4] + 'histogram')
            self.make_network_with_static_probability(0.)
            self.calculate_graph_parametrs(fileName)

            # self.make_research_static_probability(prefix=fileName)


Test = TVG()
Test.amosov_all_data_research()
# Test.amosov_research()

# Test.generate_simple321_random_data(10)
# Test.generate_poisson_random_data(10, 100)
# print Test.RRIntervals
# Test.make_network_with_static_probability(1)
# Test.make_graphic("123")
# print Test.calculate_graph_parametrs()
# print Test.calculate_average_degree()
