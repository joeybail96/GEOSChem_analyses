import xarray as xr
import matplotlib.pyplot as plt

# Load NACHTT Campaign Data
nachtt_nc_file = (
    "/uufs/chpc.utah.edu/common/home/haskins-group1/data/Campaign_Data/Raw_Data/"
    "NACHTT_2011/data/elevator/NACHTT_2011_1min_Merged.nc"
)
nachtt_nc = xr.open_dataset(nachtt_nc_file)

# --------------------------
# Plot 1: N2O5 (left), ClNO2 and Cl2 (right)
# --------------------------

fig, ax1 = plt.subplots(figsize=(14, 6))

# Left axis: N2O5
ax1.plot(nachtt_nc['time'], nachtt_nc['N2O5_pptv'], label='N2O5 (pptv)', color='tab:blue')
ax1.set_xlabel('Time')
ax1.set_ylabel('N2O5 (pptv)', color='tab:blue')
ax1.tick_params(axis='y', labelcolor='tab:blue')

# Right axis: ClNO2 and Cl2
ax2 = ax1.twinx()
ax2.plot(nachtt_nc['time'], nachtt_nc['ClNO2_pptv'], label='ClNO2 (pptv)', color='tab:red')
ax2.plot(nachtt_nc['time'], nachtt_nc['Cl2_pptv'], label='Cl2 (pptv)', color='tab:green')
ax2.set_ylabel('ClNO2 / Cl2 (pptv)', color='black')
ax2.tick_params(axis='y', labelcolor='black')

# Combine legends
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')

plt.title('Reactive Chlorine Species: N2O5, ClNO2, Cl2')
plt.grid(True)
plt.tight_layout()
plt.show()

# --------------------------
# Plot 2: AMS pCl (left), AMS Total (right)
# --------------------------

fig, ax1 = plt.subplots(figsize=(14, 6))

# Left axis: AMS pCl
ax1.plot(nachtt_nc['time'], nachtt_nc['AMS_pCl_ugm3'], label='AMS pCl (µg/m³)', color='tab:blue')
ax1.set_xlabel('Time')
ax1.set_ylabel('AMS pCl (µg/m³)', color='tab:blue')
ax1.tick_params(axis='y', labelcolor='tab:blue')

# Right axis: AMS Total
ax2 = ax1.twinx()
ax2.plot(nachtt_nc['time'], nachtt_nc['AMS_Total_ugm3'], label='AMS Total (µg/m³)', color='tab:green')
ax2.set_ylabel('AMS Total (µg/m³)', color='tab:green')
ax2.tick_params(axis='y', labelcolor='tab:green')

# Combine legends
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')

plt.title('AMS pCl and AMS Total Concentrations')
plt.grid(True)
plt.tight_layout()
plt.show()
