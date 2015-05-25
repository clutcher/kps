# -*- coding: utf-8 -*-

from graphs.BaseVisibiltyGraph import BaseVisibilityGraph


class TVG(BaseVisibilityGraph):
    """
    Tunneling Visibility Graph
    """

    def create_network_from_series(self, probability=0.):
        import random

        edge_list = []
        number_of_intervals = len(self.timeSeries)
        for i in xrange(number_of_intervals):
            delta = self.timeSeries[i]
            j = i + 1
            tunneling_flag = False
            while j < number_of_intervals:
                if self.timeSeries[i] > self.timeSeries[j]:
                    if 0 < (self.timeSeries[i] - self.timeSeries[j]) <= delta:
                        delta = self.timeSeries[i] - self.timeSeries[j]
                        edge = (i, j)
                        edge_list.append(edge)
                else:
                    edge = (i, j)
                    edge_list.append(edge)
                    if not tunneling_flag and (random.random() <= probability):
                        tunneling_flag = True
                    else:
                        tunneling_flag = False
                        break

                j += 1

        self.add_edges_from(edge_list)