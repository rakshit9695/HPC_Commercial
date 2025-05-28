# metrics.py
import numpy as np

class HPPMetrics:
    def __init__(self, config):
        self.config = config
        self.data = {
            'renewable_usage': [],
            'grid_import': [],
            'curtailment': [],
            'soc': [],
            'costs': []
        }

    def update(self, dispatch_result):
        total_supplied = (dispatch_result['wind_used'] +
                          dispatch_result['solar_used'] +
                          dispatch_result['grid'])
        renewable_share = 0.0
        if total_supplied > 0:
            renewable_share = (dispatch_result['wind_used'] + dispatch_result['solar_used']) / total_supplied

        self.data['renewable_usage'].append(renewable_share)
        self.data['grid_import'].append(dispatch_result['grid'])
        self.data['curtailment'].append(dispatch_result['wind_curtail'] + dispatch_result['solar_curtail'])
        self.data['soc'].append(dispatch_result['soc'])
        self.data['costs'].append(dispatch_result['grid'] * self.config.grid['energy_price'] * self.config.time_params['time_step_mins'] / 60.0 * 1000)

    def finalize_metrics(self):
        return {
            'renewable_penetration': np.mean(self.data['renewable_usage']),
            'total_grid_import': np.sum(self.data['grid_import']) * self.config.time_params['time_step_mins'] / 60.0,
            'total_curtailment': np.sum(self.data['curtailment']) * self.config.time_params['time_step_mins'] / 60.0,
            'total_cost': np.sum(self.data['costs']),
            'avg_soc': np.mean(self.data['soc'])
        }
