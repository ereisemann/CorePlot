import pandas as pd
#import numpy as np
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



def plot_grainsize_heatmap(data, depth_col, grainsize_cols, cmap="viridis"):
    """
    Plots a heat map of grainsize distributions down core.

    Parameters:
    - data: A DataFrame containing grain size distributions and depth.
    - depth_col: The name of the column representing depth.
    - grainsize_cols: List of column names for grain size distribution.
    - cmap: Colormap to be used for the heat map. Default is 'viridis'.
    """
    # Ensure data is sorted by depth
    data[depth_col] = data[depth_col].astype(float)
    data = data.sort_values(by=depth_col)

    # Extract core ID, first 8 characters in first entry of "ID" column
    core_id = data['ID'].iloc[0][:8]

    # Extract depth and grain size distribution values
    depths = data[depth_col]
    grainsize_distributions = data[grainsize_cols]

    # Sort the grain size columns numerically
    grainsize_distributions = grainsize_distributions.reindex(sorted(grainsize_cols, key=float), axis=1)
    # Set 0 for values below 0.05
    norm = plt.Normalize(vmin=0.05, vmax=8)

    # Plot the heatmap using Seaborn
    plt.figure(figsize=(8,6))
    sns.heatmap(grainsize_distributions, cmap = cmap, norm = norm, cbar = True,
                yticklabels = depths, xticklabels = 5)

#    ax.set_yticks(range(len(depths)))
#    ax.set_yticklabels(depths)

    plt.title(f'Grainsize - {core_id}')
    plt.xlabel('Grainsize')
    plt.ylabel('Depth (cm)')
    plt.xticks(rotation=90)  # Rotate depth labels for better readability
    plt.show()


## Function to extract depths from the sample ID
def extract_depth(id_string):
    ### Use regular expression to find patterns like '10-15cm'
    match = re.search(r'(\d+-\d+)cm', id_string)
    if match:
        return match.group(1)
    return None




### CSV file containing CILASpal output, formatted to exclude mean
csv_file = r"C:\Users\eveve\OneDrive - University of North Carolina at Chapel Hill\PhDprojects\OysterReef\LabData\WardsCreek\Grainsize\WC-23-00\WC-23-00_grainsize.CSV"
df = pd.read_csv(csv_file)

### applying depth extraction & separation into bottom and top
df['depth_range'] = df['ID'].apply(extract_depth)
df[['depth_top', 'depth_bottom']] = df['depth_range'].str.split('-', expand = True)
df['depth_top'] = df['depth_top'].astype(float)
df['depth_bottom'] = df['depth_bottom'].astype(float)



### defining vars for plot
depth_col = 'depth_top'
grainsize_cols = df.columns.difference(['ID', 'depth_range', 'depth_top', 'depth_bottom']).tolist()

### defining cmap
# Create a custom colormap where values below 0.05 are white
colors = [(1, 1, 1), (0, 0.5, 0.3), (0, 0.7, 0.5), (0.2, 0.8, 0.8), (0, 0.5, 1), (0, 0, 0.5)]  # white to other colors
cmap = LinearSegmentedColormap.from_list("gs_cmap", colors, N = 256)


### Plotting
matplotlib.use('TkAgg')
plt.ion()  # Turn off interactive mode
#plot_grainsize_heatmap(small_data, depth_col, small_grainsize_cols, cmap="viridis")
plot_grainsize_heatmap(df, depth_col, grainsize_cols, cmap = cmap)





####################### TESTING ###########################

### subset for testing
depth_col = 'depth_top'
small_data = df.head(10)
small_grainsize_cols = grainsize_cols[:20]
small_data_expand = expand_grainsize_data(small_data, 'depth_top', 'depth_bottom', grainsize_cols)

data = small_data_expand




# Ensure data is sorted by depth
data[depth_col] = data[depth_col].astype(float)
data = data.sort_values(by=depth_col)

# Extract core ID, first 8 characters in first entry of "ID" column
core_id = data['ID'].iloc[0][:8]

# Extract depth and grain size distribution values
depths = data[depth_col]
grainsize_distributions = data[small_grainsize_cols]

# Sort the grain size columns numerically
grainsize_distributions = grainsize_distributions.reindex(sorted(small_grainsize_cols, key=float), axis=1)
# Set 0 for values below 0.05
norm = plt.Normalize(vmin=0.05, vmax=8)

# Plot the heatmap using Seaborn
plt.figure(figsize=(8,6))
sns.heatmap(grainsize_distributions, cmap = cmap, cbar = True)

plt.title(f'Grainsize - {core_id}')
plt.xlabel('Grainsize')
plt.ylabel('Depth (cm)')
plt.xticks(rotation=90)  # Rotate depth labels for better readability
plt.show()




