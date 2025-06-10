from NACHTT_utils import Plotter, Processor
plotter = Plotter()
processor = Processor()

import xarray as xr



# Load NACHTT Campaign Data
nachtt_nc_file = (
    "/uufs/chpc.utah.edu/common/home/haskins-group1/data/Campaign_Data/Raw_Data/"
    "NACHTT_2011/data/elevator/NACHTT_2011_1min_Merged.nc")
nachtt_nc = xr.open_dataset(nachtt_nc_file)


# Load base run model data
base_nc_file = (
    "/uufs/chpc.utah.edu/common/home/haskins-group1/users/jbail/GEOSChem/GC_RunDirs/gc_2x25_nacht2011_base/"
    "OutputDir/Plane_Logs/planelog_concat_20110217_20110314.nc")
base_nc = xr.open_dataset(base_nc_file)


# Plot NACHTT diurnal variation in following:
    # ClNO2
ClNO2_diurnal_fig = '../figures/ClNO2_diurnal.png'
plotter.plot_diurnal_variation(nachtt_nc, 'ClNO2_pptv', scale_factor=1, time_var='time', local_offset=-7, ylabel='Observed (pptv)',
                               second_dataset=base_nc, second_variable_name='ClNO2', second_scale_factor=1e12, second_time_var='time_UTC', second_ylabel='Modeled (pptv)',
                               primary_ylim=(-0.2,50), secondary_ylim=(-0.2,10), fig_save_path=ClNO2_diurnal_fig)



# Plot NACHTT full time series for following species and identify peaks
    # ClNO2, N2O5, O3, NO2, NO, NO3, pCl, pNO3, Cl2, HONO, HCl, Temp, Pressure, wind
plotter.plot_time_series(nachtt_nc, 'ClNO2_pptv', scale_factor=1, time_var='time', local_offset=-7, ylabel='Observed (pptv)', average_interval='30min')



stats, peaks = processor.get_peak_n_values(nachtt_nc, 'ClNO2_pptv', average_interval='30min')
peak_times = peaks.time
peak_xlims = processor.get_xlim_from_peaks(peak_times, hours_before=12, hours_after=12)

for xlim in peak_xlims:
    plotter.plot_time_series(
        dataset=nachtt_nc,
        variable='ClNO2_pptv',
        xlim=xlim,
        ylabel='Observed (pptv)',
        average_interval='30min'
    )





