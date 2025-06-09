import os
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cartf
import numpy as np
from matplotlib.patches import Circle


def plot_total_dust_emissions_binary(ds, variables, bounding_box, output_png_path):
    fig = plt.figure(figsize=(16, 12))
    ax = plt.axes(projection=ccrs.PlateCarree())

    lon_min, lon_max, lat_min, lat_max = bounding_box
    ax.set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree())

    ax.coastlines()
    ax.add_feature(cartf.BORDERS)
    ax.add_feature(cartf.STATES, edgecolor='white', linestyle=':', linewidth=1)
    ax.add_feature(cartf.LAND, edgecolor='black')
    ax.add_feature(cartf.OCEAN)

    # === Gridlines matching cell resolution ===
    gl = ax.gridlines(draw_labels=True, alpha=0.5)
    gl.top_labels = False
    gl.right_labels = False
    gl.xlabel_style = {"size": 12}
    gl.ylabel_style = {"size": 12}
    lon_offset = 0.625 / 2
    lat_offset = 0.5 / 2
    gl.xlocator = plt.FixedLocator(np.arange(-180 + lon_offset, 180, 0.625))
    gl.ylocator = plt.FixedLocator(np.arange(-90 + lat_offset, 90, 0.5))

    # === Emissions Mask ===
    total_emissions = sum(ds[var].max(dim="time") for var in variables)
    binary_mask = (total_emissions > 0).astype(int)

    lon2d, lat2d = np.meshgrid(ds.lon.values, ds.lat.values)

    mesh = ax.pcolormesh(lon2d, lat2d, binary_mask,
                         cmap='gray_r', vmin=0, vmax=1, transform=ccrs.PlateCarree())

    # === Add red circle ===
    circle_lon = -109.7
    circle_lat = 37.18
    circle_radius_deg = 0.25  # Approximate degrees for ~300km (adjust as needed)
    circle = Circle((circle_lon, circle_lat), radius=circle_radius_deg,
                    transform=ccrs.PlateCarree(), edgecolor='red', facecolor='none', linewidth=3)
    ax.add_patch(circle)

    plt.title(f"Dust Emission Presence (DST1–DST4)\n{str(ds.time.values[0])[:13]}", fontsize=20, pad=10)
    plt.savefig(output_png_path, bbox_inches='tight', dpi=300)
    plt.show()
    plt.close()

# === Loop through all .nc files and generate binary emission maps ===
folder_path = '/uufs/chpc.utah.edu/common/home/haskins-group1/data/ExtData/HEMCO/OFFLINE_DUST/v2021-08/0.5x0.625/2011/03/'
output_folder = '/uufs/chpc.utah.edu/common/home/haskins-group1/users/jbail/GEOSChem/GEOSChem_analysis/my_scripts/dust/'

emission_vars = ['EMIS_DST1', 'EMIS_DST2', 'EMIS_DST3', 'EMIS_DST4']
bounding_box = (-130, -60, 20, 55)

for filename in os.listdir(folder_path):
    if filename.endswith('.nc'):
        nc_path = os.path.join(folder_path, filename)
        print(f"Processing: {filename}")
        try:
            ds = xr.open_dataset(nc_path)
            output_png_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_binary_emissions.png")
            plot_total_dust_emissions_binary(
                ds=ds,
                variables=emission_vars,
                bounding_box=bounding_box,
                output_png_path=output_png_path
            )
            ds.close()
        except Exception as e:
            print(f"Failed to process {filename}: {e}")
