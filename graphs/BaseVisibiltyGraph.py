# -*- coding: utf-8 -*-

import networkx as nx
import igraph


class BaseVisibilityGraph(nx.Graph):

    def __init__(self):
        super(BaseVisibilityGraph, self).__init__()
        self.timeSeries = []

    def get_series(self):
        return self.timeSeries

    def set_series(self, series):
        self.timeSeries = series

    def average_degree(self, weight=None):
        number_of_nodes = self.number_of_nodes()
        sum_of_degree = sum(self.degree(weight=weight).values())
        average_degree = float(sum_of_degree) / float(number_of_nodes)
        return average_degree

    def get_params(self, params=None, weight=None):
        if params is None:
            params = ["clustering", "assortativity", "average_degree", "nodes", "edges", "short_path",
                      "degree_distribution"]

        result = {}

        if "clustering" in params:
            try:
                result["clustering"] = nx.average_clustering(self, weight=weight)
            except:
                pass
        if "assortativity" in params:
            try:
                result["assortativity"] = nx.degree_assortativity_coefficient(self, weight=weight)
            except:
                pass
        if "nodes" in params:
            try:
                result["nodes"] = self.number_of_nodes()
            except:
                pass
        if "edges" in params:
            try:
                result["edges"] = self.number_of_edges()
            except:
                pass
        if "average_degree" in params:
            try:
                result["average_degree"] = self.average_degree(weight=weight)
            except:
                pass
        if "short_path" in params:
            try:
                tmp_graph = igraph.Graph()
                tmp_graph.add_vertices(self.nodes())
                tmp_graph.add_edges(self.edges())

                result["short_path"] = tmp_graph.average_path_length()
            except:
                pass
        if "degree_distribution" in params:
            try:
                degree_list = self.degree(weight=weight).values()
                degree_len = float(len(degree_list))
                degrees = dict((i, degree_list.count(i)/degree_len) for i in set(degree_list))
                result["degree_distribution"] = degrees
            except:
                pass

        return result