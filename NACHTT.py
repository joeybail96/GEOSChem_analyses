from NACHTT_utils import Plotter
plotter = Plotter()

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


Cl2_diurnal_fig = '../figures/Cl2_diurnal.png'
plotter.plot_diurnal_variation(nachtt_nc, 'Cl2_pptv', scale_factor=1, time_var='time', local_offset=-7, ylabel='Observed (pptv)',
                               second_dataset=base_nc, second_variable_name='Cl2', second_scale_factor=1e12, second_time_var='time_UTC', second_ylabel='Modeled (pptv)',
                               primary_ylim=(-5.99,5.99), secondary_ylim=(-0.02, 0.52), fig_save_path=Cl2_diurnal_fig)


Cl_diurnal_fig = '../figures/Cl_diurnal.png'
plotter.plot_diurnal_variation(nachtt_nc, 'AMS_pCl_ugm3', scale_factor=1, time_var='time', local_offset=-7, ylabel='Observed (ug m^-3)',
                               second_dataset=base_nc, second_variable_name='Cl', second_scale_factor=1, second_time_var='time_UTC', second_ylabel='Modeled (ug m^-3)',
                               primary_ylim=(-0.01,0.1), secondary_ylim=(-0.01,0.1), fig_save_path=Cl_diurnal_fig)