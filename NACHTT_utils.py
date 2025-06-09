import pandas as pd
import matplotlib.pyplot as plt

class Plotter:
    def __init__(self):
        pass
    

    def plot_diurnal_variation(self, dataset, variable_name, time_var='time', local_offset=0, ylabel=None):
        """
        Plots the diurnal variation of a specified variable from an xarray dataset.
        
        Parameters:
        - dataset: xarray dataset containing the data.
        - variable_name: str, name of the variable to plot (e.g., 'ClNO2_ppbv').
        - time_var: str, name of the time variable in the dataset (default: 'time').
        - local_offset: int, number of hours to shift from UTC to local time (default: 0).
        - ylabel: str, optional custom y-axis label.
        """
        # Extract time and variable data
        time = pd.to_datetime(dataset[time_var].values) + pd.to_timedelta(local_offset, unit='h')
        data = dataset[variable_name].values
    
        # Create DataFrame
        df = pd.DataFrame({'time': time, variable_name: data})
    
        # Extract hour of the day
        df['hour'] = df['time'].dt.hour
    
        # Group by hour and calculate mean and std
        diurnal_stats = df.groupby('hour')[variable_name].agg(['mean', 'std'])
    
        # Plot
        plt.figure(figsize=(10, 6))
        plt.errorbar(diurnal_stats.index, diurnal_stats['mean'], yerr=diurnal_stats['std'], fmt='o-', capsize=3)
        plt.xlabel('Hour of Day (Local Time)' if local_offset != 0 else 'Hour of Day (UTC)')
        plt.ylabel(ylabel if ylabel else f'{variable_name}')
        plt.title(f'Diurnal Variation of {variable_name}')
        plt.grid(True)
        plt.xticks(range(0, 24))
        plt.show()
