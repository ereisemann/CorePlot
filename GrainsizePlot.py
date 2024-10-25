import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns
import re

def expand_grainsize_data(df, depth_top_col, depth_bottom_col, grainsize_cols):
    """
    Fills in the grainsize dataframe so there is a copy of the grainsize distribution
    for each cm down core. This enables plotting with correct sample spacing in a
    heatmap.

    Parameters:
     - df: A DataFrame containing grain size distributions and depth.
    - depth_top_col: The name of the column representing top depth (format as float).
    - depth_bottom_col: the name of the column representing the bottom depth (format as float).
    - grainsize_cols: List of column names for grain size distribution.
       """
    # Create an empty list to store expanded rows
    expanded_rows = []

    # Iterate over each row in the dataframe
    for _, row in df.iterrows():
        # Get depth_top and depth_bottom for the current row
        depth_top = int(row[depth_top_col])
        depth_bottom = int(row[depth_bottom_col])

        # Iterate through each centimeter between depth_top and depth_bottom
        for depth in range(depth_top, depth_bottom):
            # Create a new row with the current depth and grain size data
            new_row = row.copy()  # Copy the existing row
            new_row[depth_top_col] = depth  # Set depth top as the current cm
            new_row[depth_bottom_col] = depth + 1  # Set depth bottom to match depth top

            # Append the new row to the list of expanded rows
            expanded_rows.append(new_row)

    # Convert the list of expanded rows back into a dataframe
    expanded_df = pd.DataFrame(expanded_rows)

    # Sort by the new depth top to maintain order
    expanded_df = expanded_df.sort_values(by=depth_top_col)

    return expanded_df


def plot_grainsize_heatmap(data, depth_col, grainsize_cols, y_axis_type , elev_correction = 0, cmap="viridis"):
    """
    Plots a heat map of grainsize distributions down core.
    Parameters:
    - data: A DataFrame containing grain size distributions and depth.
    - depth_col: The name of the column representing top of the sample depth
    - grainsize_cols: List of column names for grain size distribution.
    - y_axis_type: "elevation" or "depth" are accepted for this field
    - elev_correction: cm elevation of ground surface. this value will be added to the depth values
    - cmap: Colormap to be used for the heat map. Default is 'viridis'.
    """
    # Ensure data is sorted by depth
    data[depth_col] = data[depth_col].astype(float)
    data = data.sort_values(by=depth_col)

    # Extract core ID, first 8 characters in first entry of "ID" column
    core_id = data['ID'].iloc[0][:8]
    print(f"plotting {core_id}")

    # Extract depths and convert to elevation if specified
    if y_axis_type == 'elevation':
        elevations = elev_correction - data[depth_col]
        data['elevation'] = elevations
        depths = data['elevation']
    elif y_axis_type == 'depth':
        depths = data[depth_col]
    else:
        print(f'specify y_axis_type as "elevation" or "depth"')
        return

    # Extract grain size distribution values
    grainsize_distributions = data[grainsize_cols]

    # Sort the grain size columns numerically
    grainsize_distributions = grainsize_distributions.reindex(sorted(grainsize_cols, key=float), axis=1)

    # Set 0 for values below 0.05, color scale
    norm = plt.Normalize(vmin=0.05, vmax=8)

    # Plot the heatmap using Seaborn
    plt.figure(figsize=(8,6))
    sns.heatmap(grainsize_distributions, cmap=cmap, norm=norm, cbar=True, xticklabels=5)

    if y_axis_type == 'elevation':
        y_ticklabels = np.arange(int(max(depths)), int(min(depths)) - 1, -5)
        plt.ylabel('Elevation (cm NAVD 88)')
    else:
        y_ticklabels = np.arange(int(min(depths)), int(max(depths)) + 1, 5)
        plt.ylabel('Depth (cm)')

    # Setting the y-axis ticks to be every 5 cm
    #y_ticks = np.arange(int(min(depths)), int(max(depths)) + 1, 5)

    # Apply custom y-ticks and labels
    plt.gca().set_yticks(np.linspace(0, len(depths) - 1, len(y_ticklabels)))
    plt.gca().set_yticklabels(y_ticklabels)
    plt.title(f'Grainsize - {core_id}')
    plt.xlabel('Grainsize')
    plt.xticks(rotation=90)  # Rotate depth labels for better readability
    plt.yticks(rotation=0)
    plt.show()


def extract_depth(id_string):   ## Function to extract depths from the sample ID
    ### Use regular expression to find patterns like '10-15cm'
    match = re.search(r'(\d+-\d+)cm', id_string)
    if match:
        return match.group(1)
    return None


### CSV file containing CILASpal output, formatted to exclude mean
#csv_file = r"C:\Users\eveve\OneDrive - University of North Carolina at Chapel Hill\PhDprojects\OysterReef\LabData\WardsCreek\Grainsize\WC-23-00\WC-23-00_grainsize.CSV"
csv_file = r"C:\Users\eveve\OneDrive - University of North Carolina at Chapel Hill\PhDprojects\OysterReef\LabData\WardsCreek\Grainsize\WC-23-06\WC-23-06.csv"
df = pd.read_csv(csv_file)

### applying depth extraction & separation into bottom and top
df['depth_range'] = df['ID'].apply(extract_depth)
df[['depth_top', 'depth_bottom']] = df['depth_range'].str.split('-', expand=True)
df['depth_top'] = df['depth_top'].astype(float)
df['depth_bottom'] = df['depth_bottom'].astype(float)

### defining vars for expand & plot
depth_col = 'depth_top'
grainsize_cols = df.columns.difference(['ID', 'depth_range', 'depth_top', 'depth_bottom','Mean','Median']).tolist()

### Preparing variables for plot function
matplotlib.use('TkAgg')  # different visualizer that doesn't freeze
plt.ion()  # Turn off interactive mode
df_expand = expand_grainsize_data(df, "depth_top", "depth_bottom", grainsize_cols)
# Create a custom colormap where values below 0.05 are white
colors = [(1, 1, 1), (0, 0.5, 0.3), (0, 0.7, 0.5), (0.2, 0.8, 0.8), (0, 0.5, 1), (0, 0, 0.5)]  # white to other colors
cmap = LinearSegmentedColormap.from_list("gs_cmap", colors, N = 256)
elev_corr = 2.8

plot_grainsize_heatmap(df_expand, depth_col, grainsize_cols, y_axis_type="elevation", elev_correction=elev_corr, cmap = cmap)






####################### TESTING ###########################

### subset for testing
#depth_col = 'depth_top'
#small_data = df.head(10)
#small_grainsize_cols = grainsize_cols[:20]
#small_data_expand = expand_grainsize_data(small_data, 'depth_top', 'depth_bottom', grainsize_cols)
#data = small_data_expand
