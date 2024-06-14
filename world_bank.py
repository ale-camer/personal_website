import requests, folium, warnings, os, webbrowser
import pandas as pd
import geopandas as gpd
from branca.colormap import linear
import plotly.graph_objects as go
warnings.filterwarnings("ignore")

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

def get_country_data_for_indicator(indicator_id):
    url = f'https://api.worldbank.org/v2/country/all/indicator/{indicator_id}'
    params = {
        'format': 'json',
        'date': '1960:2023',
        'per_page': 20000
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
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

def plot_time_series(df,title='',template='plotly'):
    
    df['DATE'] = pd.to_datetime(df['DATE'])
    df['DATE'] = df['DATE'].dt.year
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['DATE'], y=df['VALUE'], mode='lines+markers', name='Data'))

    fig.update_layout(
        title=title,
        xaxis_title='Year',
        yaxis_title='Value',
        template=template
    )
    
    downloads_folder = 'downloads'
    if not os.path.exists(downloads_folder):
        os.makedirs(downloads_folder)
    temp_html_path = os.path.join(downloads_folder, 'time_series.html')
    fig.write_html(temp_html_path)
    webbrowser.open('file://' + os.path.realpath(temp_html_path))

def plot_heatmap(df):
    # Filtrar el DataFrame para obtener las últimas fechas por país
    df = df.loc[df.groupby('COUNTRY')['DATE'].idxmax()]
    df['DATE'] = pd.to_datetime(df['DATE'])
    
    # Cargar el shapefile del mundo
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    
    # Asegurarse de que los nombres de los países estén en inglés
    world = world[['iso_a3', 'geometry', 'name']]
    
    # Realizar el merge con los datos del DataFrame
    world = world.merge(df, how='left', left_on='iso_a3', right_on='ISO_CODE')
    
    # Crear el mapa base
    m = folium.Map(location=[20, 0], zoom_start=2)
    
    # Crear y agregar el colormap
    colormap = linear.YlOrRd_09.scale(df['VALUE'].min(), df['VALUE'].max())
    colormap.caption = 'Value by Country'
    
    # Agregar los polígonos de los países al mapa
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
    
    downloads_folder = 'downloads'
    if not os.path.exists(downloads_folder):
        os.makedirs(downloads_folder)
    temp_html_path = os.path.join(downloads_folder, 'heatmap.html')
    m.save(temp_html_path)
    webbrowser.open('file://' + os.path.realpath(temp_html_path))