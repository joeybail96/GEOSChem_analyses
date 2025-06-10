import pandas as pd
import matplotlib.pyplot as plt

class Plotter:
    def __init__(self):
        pass
    

    def plot_diurnal_variation(self, dataset, variable_name, scale_factor=1, time_var='time', local_offset=0, ylabel=None, p_color='blue',
                               second_dataset=None, second_variable_name=None, second_scale_factor=1, second_time_var='time_UTC', second_ylabel=None, second_p_color='red',
                               primary_ylim=None, secondary_ylim=None, fig_save_path=None):
        """
        Plots the diurnal variation of a specified variable from an xarray dataset.
        Optionally plots a second dataset on a secondary y-axis.
        """
        # Primary dataset processing
        time = pd.to_datetime(dataset[time_var].values) + pd.to_timedelta(local_offset, unit='h')
        data = dataset[variable_name].values * scale_factor
    
        df = pd.DataFrame({'time': time, variable_name: data})
        df['hour'] = df['time'].dt.hour
        diurnal_stats = df.groupby('hour')[variable_name].mean()
    
        # Plot
        fig, ax1 = plt.subplots(figsize=(10, 6))
        ax1.plot(diurnal_stats.index, diurnal_stats.values, 'o-', label=variable_name, color=p_color)
        ax1.set_xlabel('Hour of Day (Local Time)' if local_offset != 0 else 'Hour of Day (UTC)')
        ax1.set_ylabel(ylabel if ylabel else f'{variable_name}', color=p_color)
        ax1.tick_params(axis='y', labelcolor=p_color, color=p_color)
        ax1.spines['left'].set_color(p_color)
        ax1.set_xticks(range(0, 24))
        ax1.grid(False)
    
        if primary_ylim is not None:
            ax1.set_ylim(primary_ylim)
    
        if second_dataset is not None and second_variable_name is not None:
            time2 = pd.to_datetime(second_dataset[second_time_var].values) + pd.to_timedelta(local_offset, unit='h')
            data2 = second_dataset[second_variable_name].values * second_scale_factor
    
            df2 = pd.DataFrame({'time': time2, second_variable_name: data2})
            df2['hour'] = df2['time'].dt.hour
            diurnal_stats2 = df2.groupby('hour')[second_variable_name].mean()
    
            ax2 = ax1.twinx()
            ax2.plot(diurnal_stats2.index, diurnal_stats2.values, 's-', label=second_variable_name, color=second_p_color)
            ax2.set_ylabel(second_ylabel if second_ylabel else f'{second_variable_name}', color=second_p_color)
            ax2.tick_params(axis='y', labelcolor=second_p_color, color=second_p_color)
            ax2.spines['left'].set_color(p_color)
            ax2.spines['right'].set_color(second_p_color)
    
            if secondary_ylim is not None:
                ax2.set_ylim(secondary_ylim)
    
        plt.title(f'{variable_name}')
    
        if fig_save_path is not None:
            plt.savefig(fig_save_path, dpi=300, bbox_inches='tight')
            plt.close(fig)  # Close the figure explicitly to prevent auto-display
        else:
            plt.show()
            
            
            
    def plot_time_series(self, dataset, variable, scale_factor=1, time_var='time', local_offset=0, ylabel='Observed', average_interval=None, xlim=None, ylim=None):
        """
        Creates a time series plot from the given dataset, with optional averaging.
    
        Parameters:
        - dataset: Input data structure (xarray Dataset, pandas DataFrame, or similar) containing time and variable data.
        - variable: Name of the variable to plot.
        - scale_factor: Value to scale the variable (default is 1, no scaling).
        - time_var: Name of the time variable in the dataset.
        - local_offset: Time zone offset in hours to apply to the time variable.
        - ylabel: Label for the y-axis.
        - average_interval: Pandas offset string (e.g., '10min', '1H') for averaging (optional).
        """
        import pandas as pd
        import matplotlib.pyplot as plt
    
        # Extract time and variable, apply scale factor
        time = pd.to_datetime(dataset[time_var].values) + pd.to_timedelta(local_offset, unit='h')
        data = dataset[variable].values * scale_factor
    
        # Create a pandas Series for easy resampling if averaging is requested
        series = pd.Series(data, index=time)
    
        if average_interval:
            # Resample and average
            series = series.resample(average_interval).mean()
    
        # Create the plot
        plt.figure(figsize=(12, 6))
        plt.plot(series.index, series.values, label=variable, color='tab:blue')
        
        # Apply x-axis limits if provided
        if xlim:
            plt.xlim(pd.to_datetime(xlim[0]), pd.to_datetime(xlim[1]))
            
        if ylim:
            plt.ylim(pd.to_datetime(ylim[0]), pd.to_datetime(ylim[1]))
            
        plt.xlabel('Time')
        plt.ylabel(ylabel)
        plt.title(f'Time Series of {variable}' + (f' (Averaged: {average_interval})' if average_interval else ''))
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()
        
        
        
class Processor:
    def __init__(self):
        pass

    def get_peak_n_values(self, dataset, var_name, average_interval=None, n=5, time_var='time', local_offset=0):
        """
        Returns a DataFrame of the top n highest points (time and value) of a variable in the dataset,
        optionally averaging by a specified pandas offset string interval.
        Also returns summary statistics of the entire dataset variable (after averaging if applied).

        Parameters:
        - dataset: xarray Dataset loaded from a NetCDF file.
        - var_name: Name of the variable to analyze.
        - average_interval: pandas offset string for resampling and averaging (e.g., '10min', '1H'). If None, no averaging.
        - n: Number of top points to return (default 5).
        - time_var: Name of the time coordinate variable (default 'time').
        - local_offset: Timezone offset in hours to apply to the time coordinate (default 0).

        Returns:
        - summary_stats: dict with keys ['mean', 'median', 'std', 'min', 'max'] for the entire data
        - top_n_df: pandas DataFrame with columns ['time', 'value'] for the top n points
        """
        # Convert time coordinate to pandas datetime with local offset
        time = pd.to_datetime(dataset[time_var].values) + pd.to_timedelta(local_offset, unit='h')
        data = dataset[var_name].values

        # Create pandas Series for easy resampling and handling time index
        series = pd.Series(data, index=time)

        if average_interval:
            # Resample with mean, ignoring NaNs where possible
            series = series.resample(average_interval).mean().dropna()

        # Compute summary statistics on the whole series
        summary_stats = {
            'mean': series.mean(),
            'median': series.median(),
            'std': series.std(),
            'min': series.min(),
            'max': series.max()
        }

        # Get top n values and corresponding times
        top_n = series.nlargest(n)
        top_n_df = pd.DataFrame({'time': top_n.index, 'value': top_n.values}).reset_index(drop=True)

        return summary_stats, top_n_df
    
    
    def get_xlim_from_peaks(self, peak_times, hours_before=12, hours_after=12):
        """
        Given a DataFrame with a 'time' column, return a list of (start, end) tuples
        where start = peak_time - hours_before, end = peak_time + hours_after.
        """
        return [(t - pd.Timedelta(hours=hours_before), t + pd.Timedelta(hours=hours_after)) for t in peak_times]
    
    
    
    
    