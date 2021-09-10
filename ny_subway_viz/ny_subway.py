import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
import seaborn as sns

'''
Data Visualization Using NYC Subway Entry and Exit Data
-------------------------------------------------------
Dataset download link for reference: https://www.kaggle.com/kalilurrahman/newyork-subway-entry-exit-dataset-for-dataviz
Shape file download for railroads and roads: https://www.statsilk.com/maps/download-free-shapefile-maps
Shape file download for outline of land: https://gadm.org/download_country_v3.html
geopandas allows for processing of shape files to make maps
'''

DATA_FILE = 'rows.csv'      # NYC subway data
SHAPE_FILE = gpd.read_file('USA_roads.shp')
SHAPE_FILE_TWO = gpd.read_file('gadm36_USA_1.shp')

'''
Main function calls the functions to load the data,prints the first few rows, and gives extra info on the dataset.
Data manipulation to prepare the dataset to be used in plotting functions is done in this function.
When data is prepared, plotting functions are called. They all start with the word 'plot'.
'''
def main():

    subway_df = load_data()
    # Subsets the subway_df dataframe to ensure only necessary columns are used
    subway_df = subway_df[["Division", "Line", "Station Name", "Station Latitude", "Station Longitude"]]
    print(subway_df.head())
    print(subway_df.info())
    print(subway_df.columns)

    # Groups the dataframe by Division to make bar charts based on the number of entries by Division
    div_count = subway_df.groupby('Division').agg('count').reset_index()
    print(div_count.head())
    plot_chart_one(div_count)

    # Groups the dataframe by Line to make bar charts based on the number of entries by Line
    line_count = subway_df.groupby('Line').agg('count').reset_index()
    print(line_count.head())
    plot_chart_two(line_count)

    # Extracts a series of counts for the line column and adds it to the dataframe to sort other variables by the number
    # of entries by line
    line_count_series = subway_df.groupby('Line')['Line'].transform('count')
    # Duplicating the old dataframe with a new name
    subway_df_update = subway_df
    # Using assign function to add the series to the dataset
    subway_df_update = subway_df_update.assign(line_count=line_count_series.values)
    print(subway_df_update.head())

    plot_scatter_one(subway_df_update)
    plot_scatter_two(subway_df_update)
    plot_street_map(subway_df_update)
    plot_street_map_two(subway_df_update)
    plot_street_map_three(subway_df_update)


'''
This function loads data from the constant DATA_FILE using pandas to import the csv.
'''
def load_data():
    csv_file = pd.read_csv(DATA_FILE)
    return csv_file


'''
Plots a scatter plot of the location (latitude by longitude) and sorts by Division using hue. File is 
saved using save_fig() function.
'''
def plot_scatter_one(subway_df_update):
    x = subway_df_update['Station Longitude']
    y = subway_df_update['Station Latitude']
    sort_hue = subway_df_update['Division']
    plt.figure(figsize=(12, 12))
    sns.scatterplot(x, y, hue=sort_hue)
    plt.title("Station Location", fontsize=20)
    plt.xlabel("Latitude", fontsize=16)
    plt.ylabel("Longitude", fontsize=16)
    save_fig(fig_id="location_scatter_color_division")
    plt.show(block=False)
    plt.pause(1)                     # Opens the window for 1 second before closing it
    plt.close("all")


'''
Plots a scatter plot of the location (latitude by longitude) and sorts by Line using hue. File is 
saved using save_fig() function.
'''
def plot_scatter_two(subway_df_update):
    x = subway_df_update['Station Longitude']
    y = subway_df_update['Station Latitude']
    sort_hue = subway_df_update['Line']
    sort_size = subway_df_update['line_count']
    plt.figure(figsize=(14, 12))
    sns.scatterplot(x, y, hue=sort_hue, size=sort_size)
    plt.title("Station Location", fontsize=20)
    plt.xlabel("Latitude", fontsize=16)
    plt.ylabel("Longitude", fontsize=16)
    plt.legend(bbox_to_anchor=(1.18, 1), borderaxespad=0)
    save_fig(fig_id="location_scatter_color_line")
    plt.show(block=False)
    plt.pause(1)
    plt.close("all")


'''
Plots bar chart of the number of entries by Division
'''
def plot_chart_one(div_count):
    x = div_count['Division']
    y = div_count['Line']
    plt.figure(figsize=(12, 12))
    sns.barplot(x, y)
    plt.title("Number of Entries by Division", fontsize=20)
    plt.xlabel("Division \n\n"
               "This chart counts the number of subway entries in each division.", fontsize=16)
    plt.ylabel("Number of Entries", fontsize=16)
    save_fig(fig_id="division_barchart")
    plt.show(block=False)
    plt.pause(1)                        # Opens the window for 1 second before closing it
    plt.close("all")


'''
Plots bar chart of the number of entries by Line
'''
def plot_chart_two(line_count):
    x = line_count['Division']
    y = line_count['Line']
    plt.figure(figsize=(12, 12))
    sns.barplot(x, y)
    plt.title("Number of Entries by Line", fontsize=20)
    plt.xlabel("Number of Entries \n\n"
               "This chart counts the number of subway entries in each line.", fontsize=16)
    plt.ylabel("Line", fontsize=16)
    save_fig(fig_id="line_barchart")
    plt.show(block=False)
    plt.pause(1)                    # Opens the window for 1 second before closing it
    plt.close("all")


'''
Plots a scatter plot of the location (latitude by longitude) over a road map of the NYC area
and sorts by Line using hue and sorts the number of entries in a line using the size of the markers. 
File is saved using save_fig() function.
'''
def plot_street_map(subway_df_update):
    street_map = SHAPE_FILE
    # Creates bounds for the shape file
    bbox = (subway_df_update['Station Longitude'].min(), subway_df_update['Station Longitude'].max(),
            subway_df_update['Station Latitude'].min(), subway_df_update['Station Latitude'].max())
    x = subway_df_update['Station Longitude']
    y = subway_df_update['Station Latitude']
    sort_hue = subway_df_update['Line']
    sort_size = subway_df_update['line_count']

    fig, ax = plt.subplots(figsize=(12, 12))
    street_map.plot(ax=ax, color='grey')
    ax.set_xlim(bbox[0] - 0.005, bbox[1] + 0.005)
    ax.set_ylim(bbox[2] - 0.005, bbox[3] + 0.005)
    sns.scatterplot(x, y, hue=sort_hue, size=sort_size, ax=ax)
    ax.legend(bbox_to_anchor=(1.05, 1), borderaxespad=0)
    save_fig(fig_id="geo_chart")
    fig.show()


'''
Plots a scatter plot of the location (latitude by longitude) over an administrative map of the NYC area
and sorts by Line using hue and sorts the number of entries in a line using the size of the markers. 
File is saved using save_fig() function.
'''
def plot_street_map_two(subway_df_update):
    street_map = SHAPE_FILE_TWO
    # Creates bounds for the shape file
    bbox = (subway_df_update['Station Longitude'].min(), subway_df_update['Station Longitude'].max(),
            subway_df_update['Station Latitude'].min(), subway_df_update['Station Latitude'].max())
    x = subway_df_update['Station Longitude']
    y = subway_df_update['Station Latitude']
    sort_hue = subway_df_update['Line']
    sort_size = subway_df_update['line_count']

    fig, ax = plt.subplots(figsize=(12, 15))
    street_map.plot(ax=ax, color='black', alpha=0.6)
    ax.set_xlim(bbox[0] - 0.005, bbox[1] + 0.005)
    ax.set_ylim(bbox[2] - 0.005, bbox[3] + 0.005)
    sns.scatterplot(x, y, hue=sort_hue, size=sort_size, ax=ax)
    ax.legend(bbox_to_anchor=(1.05, 1), borderaxespad=0)
    ax.set_xlabel("Station Longitude  \n\n\n"
                  "This scatter plot shows each subway station's location on a map. Each line has a different hue \n"
                  "and the size of the markers is determined by the number of entries each line has.",
                  fontsize=16)
    ax.set_ylabel("Station Latitude", fontsize=16)
    ax.set_title("Station Location by Line", fontsize=20)
    save_fig(fig_id="geo_chart(1)")
    fig.show()


'''
Plots a scatter plot of the location (latitude by longitude) over an administrative map of the NYC area
and sorts by Division using hue. File is saved using save_fig() function.
'''
def plot_street_map_three(subway_df_update):
    street_map = SHAPE_FILE
    # Creates bounds for the shape file
    bbox = (subway_df_update['Station Longitude'].min(), subway_df_update['Station Longitude'].max(),
            subway_df_update['Station Latitude'].min(), subway_df_update['Station Latitude'].max())
    x = subway_df_update['Station Longitude']
    y = subway_df_update['Station Latitude']
    sort_hue = subway_df_update['Division']

    fig, ax = plt.subplots(figsize=(12, 15))
    street_map.plot(ax=ax, color='black')
    ax.set_xlim(bbox[0] - 0.005, bbox[1] + 0.005)
    ax.set_ylim(bbox[2] - 0.005, bbox[3] + 0.005)
    sns.scatterplot(x, y, hue=sort_hue, ax=ax)
    ax.legend(bbox_to_anchor=(1.11, 1), borderaxespad=0)
    ax.set_xlabel("Station Longitude  \n\n\n"
                  "This scatter plot shows each subway station's location on a road map. Each division has a different "
                  "hue.",
                  fontsize=16)
    ax.set_ylabel("Station Latitude", fontsize=16)
    ax.set_title("Station Location by Division", fontsize=20)
    save_fig(fig_id="geo_chart(2)")
    fig.show()


'''
Name of file (fig_id) is passed in when calledfrom the plot functions. Creates a png file in the project folder.
'''
def save_fig(fig_id, tight_layout=True, fig_extension="png", resolution=300):
    path = fig_id + "." + fig_extension
    print("Saving figure", fig_id)
    if tight_layout:
        plt.tight_layout()
    plt.savefig(path, format=fig_extension, dpi=resolution)


if __name__ == '__main__':
    main()

