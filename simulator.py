import pandas as pd
import numpy as np
from config import Config
import logging

log = logging.getLogger('sim')

class Simulator():
    def __init__(self, cfg):
        self.df_bd = pd.read_csv(cfg['bandwidth_path'])
        self.df_t = pd.read_json(cfg['table_path'])
        self.fps = cfg['fps_target']
        self.mode = cfg['mode']

    def opt_acc_latency_server_only(self, bd):
        max_acc = 0
        final_latency = 0
        latency_bound = 1000 / self.fps
        for index, row in self.df_t.iterrows():
            total_latency = row['size'] / bd * 1000 + row['1st_inf'] \
                            + row['encoding_latency'] + row['decoding_latency']
            if  total_latency < latency_bound and row['1st_acc'] > max_acc:
                max_acc = row['1st_acc']
                final_latency = total_latency
        return max_acc, final_latency

    def opt_acc_latency_mixed(self, bd):
        max_acc = 0
        final_latency = 0
        latency_bound = 1000 / self.fps
        for index, row in self.df_t.iterrows():
            total_latency = row['size'] / bd * 1000 + row['1st_inf'] \
                            + row['encoding_latency'] + row['decoding_latency'] + row['2nd_inf']
            if total_latency<latency_bound and row['2nd_acc'] > max_acc:
                max_acc = row['2nd_acc']
                final_latency = total_latency
        return max_acc, final_latency

    def sim_acc(self):
        results = []
        bds = self.df_bd['bandwidth']
        for bd in bds:
            if self.mode == 0:
                acc = self.opt_acc_latency_server_only(bd)
            elif self.mode == 1:
                acc = self.opt_acc_latency_edge_only(bd)
            elif self.mode == 2:
                acc = self.opt_acc_latency_mixed(bd)
            log.info("bandwidth: "+str(bd))
            log.info("accuracy: "+str(acc))
            results.append(acc)
        return np.array(results)