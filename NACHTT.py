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
plotter.plot_diurnal_variation(nachtt_nc, 'ClNO2_pptv', local_offset=-7, ylabel='ClNO₂ (ppbv)')


