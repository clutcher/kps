# -*- coding: utf-8 -*-

from graphs.impl.HVG import HVG
from utils.Compactification import compactify


class CHVG(HVG):
    """
    Compactified Horizontal Visibility Graph
    """

    def create_network_from_series(self):
        super(CHVG, self).create_network_from_series()
        compact_graph = compactify(self, "occurrence")
        self.clear()
        self.add_nodes_from(compact_graph.nodes())
        self.add_edges_from(compact_graph.edges(data=True))