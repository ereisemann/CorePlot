import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import re


def extract_depth(id_string):   ## Function to extract depths from the sample ID column
    """
    this function uses a regular expression to find numerical patterns in the ID field of grainsize data
    it will match any pattern number-number followed directly by 'cm', like 0-5cm, 0-15cm, 100-105cm
    :param id_string: the ID string containing the depth information, e.g. 'WC-23-00_10-15cm'
    :return: the depth range as a string, e.g. '05-10'
    """

    id_string = id_string.replace("\n", "")

    ### Use regular expression to find patterns like '10-15cm'
    match = re.search(r'(\d+-\d+)cm', id_string)
    if match:
        return match.group(1)
    return None

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

    # Reindex to include all depths from min to max depth, inserting NaNs where data is missing
    full_depth_range = range(int(expanded_df[depth_top_col].min()), int(expanded_df[depth_top_col].max()) + 1)
    expanded_df = expanded_df.set_index(depth_top_col).reindex(full_depth_range).reset_index()
    expanded_df = expanded_df.rename(columns={'index': depth_top_col})

    return expanded_df

#
# def plot_grainsize_heatmap(grainsize_csv, y_axis_type, elev_correction=0, cmap="viridis"):
#     """
#     Plots a heat map of grainsize distributions down core.
#     Parameters:
#     - grainsize_csv: a csv file saved from cilas pal excel output
#     - y_axis_type: "elevation" or "depth" are accepted for this field
#     - elev_correction: cm elevation of ground surface. this value will be added to the depth values
#     - cmap: Colormap to be used for the heat map. Default is 'viridis'.
#     """
#
#     df = pd.read_csv(grainsize_csv)
#
#     ### applying depth extraction & separation into bottom and top
#     df['depth_range'] = df['ID'].apply(extract_depth)
#     df[['depth_top', 'depth_bottom']] = df['depth_range'].str.split('-', expand=True)
#     df['depth_top'] = df['depth_top'].astype(float)
#     df['depth_bottom'] = df['depth_bottom'].astype(float)
#
#     ### defining vars for expand
#     grainsize_cols = df.columns.difference(
#         ['ID', 'depth_range', 'depth_top', 'depth_bottom', 'Mean', 'Median']).tolist()
#
#     ### Preparing variables for plot
#     # use expand_grainsize_data function to copy gs distribution for each cm in sample (see function descript above)
#     data = expand_grainsize_data(df, "depth_top", "depth_bottom", grainsize_cols)
#
#     # Ensure data is sorted by depth
#     depth_col = 'depth_top'   # can edit this if prefer to plot with depth bottom or average
#     data[depth_col] = data[depth_col].astype(float)
#     data = data.sort_values(by=depth_col)
#
#     # Extract core ID, first 8 characters in first entry of "ID" column
#     core_id = data['ID'].iloc[0][:8]
#     print(f"plotting {core_id}")
#
#     # Extract depths and convert to elevation if specified
#     if y_axis_type == 'elevation':
#         elevations = elev_correction - data[depth_col]
#         data['elevation'] = elevations
#         depths = data['elevation']
#     elif y_axis_type == 'depth':
#         depths = data[depth_col]
#     else:
#         print(f'specify y_axis_type as "elevation" or "depth"')
#         return
#
#     # Extract grain size distribution values
#     grainsize_distributions = data[grainsize_cols]
#
#     # Sort the grain size columns numerically
#     grainsize_distributions = grainsize_distributions.reindex(sorted(grainsize_cols, key=float), axis=1)
#
#     # Set 0 for values below 0.05, color scale
#     norm = plt.Normalize(vmin=0.05, vmax=8)
#
#     # Plot the heatmap using Seaborn
#     matplotlib.use('TkAgg')  # different visualizer that doesn't freeze
#     plt.ion()  # Turn on interactive mode
#     plt.figure(figsize=(4,8))
#     sns.heatmap(grainsize_distributions, cmap=cmap, norm=norm, cbar=True, xticklabels=5)
#
#     min_depth = int(np.floor(min(depths)/5)*5)
#     max_depth = int(np.ceil(max(depths)/5)*5)
#
#     if y_axis_type == 'elevation':
#         y_ticklabels = np.arange(max_depth, min_depth - 1, -5)
#         plt.ylabel('Elevation (cm NAVD 88)')
#     else:
#         y_ticklabels = np.arange(min_depth, int(max_depth) + 1, 5)
#         plt.ylabel('Depth (cm)')
#
#     # Setting the y-axis ticks to be every 5 cm
#     #y_ticks = np.arange(int(min(depths)), int(max(depths)) + 1, 5)
#
#     # Apply custom y-ticks and labels
#     plt.gca().set_yticks(np.linspace(0, len(depths) - 1, len(y_ticklabels)))
#     plt.gca().set_yticklabels(y_ticklabels)
#     plt.title(f'Grainsize - {core_id}')
#     plt.xlabel('Grainsize')
#     plt.xticks(rotation=90)  # Rotate depth labels for better readability
#     plt.yticks(rotation=0)
#     plt.show()



    ## DRAFT of new function:
def plot_grainsize_heatmap(grainsize_csv, y_axis_type, elev_correction=0, cmap="viridis", ax=None):
    """
    Plots a heat map of grainsize distributions down core.

    Parameters:
    - grainsize_csv: a CSV file saved from cilas pal excel output.
    - y_axis_type: "elevation" or "depth" are accepted for this field.
    - elev_correction: cm elevation of ground surface; this value will be added to the depth values.
    - cmap: Colormap to be used for the heat map. Default is 'viridis'.
    - ax: Matplotlib Axes object to plot on. If None, a new figure and axis will be created.
    """
    import pandas as pd
    import numpy as np
    import matplotlib
    import matplotlib.pyplot as plt
    import seaborn as sns

    # Read CSV data
    df = pd.read_csv(grainsize_csv)

    # Applying depth extraction & separation into bottom and top
    df['depth_range'] = df['ID'].apply(extract_depth)
    df[['depth_top', 'depth_bottom']] = df['depth_range'].str.split('-', expand=True)
    df['depth_top'] = df['depth_top'].astype(float)
    df['depth_bottom'] = df['depth_bottom'].astype(float)

    # Define variables for expand: select all columns except these ones
    grainsize_cols = df.columns.difference(
        ['ID', 'depth_range', 'depth_top', 'depth_bottom', 'Mean', 'Median']
    ).tolist()

    # Prepare variables for plot using expand_grainsize_data function
    data = expand_grainsize_data(df, "depth_top", "depth_bottom", grainsize_cols)

    # Ensure data is sorted by depth (using depth_top)
    depth_col = 'depth_top'
    data[depth_col] = data[depth_col].astype(float)
    data = data.sort_values(by=depth_col)

    # Extract core ID from the first 8 characters of the first "ID" entry
    core_id = data['ID'].iloc[0][:8]
    print(f"plotting {core_id}")

    # Compute depths or elevations based on y_axis_type
    if y_axis_type == 'elevation':
        elevations = elev_correction - data[depth_col]
        data['elevation'] = elevations
        depths = data['elevation']
    elif y_axis_type == 'depth':
        depths = data[depth_col]
    else:
        print('Specify y_axis_type as "elevation" or "depth"')
        return

    # Extract grain size distribution values and sort columns numerically
    grainsize_distributions = data[grainsize_cols]
    grainsize_distributions = grainsize_distributions.reindex(
        sorted(grainsize_cols, key=float), axis=1
    )

    # Set values below 0.05 and define the normalization for the colormap
    norm = plt.Normalize(vmin=0.05, vmax=8)

    # Set up the plotting axis: create one if not provided
    #matplotlib.use('TkAgg')
    plt.ion()  # Enable interactive mode

    new_fig = False
    if ax is None:
        fig, ax = plt.subplots(figsize=(4, 8))
        new_fig = True

    # Plot the heatmap on the specified axis using seaborn
    sns.heatmap(grainsize_distributions, cmap=cmap, norm=norm, cbar=True,
                xticklabels=5, ax=ax)

    # Determine min and max depths for tick settings
    min_depth = int(np.floor(min(depths) / 5) * 5)
    max_depth = int(np.ceil(max(depths) / 5) * 5)

    # Set y-tick labels and axis label based on y_axis_type
    if y_axis_type == 'elevation':
        y_ticklabels = np.arange(max_depth, min_depth - 1, -5)
        ax.set_ylabel('Elevation (cm NAVD 88)')
    else:
        y_ticklabels = np.arange(min_depth, max_depth + 1, 5)
        ax.set_ylabel('Depth (cm)')

    ax.set_yticks(np.linspace(0, len(depths) - 1, len(y_ticklabels)))
    ax.set_yticklabels(y_ticklabels)
    ax.set_title(f'Grainsize - {core_id}')
    ax.set_xlabel('Grainsize')
    plt.setp(ax.get_xticklabels(), rotation=90)
    plt.setp(ax.get_yticklabels(), rotation=0)


    if new_fig:
        plt.show()