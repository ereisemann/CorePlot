from matplotlib.colors import LinearSegmentedColormap
from GrainsizeHelpers import plot_grainsize_heatmap
from OysterHelpers import plot_shell_fraction


### Grainsize Plotting (see GrainsizeHelpers.py for functions)
## Format CSV: sample rows, sample name include core name and depth in format nn_nncm, columns grainsize bins.
gs_csv = r"C:\Users\eveve\OneDrive - University of North Carolina at Chapel Hill\PhDprojects\OysterReef\LabData\WardsCreek\Grainsize\WC-23-04\WC-23-04.csv"
ec = 18.10  # elevation correction
colors = [(1, 1, 1), (0, 0.5, 0.3), (0, 0.7, 0.5), (0.2, 0.8, 0.8), (0, 0.5, 1),  # creating custom color map
          (0, 0, 0.5)]  # white to other colors
cm = LinearSegmentedColormap.from_list("gs_cmap", colors, N=256)
plot_grainsize_heatmap(gs_csv, y_axis_type="elevation", elev_correction=ec, cmap=cm)  # calling the plot function


### Oyster Shell Fraction Plotting (see OysterHelpers.py for functions)
## Format CSV: file name must include core name as first characters, specify depth interval top and bottom as columns, and a shell fraction column
sf_csv = r"C:\Users\eveve\OneDrive - University of North Carolina at Chapel Hill\PhDprojects\OysterReef\LabData\WardsCreek\DataSheets\WC-23-04_shellfraction.csv"
sf_df = pd.read_csv(sf_csv)
ec = 18.10  # elevation correction
#plt.scatter(sf_df['dry_shell_fraction'], sf_df['Interval_top_cm'])
plot_shell_fraction(sf_csv, depth_top_col='interval_top_cm', depth_bottom_col="interval_bottom_cm",
                    shell_fraction_col="dry_shell_fraction", y_axis_type='elevation', elev_correction=ec)

