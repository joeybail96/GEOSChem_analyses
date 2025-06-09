import os
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
from datetime import datetime

# Directory containing the species concentration files
file_directory = '/uufs/chpc.utah.edu/common/home/haskins-group1/users/jbail/GEOSChem/GC_RunDirs/gc_2x25_nacht2011_base/OutputDir/'

# Create a folder for saving the figures if it doesn't exist
output_folder = '/uufs/chpc.utah.edu/common/home/haskins-group1/users/jbail/GEOSChem/scripting/plots'
os.makedirs(output_folder, exist_ok=True)

# List all files in the directory (assumes files are in .nc4 format)
file_list = [f for f in os.listdir(file_directory) if 'SpeciesConc' in f and f.endswith('.nc4')]

# Iterate through each file
for file_name in file_list:
    # Read the dataset
    ds = xr.open_dataset(os.path.join(file_directory, file_name))

    # Extract the variable (modify this to match your actual variable name)
    species_var = 'SpeciesConcVV_ClNO2'  # Replace with the appropriate variable name if needed
    mean_data = ds[species_var].mean(dim=['time', 'lev'])

    # Get the actual latitude and longitude edges from the dataset
    lons = ds['lon'].values
    lats = ds['lat'].values

    # Create a plot with PlateCarree projection
    fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})

    # Add geographic features
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.add_feature(cfeature.STATES, linestyle='-', linewidth=1)

    # Plot data
    pc = mean_data.plot(ax=ax, cmap='viridis', add_colorbar=False)

    # Add a horizontal colorbar
    cbar = plt.colorbar(pc, ax=ax, orientation='horizontal', pad=0.05)
    cbar.set_label('ClNO2 Concentration')

    # Define grid lines using actual GEOS-Chem grid boundaries
    lon_lines = np.arange(-180, 180, 2.5) + 1.25  # Round to avoid floating-point precision issues
    lat_lines = np.arange(-90, 90, 2) + 1

    # Add gridlines to match GEOS-Chem grid boxes
    ax.set_xticks(lon_lines, crs=ccrs.PlateCarree())
    ax.set_yticks(lat_lines, crs=ccrs.PlateCarree())
    ax.grid(visible=True, color='white', linestyle='-', linewidth=0.5, alpha=0.3)

    ax.set_xticklabels([])
    ax.set_yticklabels([])

    ax.set_extent([-125, -70, 20, 47])  # Keep the extent as you requested

    # Extract the date and species concentration from the file name (modify based on your file naming convention)
    date_str = file_name.split('.')[2]  # Assuming date is the second part of the filename
    date_obj = datetime.strptime(date_str, '%Y%m%d_%H%Mz')  # Adjust format as needed
    formatted_date = date_obj.strftime('%Y-%m-%d')

    # Create the output filename
    output_file = os.path.join(output_folder, f"{formatted_date}_{species_var}.png")

    # Save the plot
    plt.savefig(output_file, dpi=300)
    plt.close()

    print(f"Saved plot for {file_name} to {output_file}")
