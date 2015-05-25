import os
import numpy as np
import cPickle as pickle

import networkx as nx

import graphs.GraphFactory as gf
import utils.PlotParameters as pp
import utils.DataImport as di

from research.BaseResearch import BaseResearch


class TVGResearch(BaseResearch):
    def __init__(self, p_interval=None):
        super(TVGResearch, self).__init__()
        self.NETWORK_TYPE = "TVG"
        self.NUMBER_OF_NODES_IN_TS = 1000
        self.CALCULATING_PARAMS = ["clustering", "assortativity", "average_degree", "nodes", "edges", "short_path"]
        if p_interval:
            self.P = p_interval
        else:
            self.P = np.arange(0, 1, 0.05)

    def create_networks_from_data(self):
        db = os.path.join(self.ROOT_DIRECTORY, self.DB_DIRECTORY)
        res = os.path.join(self.ROOT_DIRECTORY, self.RESULT_DIRECTORY, self.NETWORK_DIRECTORY, self.NETWORK_TYPE)

        for directory in self.PHYSIO_NET_DBS:
            data_dir_full_path = os.path.join(db, directory)

            files = next(os.walk(data_dir_full_path))[2]
            for kardio_file in files:
                time_series = di.import_from_file(os.path.join(data_dir_full_path, kardio_file))
                for p in self.P:
                    graph = gf.get_graph(self.NETWORK_TYPE)
                    graph.set_series(time_series)
                    graph.create_network_from_series(probability=p)

                    result_dir_full_path = os.path.join(res, directory, kardio_file[:-4])
                    try:
                        os.makedirs(result_dir_full_path)
                    except:
                        pass

                    result_file_full_path = os.path.join(result_dir_full_path, str(p) + ".pck")
                    result_file = open(result_file_full_path, 'wb')
                    nx.write_gpickle(graph, result_file)
                    result_file.close()

    def calculate_networks_params(self):
        start_dir = os.path.join(self.ROOT_DIRECTORY, self.RESULT_DIRECTORY, self.NETWORK_DIRECTORY, self.NETWORK_TYPE)
        param_dir = os.path.join(self.ROOT_DIRECTORY, self.RESULT_DIRECTORY, self.PARAMS_DIRECTORY, self.NETWORK_TYPE)

        for db_dir in self.PHYSIO_NET_DBS:

            dirs = next(os.walk(os.path.join(start_dir, db_dir)))[1]
            for graph_dir in dirs:
                p_dir = os.path.join(start_dir, db_dir, graph_dir)
                output_dir = os.path.join(param_dir, db_dir, graph_dir)
                try:
                    os.makedirs(output_dir)
                except:
                    pass

                graph_files = next(os.walk(p_dir))[2]
                for graph_file in graph_files:
                    graph_file_full_path = os.path.join(p_dir, graph_file)
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

    def make_canonical_research(self):
        result_dir = os.path.join(self.ROOT_DIRECTORY, self.RESULT_DIRECTORY, self.GRAPHICS_DIRECTORY,
                                  self.NETWORK_TYPE)
        x = np.arange(0, 1, 0.01)
        for ts_name in self.CALCULATING_TS:
            graph_params = []
            time_series = self.get_time_series(ts_name)
            for p in x:
                graph = gf.get_graph(self.NETWORK_TYPE, series=time_series)
                graph.create_network_from_series(probability=p)
                graph_params.append(graph.get_params(params=self.CALCULATING_PARAMS))

            for param in self.CALCULATING_PARAMS:
                try:
                    os.makedirs(os.path.join(result_dir, param))
                except:
                    pass
                y = self.get_param_from_list(param, graph_params)
                file_path = os.path.join(result_dir, param, ts_name + ".png")

                pp.make_xy_plot(x, y, full_path=file_path, labels=["p", param], log="log")

    def make_all_db_graph(self, x_param, y_param, labels=None):
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
            kardio_dirs = next(os.walk(path))[1]

            for kardio_dir in kardio_dirs:
                x = []
                y = []
                files = next(os.walk(os.path.join(path, kardio_dir)))[2]
                files = sorted(files, key=lambda xf: float(xf[:-4]))

                for param_file in files:
                    param_file_full_path = os.path.join(path, kardio_dir, param_file)
                    with open(param_file_full_path, 'rb') as fr:
                        param = pickle.load(fr)
                    # print param
                    if x_param == "p":
                        x.append(param_file[:-4])
                        y.append(param[y_param])
                    elif y_param == "p":
                        x.append(param[x_param])
                        y.append(param_file[:-4])
                    else:
                        x.append(param[x_param])
                        y.append(param[y_param])
                    pp.add_xy_plot(x, y, color=color, labels=labels)
        pp.save_plots("t.png")
