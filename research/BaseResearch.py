import os
import cPickle as pickle
import networkx as nx
import re

import utils.TimeSeriesGenerator as ts
import utils.PlotParameters as pp
import graphs.GraphFactory as gf
import utils.DataImport as di


class BaseResearch(object):
    def __init__(self, network_type=None):
        self.ROOT_DIRECTORY = ""
        self.DB_DIRECTORY = "data"
        self.RESULT_DIRECTORY = "results"
        self.NETWORK_DIRECTORY = "networks"
        self.PARAMS_DIRECTORY = "params"
        self.GRAPHICS_DIRECTORY = "graphics"
        self.NETWORK_TYPE = network_type

        self.NUMBER_OF_NODES_IN_TS = 1000
        self.CALCULATING_TS = ["periodic", "static", "random", "poisson", "sinusoid"]

        self.CALCULATING_PARAMS = ["clustering", "assortativity", "average_degree", "nodes", "edges", "short_path",
                                   "degree_distribution"]
        self.PHYSIO_NET_DBS = ["afdb", "chfdb", "chf2db", "ltafdb", "mitdb", "nsr2db"]

    def create_networks_from_data(self):
        db = os.path.join(self.ROOT_DIRECTORY, self.DB_DIRECTORY)
        res = os.path.join(self.ROOT_DIRECTORY, self.RESULT_DIRECTORY, self.NETWORK_DIRECTORY, self.NETWORK_TYPE)

        for directory in self.PHYSIO_NET_DBS:
            data_dir_full_path = os.path.join(db, directory)
            result_dir_full_path = os.path.join(res, directory)
            try:
                os.makedirs(result_dir_full_path)
            except:
                pass

            files = next(os.walk(data_dir_full_path))[2]
            for kardio_file in files:
                time_series = di.import_from_file(os.path.join(data_dir_full_path, kardio_file))
                graph = gf.get_graph(self.NETWORK_TYPE, time_series)
                result_file_full_path = os.path.join(result_dir_full_path, self.NETWORK_TYPE + kardio_file[:-3] + "pck")
                result_file = open(result_file_full_path, 'wb')
                nx.write_gpickle(graph, result_file)
                result_file.close()

    def calculate_networks_params(self):
        start_dir = os.path.join(self.ROOT_DIRECTORY, self.RESULT_DIRECTORY, self.NETWORK_DIRECTORY, self.NETWORK_TYPE)
        param_dir = os.path.join(self.ROOT_DIRECTORY, self.RESULT_DIRECTORY, self.PARAMS_DIRECTORY, self.NETWORK_TYPE)

        for db_dir in self.PHYSIO_NET_DBS:
            output_dir = os.path.join(param_dir, db_dir)
            try:
                os.makedirs(output_dir)
            except:
                pass

            files = next(os.walk(os.path.join(start_dir, db_dir)))[2]
            for graph_file in files:
                graph_file_full_path = os.path.join(start_dir, db_dir, graph_file)
                graph = nx.read_gpickle(open(graph_file_full_path, 'rb'))
                new_params = graph.get_params(self.CALCULATING_PARAMS)

                param_file_path = os.path.join(output_dir, graph_file)
                if os.path.isfile(param_file_path):
                    with open(param_file_path, 'rb') as fr:
                        old_param = pickle.load(fr)
                    merged_params = old_param.copy()
                    merged_params.update(new_params)
                else:
                    merged_params = new_params
                with open(param_file_path, 'wb') as fw:
                    pickle.dump(merged_params, fw)

    def get_all_params(self):
        base_param_dir = os.path.join(self.ROOT_DIRECTORY, self.RESULT_DIRECTORY, self.PARAMS_DIRECTORY)
        network_types_dirs = next(os.walk(base_param_dir))[1]
        data = {}
        for network_type in network_types_dirs:
            for db_dir in self.PHYSIO_NET_DBS:
                data[network_type] = {}
                param_dir_path = os.path.join(base_param_dir, network_type, db_dir)
                data[network_type][db_dir] = self.get_params_from_dir(param_dir_path)

        return data

    def make_all_db_graph(self, x_param, y_param):
        result_dir = os.path.join(self.ROOT_DIRECTORY, self.RESULT_DIRECTORY)
        param_dir = os.path.join(result_dir, self.PARAMS_DIRECTORY, self.NETWORK_TYPE)
        graphics_dir = os.path.join(result_dir, self.GRAPHICS_DIRECTORY, self.NETWORK_TYPE)

        for db_dir in self.PHYSIO_NET_DBS:
            color = pp.get_color_by_db(db_dir)
            output_dir = os.path.join(graphics_dir, db_dir)
            try:
                os.makedirs(output_dir)
            except:
                pass

            path = os.path.join(param_dir, db_dir)
            files = next(os.walk(path))[2]
            for kardio_file in files:
                kardio_file_full_path = os.path.join(path, kardio_file)
                with open(kardio_file_full_path, 'rb') as fr:
                    param = pickle.load(fr)

                pp.add_xy_plot(param[x_param], param[y_param], color=color)
        pp.save_plots("t.png")

    def get_time_series(self, ts_name):
        if ts_name == "periodic":
            return ts.generate_periodic(self.NUMBER_OF_NODES_IN_TS)
        elif ts_name == "static":
            return ts.generate_static(self.NUMBER_OF_NODES_IN_TS)
        elif ts_name == "random":
            return ts.generate_random(self.NUMBER_OF_NODES_IN_TS)
        elif ts_name == "poisson":
            return ts.generate_poisson(self.NUMBER_OF_NODES_IN_TS)
        elif ts_name == "sinusoid":
            return ts.generate_sinusoid(self.NUMBER_OF_NODES_IN_TS)

    @staticmethod
    def natural_sort_files(files):
        return sorted(files, key=lambda xf: float(xf[:-4]))

    @staticmethod
    def get_params_from_dir(path):
        params = []
        files = next(os.walk(path))[2]
        for kardio_file in files:
            kardio_file_full_path = os.path.join(path, kardio_file)
            with open(kardio_file_full_path, 'rb') as fr:
                param = pickle.load(fr)
            params.append(param)
        return params

    @staticmethod
    def get_params_from_file(path):
        with open(path, 'rb') as fr:
            param = pickle.load(fr)
        return param

    @staticmethod
    def get_param_from_list(param, param_list):
        try:
            result = [d[param] for d in param_list]
        except:
            result = []
        return result
