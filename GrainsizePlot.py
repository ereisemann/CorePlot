import pandas as pd
#import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re


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
    data = data.sort_values(by=depth_col)

    # Extract depth and grain size distribution values
    depths = data[depth_col]
    grainsize_distributions = data[grainsize_cols]

    # Plot the heatmap using Seaborn
    plt.figure(figsize=(8,6))
    sns.heatmap(grainsize_distributions, cmap=cmap, cbar=True,
                yticklabels=depths, xticklabels=grainsize_cols if len(grainsize_cols) <20 else False)

    plt.title('Grainsize Distribution Down Core')
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


### defining vars for plot
depth_col = 'depth_top'
grainsize_cols = df.columns.difference(['ID', 'depth_range', 'depth_top', 'depth_bottom']).tolist()

small_data = data = df.head(5)
small_grainsize_cols = grainsize_cols[:20]


plt.ion()  # Turn off interactive mode
plot_grainsize_heatmap(small_data, depth_col, small_grainsize_cols, cmap="viridis")
