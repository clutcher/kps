import random
import os
import matplotlib.pyplot as plt
from research.BaseResearch import BaseResearch


class DBResearch(BaseResearch):
    def make_research(self):
        result_dir = os.path.join(self.ROOT_DIRECTORY, self.RESULT_DIRECTORY)
        param_dir = os.path.join(result_dir, self.PARAMS_DIRECTORY, self.NETWORK_TYPE)
        graphics_dir = os.path.join(result_dir, self.GRAPHICS_DIRECTORY, self.NETWORK_TYPE)

        dirs = next(os.walk(param_dir))[1]
        i = 0
        for db_dir in dirs:
            color = "#"+str(random.randint(111111,999999))
            print db_dir
            print color
            output_dir = os.path.join(graphics_dir, db_dir)
            try:
                os.makedirs(output_dir)
            except:
                pass

            db_params = self.get_params_from_dir(os.path.join(param_dir, db_dir))
            for calc_param in self.CALCULATING_PARAMS:
                pm = self.get_param_from_list(calc_param, db_params)
            for tmp in pm:
                plt.plot(tmp.keys(), tmp.values(), "x", color=color)
            i += 1
        # plt.legend()
        plt.xscale("log")
        plt.yscale("log")
        plt.savefig(os.path.join(graphics_dir, self.CALCULATING_PARAMS[0] + ".png"))
