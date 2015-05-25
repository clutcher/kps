# -*- coding: utf-8 -*-

from graphs.BaseVisibiltyGraph import BaseVisibilityGraph


class LEG(BaseVisibilityGraph):
    """
    Line Equal Graph
    """

    def create_network_from_series(self):
        self.add_node(0)
        for i in xrange(1, len(self.timeSeries), 1):
            self.add_node(i)
            self.add_edge(i - 1, i)
            previous_index = self.__find_previous_index__(i)
            if previous_index != -1:
                self.add_edge(previous_index, i)

    def __find_previous_index__(self, start_index):
        for i in reversed(xrange(start_index)):
            if self.timeSeries[i] == self.timeSeries[start_index]:
                return i
        return -1
