# -*- coding: utf-8 -*-

from graphs.BaseVisibiltyGraph import BaseVisibilityGraph


class CWG(BaseVisibilityGraph):
    """
    Compactified Weighted Graph
    """

    def create_network_from_series(self):
        # Before init node data was without set on self.timeSeries
        init_node_data = dict((i, self.timeSeries.count(i)) for i in set(self.timeSeries))
        for node, occurrence in init_node_data.items():
            self.add_node(node, occurrence=occurrence)
        if len(init_node_data) > 1:
            for i, value in enumerate(self.timeSeries[:-1]):
                if self.has_edge(self.timeSeries[i], self.timeSeries[i + 1]):
                    self.edge[self.timeSeries[i]][self.timeSeries[i + 1]]["weight"] += 1
                else:
                    self.add_edge(self.timeSeries[i], self.timeSeries[i + 1], weight=1)