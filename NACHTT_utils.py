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