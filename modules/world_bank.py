# Import necessary libraries
import requests, folium, warnings, os, webbrowser
import pandas as pd
import geopandas as gpd
from branca.colormap import linear
import plotly.graph_objects as go

# Ignore warnings to keep the output clean
warnings.filterwarnings("ignore")

# Dictionary mapping indicator names to their corresponding World Bank codes
indicators = {
    'Agricultural land (% of land area)': 'AG.LND.AGRI.ZS',
    'Arable land (% of land area)': 'AG.LND.ARBL.ZS',
    'Forest area (% of land area)': 'AG.LND.FRST.ZS',
    'Land area (sq. km)': 'AG.LND.TOTL.K2',
    'Rural land area (sq. km)': 'AG.LND.TOTL.RU.K2',
    'Surface area (sq. km)': 'AG.SRF.TOTL.K2',
    'Primary completion rate (% of relevant age group)': 'SE.PRM.CMPT.ZS',
    'Net migration': 'SM.POP.NETM',
    'GDP (current US$)': 'NY.GDP.MKTP.CD',
    'GDP per capita (current US$)': 'NY.GDP.PCAP.CD',
    'Children out of school (% of primary school age)': 'SE.PRM.UNER.ZS',
    'Unemployment (% of total labor force) (modeled ILO estimate)': 'SL.UEM.TOTL.ZS',
    'Access to electricity (% of population)': 'EG.ELC.ACCS.ZS',
    'Renewable electricity output (% of total electricity output)': 'EG.ELC.RNEW.ZS',
    'Alternative and nuclear energy (% of total energy use)': 'EG.USE.COMM.CL.ZS',
    'Urban land area (sq. km)': 'AG.LND.TOTL.UR.K2',
    'Domestic credit to private sector by banks (% of GDP)': 'FD.AST.PRVT.GD.ZS',
    'Domestic credit to private sector (% of GDP)': 'GFDD.DI.14',
    'Suicide mortality rate (per 100,000 population)': 'SH.STA.SUIC.P5',
    'Life expectancy at birth (years)': 'SP.DYN.LE00.IN',
    'Population': 'SP.POP.TOTL',
    'International tourism, number of arrivals': 'ST.INT.ARVL',
    'High-technology exports (current US$)': 'TX.VAL.TECH.CD',
    'High-technology exports (% of manufactured exports)': 'TX.VAL.TECH.MF.ZS',
    'Human Capital Index': 'HD.HCI.OVRL',
    'Military expenditure (% of GDP)': 'MS.MIL.XPND.GD.ZS',
    'Research and development expenditure (% of GDP)': 'GB.XPD.RSDV.GD.ZS',
    'Trademark applications': 'IP.TMK.TOTL',
    'Researchers in R&D (per million people)': 'SP.POP.SCIE.RD.P6',
    'Technicians in R&D (per million people)': 'SP.POP.TECH.RD.P6',
    'Children in employment (% of children ages 7-14)': 'SL.TLF.0714.ZS',
    'Labor force participation rate (% of total population ages 15-64)': 'SL.TLF.ACTI.ZS'
}

# List of strings representing regions or groupings to exclude from data visualization
strings_to_exclude = [
    'Africa Eastern and Southern',
    'Africa Western and Central',
    'Arab World',
    'Caribbean small states',
    'Central Europe and the Baltics',
    'Early-demographic dividend',
    'East Asia & Pacific',
    'East Asia & Pacific (IDA & IBRD countries)',
    'East Asia & Pacific (excluding high income)',
    'Euro area',
    'Europe & Central Asia',
    'Europe & Central Asia (IDA & IBRD countries)',
    'Europe & Central Asia (excluding high income)',
    'European Union',
    'Fragile and conflict affected situations',
    'Heavily indebted poor countries (HIPC)',
    'High income',
    'IBRD only',
    'IDA & IBRD total',
    'IDA blend',
    'IDA only',
    'IDA total',
    'Late-demographic dividend',
    'Latin America & Caribbean',
    'Latin America & Caribbean (excluding high income)',
    'Latin America & the Caribbean (IDA & IBRD countries)',
    'Least developed countries: UN classification',
    'Low & middle income',
    'Low income',
    'Lower middle income',
    'Middle East & North Africa',
    'Middle East & North Africa (IDA & IBRD countries)',
    'Middle East & North Africa (excluding high income)',
    'Middle income',
    'OECD members',
    'Other small states',
    'Pacific island small states',
    'Post-demographic dividend',
    'Pre-demographic dividend',
    'Small states',
    'South Asia (IDA & IBRD)',
    'Sub-Saharan Africa',
    'Sub-Saharan Africa (IDA & IBRD countries)',
    'Sub-Saharan Africa (excluding high income)',
    'Upper middle income',
    'World',
    'South Asia',
    'North America'
]

# Function to fetch country-level data for a given indicator ID from the World Bank API
def get_country_data_for_indicator(indicator_id):
    """
    Fetches country-level data for a specified indicator from the World Bank API.
    
    Parameters:
    indicator_id (str): The ID of the indicator to fetch data for.
    
    Returns:
    list or None: A list of filtered data entries if the request is successful and data is in the expected format, 
    or None if there is an error or unexpected data structure.
    
    This function constructs the API request URL using the provided indicator ID, specifies the desired parameters 
    (data format as JSON, date range from 1960 to 2023, and a large page size to include all data), and sends 
    the request to the World Bank API. If the response is successful (HTTP status code 200) and the data is in 
    the expected format, it filters out entries for excluded countries and entries with None values for the indicator. 
    If the response status code is not 200 or the data structure is not as expected, it prints an error message and 
    returns None.
    """
    url = f'https://api.worldbank.org/v2/country/all/indicator/{indicator_id}'
    params = {
        'format': 'json',
        'date': '1960:2023',
        'per_page': 20000
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        # Check if the response is in the expected format and filter out excluded countries and None values
        if isinstance(data, list) and len(data) > 1 and 'country' in data[1][0]:
            filtered_data = [
                entry for entry in data[1]
                if entry['country']['value'] not in strings_to_exclude and entry['value'] is not None
            ]
            return filtered_data
        else:
            print(f'\nError {indicator_id}: Unexpected data structure')
            return None
    else:
        print(f'\nError {indicator_id}: {response.status_code}')
        return None

# Function to plot time series data using Plotly, saving as an interactive HTML file
def plot_time_series(df, title='', template='plotly'):
    """
    Plots time series data using Plotly and saves the plot as an interactive HTML file.
    
    Parameters:
    df (pandas.DataFrame): The DataFrame containing the time series data with columns 'DATE' and 'VALUE'.
    title (str, optional): The title of the plot. Default is an empty string.
    template (str, optional): The Plotly template to use for the plot. Default is 'plotly'.
    
    This function converts the 'DATE' column in the DataFrame to datetime format and extracts the year. 
    It then creates a Plotly figure with a time series plot (lines and markers) using the 'DATE' and 'VALUE' 
    columns from the DataFrame. The plot is customized with a title and axis labels. The resulting plot is saved 
    as an HTML file in the 'downloads' folder and opened in the default web browser.
    """
    # Convert DATE column to datetime format and extract year
    df['DATE'] = pd.to_datetime(df['DATE'])
    df['DATE'] = df['DATE'].dt.year
    
    # Create a Plotly figure with time series data, customize axes and add title
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['DATE'], y=df['VALUE'], mode='lines+markers', name='Data'))

    fig.update_layout(
        title=title,
        xaxis_title='Year',
        yaxis_title='Value',
        template=template
    )
    
    # Save the interactive Plotly figure as an HTML file and open it in the default web browser
    downloads_folder = 'static/temp_images/world_bank/'
    if not os.path.exists(downloads_folder):
        os.makedirs(downloads_folder)
    temp_html_path = os.path.join(downloads_folder, 'time_series.html')
    fig.write_html(temp_html_path)
    webbrowser.open('file://' + os.path.realpath(temp_html_path))

# Function to plot a heatmap using Folium and GeoPandas, saving as an interactive HTML file
def plot_heatmap(df):
    """
    Plots a heatmap using Folium and GeoPandas, and saves the map as an interactive HTML file.
    
    Parameters:
    df (pandas.DataFrame): The DataFrame containing the data with columns 'COUNTRY', 'DATE', 'ISO_CODE', and 'VALUE'.
    
    This function filters the DataFrame to include only the latest data for each country. It loads the world shapefile 
    from GeoPandas and ensures the country names are in English. The shapefile is merged with the DataFrame's data 
    on country ISO codes. A base Folium map is created and country polygons are added with colors based on data values. 
    A colormap is created and added to the map, which is then saved as an HTML file in the 'downloads' folder and 
    opened in the default web browser.
    """
    # Filter the DataFrame to include only the latest data per country
    df = df.loc[df.groupby('COUNTRY')['DATE'].idxmax()]
    df['DATE'] = pd.to_datetime(df['DATE'])
    
    # Load the world shapefile from GeoPandas
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    
    # Ensure country names are in English
    world = world[['iso_a3', 'geometry', 'name']]
    
    # Merge the world shapefile with the DataFrame's data
    world = world.merge(df, how='left', left_on='iso_a3', right_on='ISO_CODE')
    
    # Create a base Folium map
    m = folium.Map(location=[20, 0], zoom_start=2)
    
    # Create and add the colormap
    colormap = linear.YlOrRd_09.scale(df['VALUE'].min(), df['VALUE'].max())
    colormap.caption = 'Value by Country'
    
    # Add country polygons to the map with color based on data values
    for _, row in world.iterrows():
        if pd.notna(row['VALUE']):
            formatted_value = '{:,}'.format(round(row['VALUE'], 2))
            geo_json = folium.GeoJson(
                row['geometry'],
                style_function=lambda x, value=row['VALUE']: {
                    'fillColor': colormap(value),
                    'color': 'black',
                    'weight': 0.5,
                    'fillOpacity': value / df['VALUE'].max()
                }
            )
            geo_json.add_child(folium.Tooltip(f"{row['name']} ({row['DATE'].year}): {formatted_value}"))
            geo_json.add_to(m)
    
    colormap.add_to(m)
    
    # Save the interactive Folium map as an HTML file and open it in the default web browser
    downloads_folder = 'static/temp_images/world_bank/'
    if not os.path.exists(downloads_folder):
        os.makedirs(downloads_folder)
    temp_html_path = os.path.join(downloads_folder, 'heatmap.html')
    m.save(temp_html_path)
    webbrowser.open('file://' + os.path.realpath(temp_html_path))
