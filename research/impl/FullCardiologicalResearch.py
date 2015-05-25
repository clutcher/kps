# coding=utf-8

import os
import networkx as nx
import matplotlib.pyplot as plt
from graphs import GraphFactory
from utils import TimeSeriesGenerator as TS


class Research(object):

    def __init__(self, root='', db='data', result='research', network_type="CWG"):
        self.ROOT_DIRECTORY = root
        self.DB_DIRECTORY = db
        self.RESULT_DIRECTORY = result
        self.network_type = network_type

    def research_complex_kardiological_data(self):

        def create_networks_from_data():
            dirs = next(os.walk(self.ROOT_DIRECTORY + self.DB_DIRECTORY))[1]

            for directory in dirs:
                data_dir_full_path = os.path.join(self.ROOT_DIRECTORY + self.DB_DIRECTORY, directory)
                result_dir_full_path = os.path.join(self.ROOT_DIRECTORY + self.RESULT_DIRECTORY, directory)
                files = next(os.walk(data_dir_full_path))[2]

                for kardio_file in files:
                    data_file = open(os.path.join(data_dir_full_path, kardio_file))
                    time_series = data_file.read().split('\n')
                    data_file.close()

                    time_series.remove('')
                    time_series = [float(i) for i in time_series]

                    graph = GraphFactory.get_graph(self.network_type, time_series)

                    try:
                        os.makedirs(result_dir_full_path)
                    except:
                        pass
                    result_file_full_path = os.path.join(result_dir_full_path,
                                                         self.network_type + kardio_file)

                    result_file = open(result_file_full_path, 'wb')
                    nx.write_gpickle(graph, result_file)
                    print "1"


        def calculate_network_params():
            start_dir = self.ROOT_DIRECTORY + self.RESULT_DIRECTORY
            dirs = next(os.walk(start_dir))[1]
            for db_dir in dirs:
                case_dir = next(os.walk(os.path.join(start_dir, db_dir)))[1]
                if len(case_dir) != 0:
                    for dir in case_dir:
                        files = next(os.walk(os.path.join(start_dir, db_dir, dir)))[2]
                        params = []
                        for kardio_file in files:
                            kardio_file_full_path = os.path.join(start_dir, db_dir, dir, kardio_file)
                            f = open(kardio_file_full_path, 'rb')
                            graph = nx.read_gpickle(f)
                            params.append(nx.average_clustering(graph, weight="weight"))
                        fw = open(os.path.join(start_dir, db_dir, dir + "clustering.txt"), "w")
                        for param in params:
                            fw.write("%s\n" % param)
                else:
                    params = []
                    files = next(os.walk(os.path.join(start_dir, db_dir)))[2]
                    for kardio_file in files:
                        kardio_file_full_path = os.path.join(start_dir, db_dir, kardio_file)
                        f = open(kardio_file_full_path, 'rb')
                        graph = nx.read_gpickle(f)
                        params.append(nx.degree_assortativity_coefficient(graph, weight="weight"))
                    try:
                        os.makedirs(os.path.join(start_dir, "assort"))
                    except:
                        pass
                    fw = open(os.path.join(start_dir, "assort", db_dir + ".txt"), "w")
                    for param in params:
                        fw.write("%s\n" % param)

        # create_networks_from_data()
        calculate_network_params()
        # self.make_params_graphic()

    def make_params_graphic(self, file_name='graph.png'):

        start_dir = "params/wavdeg"
        start_dir2= "params/node"
        files = next(os.walk(start_dir))[2]

        for i, file in enumerate(files):
            cluster = TS.import_from_file(os.path.join(start_dir, file))
            node = TS.import_from_file(os.path.join(start_dir2, file))
            plt.plot(node, cluster, 'x', label=file[:-4])

        # plt.xlim([-1, 8])
        plt.legend()
        plt.savefig(os.path.join("params", "wavdeg_node.png"))
        plt.close('all')

r = Research()
r.research_complex_kardiological_data()