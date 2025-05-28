# simulation.py
import numpy as np
from datacenter_config import CONFIG

class HPCSimulation:
    def __init__(self, hpp, metrics):
        self.hpp = hpp
        self.metrics = metrics
        self.time_steps = CONFIG.time_params['total_steps']

    def generate_hpc_load(self):
        base_load = CONFIG.hpc_load['base_load']
        time = np.linspace(0, 24, self.time_steps)
        load_variation = (np.sin(2 * np.pi * (time / 24 - 0.25)) *
                          CONFIG.hpc_load['variation'] * base_load)
        noise = np.random.normal(0, 0.05 * base_load, self.time_steps)
        return np.clip(base_load + load_variation + noise,
                       base_load * CONFIG.hpc_load['min_factor'], None)

    def run(self):
        load_profile = self.generate_hpc_load()
        dispatch_results = []

        for step in range(self.time_steps):
            dispatch = self.hpp.optimize_dispatch(load_profile[step], step)
            self.metrics.update(dispatch)
            dispatch_results.append(dispatch)

        return dispatch_results
