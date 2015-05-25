# -*- coding: utf-8 -*-

from graphs.BaseVisibiltyGraph import BaseVisibilityGraph


class HVG(BaseVisibilityGraph):
    """
    Horizontal Visibility Graph
    """

    def create_network_from_series(self):
        edge_list = []
        number_of_elements = len(self.timeSeries)
        for i in xrange(number_of_elements):
            delta = self.timeSeries[i]
            self.add_node(i, occurrence=self.timeSeries[i])
            j = i + 1
            while j < number_of_elements:
                if self.timeSeries[i] > self.timeSeries[j]:
                    if 0 < (self.timeSeries[i] - self.timeSeries[j]) <= delta:
                        delta = self.timeSeries[i] - self.timeSeries[j]
                        edge = (i, j)
                        edge_list.append(edge)
                else:
                    edge = (i, j)
                    edge_list.append(edge)
                    break
                j += 1

        self.add_edges_from(edge_list)
