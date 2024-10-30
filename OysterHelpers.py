import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import os

sf_csv = r"C:\Users\eveve\OneDrive - University of North Carolina at Chapel Hill\PhDprojects\OysterReef\LabData\WardsCreek\DataSheets\WC-23-00_shellfraction.csv"
sf_df = pd.read_csv(sf_csv)
plt.scatter(sf_df['dry_shell_fraction'], sf_df['Interval_top_cm'])

def plot_shell_fraction(shell_fraction_csv, depth_top_col, depth_bottom_col, shell_fraction_col, y_axis_type, elev_correction):
    filename = os.path.basename(shell_fraction_csv)  # Gets 'WC-23-00_shellfraction.csv'
    core_id = filename[:8]         # Gets 'WC-23-00'

    sf_df = pd.read_csv(shell_fraction_csv)
    # calculating sample center depth for point plotting
    sf_df['ave_depth'] = ((sf_df[depth_top_col] - sf_df[depth_bottom_col])/2) + sf_df[depth_bottom_col]
    sf_df = sf_df.sort_values(by = depth_top_col)

    # Extract depths and convert to elevation if specified
    if y_axis_type == 'elevation':
        elevations = elev_correction - sf_df['ave_depth']
        sf_df['elevation'] = elevations
        depths = sf_df['elevation']
    elif y_axis_type == 'depth':
        depths = sf_df['ave_depth']
    else:
        print(f'specify y_axis_type as "elevation" or "depth"')
        return

    matplotlib.use('TkAgg')  # different visualizer that doesn't freeze
    plt.ion()  # Turn on interactive mode
    plt.figure(figsize=(8, 6))
    plt.scatter(sf_df[shell_fraction_col], depths)

    if y_axis_type == 'elevation':
        y_ticklabels = np.arange(int(max(depths)), int(min(depths)) - 1, -5)
        plt.ylabel('Elevation (cm NAVD 88)')
    else:
        y_ticklabels = np.arange(int(min(depths)), int(max(depths)) + 1, 5)
        plt.ylabel('Depth (cm)')

    # Apply custom y-ticks and labels
    plt.gca().invert_yaxis()
    #plt.gca().set_yticks(np.linspace(0, len(depths) - 1, len(y_ticklabels)))
    plt.gca().set_yticklabels(y_ticklabels)
    plt.title(f'Oyster Shell Fraction - {core_id}')
    plt.xlabel('Dry Shell Fraction')
    plt.xticks(rotation=90)  # Rotate depth labels for better readability
    plt.yticks(rotation=0)
    plt.show()