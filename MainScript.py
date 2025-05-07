
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.colors import LinearSegmentedColormap
from GrainsizeHelpers import plot_grainsize_heatmap
from OysterHelpers import plot_shell_fraction
import pandas as pd


### SINGLES ###
### Grainsize Plotting (see GrainsizeHelpers.py for functions)
## Format CSV: sample rows, sample name include core name and depth in format nn_nncm, columns grainsize bins.
#gs_csv = r"C:\Users\eveve\OneDrive - University of North Carolina at Chapel Hill\PhDprojects\OysterReef\LabData\WardsCreek\Grainsize\WC-23-04\WC-23-04.csv"

## ## ## White Oak (WO)
gs_csv = r"C:\Users\eveve\OneDrive - University of North Carolina at Chapel Hill\PhDprojects\OysterReef\LabData\WhiteOak\Grainsize\WO-23-JI\WO-JI-02_all.csv"
ec = 2.40
gs_csv = r"C:\Users\eveve\OneDrive - University of North Carolina at Chapel Hill\PhDprojects\OysterReef\LabData\WhiteOak\Grainsize\WO-21-3\WO-21-03_ALL.csv"
ec = -16.2  # cm elevation of surface of core, use 0 if plotting with depth
gs_csv = r"C:\Users\eveve\OneDrive - University of North Carolina at Chapel Hill\PhDprojects\OysterReef\LabData\WhiteOak\Grainsize\WO-21-2\WO-21-02_All.csv"
ec = -11.3  # cm elevation of surface of core, use 0 if plotting with depth
gs_csv = r"C:\Users\eveve\OneDrive - University of North Carolina at Chapel Hill\PhDprojects\OysterReef\LabData\WhiteOak\Grainsize\WO-21-1\WO-21-01_ALL.csv"
ec = -18.5  # cm elevation of surface of core, use 0 if plotting with depth

## ## NEWPORT (CR)
gs_csv = r"C:\Users\eveve\OneDrive - University of North Carolina at Chapel Hill\PhDprojects\OysterReef\LabData\NewportRiver\Grainsize\CR-23-02\CR-23-02_ALL.csv"
ec = 33.4  # cm elevation of surface of core, use 0 if plotting with depth
gs_csv = r"C:\Users\eveve\OneDrive - University of North Carolina at Chapel Hill\PhDprojects\OysterReef\LabData\NewportRiver\Grainsize\CR-23-03\CR-23-03_ALL.csv"
ec = 39.0  # cm elevation of surface of core, use 0 if plotting with depth
gs_csv = r"C:\Users\eveve\OneDrive - University of North Carolina at Chapel Hill\PhDprojects\OysterReef\LabData\NewportRiver\Grainsize\CR-21-01\CR-21-01_ALL.csv"
ec = 29.1  # cm elevation of surface of core, use 0 if plotting with depth
gs_csv = r"C:\Users\eveve\OneDrive - University of North Carolina at Chapel Hill\PhDprojects\OysterReef\LabData\NewportRiver\Grainsize\CR-21-02\CR-21-02_ALL.csv"
ec = 9.7  # cm elevation of surface of core, use 0 if plotting with depth
gs_csv = r"C:\Users\eveve\OneDrive - University of North Carolina at Chapel Hill\PhDprojects\OysterReef\LabData\NewportRiver\Grainsize\CR-21-03\CR-21-03_ALL.csv"
ec = 18.7  # cm elevation of surface of core, use 0 if plotting with depth

colors = [(1, 1, 1), (0, 0.5, 0.3), (0, 0.7, 0.5), (0.2, 0.8, 0.8), (0, 0.5, 1),  # creating custom color map
          (0, 0, 0.5)]  # white to other colors
cm = LinearSegmentedColormap.from_list("gs_cmap", colors, N=256)
plot_grainsize_heatmap(gs_csv, y_axis_type="elevation", elev_correction=ec, cmap=cm)  # calling the plot function


### Oyster Shell Fraction Plotting (see OysterHelpers.py for functions)
## Format CSV: file name must include core name as first characters, specify depth interval top and bottom as columns, and a shell fraction column
#sf_csv = r"C:\Users\eveve\OneDrive - University of North Carolina at Chapel Hill\PhDprojects\OysterReef\LabData\WardsCreek\DataSheets\WC-23-07_shellfraction.csv"

## ## White Oak (WO)
sf_csv = r"C:\Users\eveve\OneDrive - University of North Carolina at Chapel Hill\PhDprojects\OysterReef\LabData\WhiteOak\DataSheets\WO-JI-23-03.csv"
ec = -42.9  # elevation of surface of core, use 0 if plotting with depth

sf_csv = r"C:\Users\eveve\OneDrive - University of North Carolina at Chapel Hill\PhDprojects\OysterReef\LabData\WhiteOak\DataSheets\WO-JI-23-02.csv"
ec = 2.4  # elevation of surface of core, use 0 if plotting with depth

sf_csv = r"C:\Users\eveve\OneDrive - University of North Carolina at Chapel Hill\PhDprojects\OysterReef\LabData\WhiteOak\DataSheets\WO-21-03_shellfraction.csv"
ec = -16.2  # elevation of surface of core, use 0 if plotting with depth

sf_csv = r"C:\Users\eveve\OneDrive - University of North Carolina at Chapel Hill\PhDprojects\OysterReef\LabData\WhiteOak\DataSheets\WO-21-02_shellfraction.csv"
ec = -11.3  # elevation of surface of core, use 0 if plotting with depth

sf_csv = r"C:\Users\eveve\OneDrive - University of North Carolina at Chapel Hill\PhDprojects\OysterReef\LabData\WhiteOak\DataSheets\WO-21-01_shellfraction.csv"
ec = -18.5  # elevation of surface of core, use 0 if plotting with depth

## ## Newport (CR)
sf_csv = r"C:\Users\eveve\OneDrive - University of North Carolina at Chapel Hill\PhDprojects\OysterReef\LabData\NewportRiver\DataSheets\CR-21-01_shellfraction.csv"
ec = 29.1
sf_csv = r"C:\Users\eveve\OneDrive - University of North Carolina at Chapel Hill\PhDprojects\OysterReef\LabData\NewportRiver\DataSheets\CR-21-02_shellfraction.csv"
ec = 9.7
sf_csv = r"C:\Users\eveve\OneDrive - University of North Carolina at Chapel Hill\PhDprojects\OysterReef\LabData\NewportRiver\DataSheets\CR-21-03_shellfraction.csv"
ec = 18.7


sf_df = pd.read_csv(sf_csv)
#plt.scatter(sf_df['dry_shell_fraction'], sf_df['Interval_top_cm'])
plot_shell_fraction(sf_csv, depth_top_col='interval_top_cm', depth_bottom_col="interval_bottom_cm",
                    shell_fraction_col="dry_shell_fraction", y_axis_type='elevation', elev_correction=ec)





### MULTIPLES ###

### Needs work

# File paths and corresponding elevation corrections
gs_csv1 = r"C:\Users\eveve\OneDrive - University of North Carolina at Chapel Hill\PhDprojects\OysterReef\LabData\WhiteOak\Grainsize\WO-23-JI\WO-JI-01_all.csv"
ec1 = -8.4

gs_csv2 = r"C:\Users\eveve\OneDrive - University of North Carolina at Chapel Hill\PhDprojects\OysterReef\LabData\WhiteOak\Grainsize\WO-23-JI\WO-JI-02_all.csv"
ec2 = 2.4

gs_csv3 = r"C:\Users\eveve\OneDrive - University of North Carolina at Chapel Hill\PhDprojects\OysterReef\LabData\WhiteOak\Grainsize\WO-23-JI\WO-JI-03_all.csv"
ec3 = -42.9

# Define color map
colors = [
    (1, 1, 1),
    (0, 0.5, 0.3),
    (0, 0.7, 0.5),
    (0.2, 0.8, 0.8),
    (0, 0.5, 1),
    (0, 0, 0.5)
]
cm = LinearSegmentedColormap.from_list("gs_cmap", colors, N=256)


# Create a figure with 3 subplots sharing the y-axis
fig, axes = plt.subplots(nrows=1, ncols=3, sharey=True, figsize=(15, 5))

# Plot each heatmap on its respective axis
plot_grainsize_heatmap(gs_csv1, y_axis_type="elevation", elev_correction=ec1, cmap=cm, ax=axes[0])
plot_grainsize_heatmap(gs_csv2, y_axis_type="elevation", elev_correction=ec2, cmap=cm, ax=axes[1])
plot_grainsize_heatmap(gs_csv3, y_axis_type="elevation", elev_correction=ec3, cmap=cm, ax=axes[2])

# Adjust layout for better spacing
plt.tight_layout()
plt.show()