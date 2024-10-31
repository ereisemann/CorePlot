
from matplotlib.colors import LinearSegmentedColormap
from GrainsizeHelpers import plot_grainsize_heatmap





### Grainsize Plotting (see GrainsizeHelpers.py for functions)
gs_csv = r"C:\Users\eveve\OneDrive - University of North Carolina at Chapel Hill\PhDprojects\OysterReef\LabData\WardsCreek\Grainsize\WC-23-00\WC-23-00_grainsize.csv"
ec = -27.6  # elevation correction
colors = [(1, 1, 1), (0, 0.5, 0.3), (0, 0.7, 0.5), (0.2, 0.8, 0.8), (0, 0.5, 1),  # creating custom color map
          (0, 0, 0.5)]  # white to other colors
cm = LinearSegmentedColormap.from_list("gs_cmap", colors, N=256)
plot_grainsize_heatmap(gs_csv, y_axis_type="elevation", elev_correction=ec, cmap=cmap)  # calling the plot function


### plotting oyster shell fraction
sf_csv = r"C:\Users\eveve\OneDrive - University of North Carolina at Chapel Hill\PhDprojects\OysterReef\LabData\WardsCreek\DataSheets\WC-23-00_shellfraction.csv"
sf_df = pd.read_csv(sf_csv)
#plt.scatter(sf_df['dry_shell_fraction'], sf_df['Interval_top_cm'])
plot_shell_fraction(sf_csv, 'interval_top_cm', "interval_bottom_cm", "dry_shell_fraction ", y_axis_type = 'elevation', elev_correction = ec)