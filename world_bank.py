#%% DOWNLOADING DATA

indicators = {
    'Agricultural land (% of land area)': 'AG.LND.AGRI.ZS',
    'Arable land (% of land area)': 'AG.LND.ARBL.ZS',
    'Forest area (% of land area)': 'AG.LND.FRST.ZS',
    'Land area (sq. km)': 'AG.LND.TOTL.K2',
    'Rural land area (sq. km)': 'AG.LND.TOTL.RU.K2',
    'Surface area (sq. km)': 'AG.SRF.TOTL.K2',
    'Primary completion rate, total (% of relevant age group)': 'SE.PRM.CMPT.ZS',
    'Net migration': 'SM.POP.NETM',
    'Expense (% of GDP)': 'GC.XPN.TOTL.GD.ZS',
    'GDP (current US$)': 'NY.GDP.MKTP.CD',
    'GDP per capita (current US$)': 'NY.GDP.PCAP.CD',
    'Children out of school (% of primary school age)': 'SE.PRM.UNER.ZS',
    'Unemployment, total (% of total labor force) (modeled ILO estimate)': 'SL.UEM.TOTL.ZS',
    'Access to electricity (% of population)': 'EG.ELC.ACCS.ZS',
    'Renewable electricity output (% of total electricity output)': 'EG.ELC.RNEW.ZS',
    'Alternative and nuclear energy (% of total energy use)': 'EG.USE.COMM.CL.ZS',
    'Urban land area (sq. km)': 'AG.LND.TOTL.UR.K2',
    'Domestic credit to private sector by banks (% of GDP)': 'FD.AST.PRVT.GD.ZS',
    'Domestic credit to private sector (% of GDP)': 'GFDD.DI.14',
    'Suicide mortality rate (per 100,000 population)': 'SH.STA.SUIC.P5',
    'Life expectancy at birth, total (years)': 'SP.DYN.LE00.IN',
    'Population, total': 'SP.POP.TOTL',
    'Employees (%)': '9.0.Employee.All',
    'Employers (%)': '9.0.Employer.All',
    'Self-Employed (%)': '9.0.SelfEmp.All',
    'Unemployed (%)': '9.0.Unemp.All',
    'Unpaid Workers (%)': '9.0.Unpaid.All',
    'Coverage: Mobile Phone': '2.0.cov.Cel',
    'Coverage: Electricity': '2.0.cov.Ele',
    'Coverage: Mathematics Proficiency Level 2': '2.0.cov.Math.pl_2.all',
    'Coverage: Sanitation': '2.0.cov.San',
    'Coverage: Water': '2.0.cov.Wat',
    'International tourism, number of arrivals': 'ST.INT.ARVL',
    'High-technology exports (current US$)': 'TX.VAL.TECH.CD',
    'High-technology exports (% of manufactured exports)': 'TX.VAL.TECH.MF.ZS',
    'Human Capital Index (HCI) (scale 0-1)': 'HD.HCI.OVRL',
    'Military expenditure (% of GDP)': 'MS.MIL.XPND.GD.ZS',
    'Research and development expenditure (% of GDP)': 'GB.XPD.RSDV.GD.ZS',
    'Trademark applications, total': 'IP.TMK.TOTL',
    'Researchers in R&D (per million people)': 'SP.POP.SCIE.RD.P6',
    'Technicians in R&D (per million people)': 'SP.POP.TECH.RD.P6',
    'Children in employment, total (% of children ages 7-14)': 'SL.TLF.0714.ZS',
    'Labor force participation rate, total (% of total population ages 15-64) (modeled ILO estimate)': 'SL.TLF.ACTI.ZS'}

import requests, json
import pandas as pd
from tqdm import tqdm

# Función para obtener datos de un indicador a nivel país
def get_country_data_for_indicator(indicator_id):
    url = f'https://api.worldbank.org/v2/country/all/indicator/{indicator_id}'
    params = {
        'format': 'json',
        'date': '1960:2023',
        'per_page': 20000
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'\nError {indicator_id}: {response.status_code}')
        return None

data = {}
for key, value in tqdm(indicators.items()):
    data[key] = get_country_data_for_indicator(value)

#%% PREPROCESSING DATA

"""
hay que ver los datos que hay por tema. es probable que
algunos temas no valga la pena tenerlos.
"""

df=[]
for key in tqdm(list(data.keys())):
    try:
        for i in range(len(data[key][1])):
            
                df.append((
                    key,
                    data[key][1][i]['country']['value'],
                    data[key][1][i]['date'],
                    data[key][1][i]['value']))
    except: pass
df=pd.DataFrame(df,columns=['TOPIC','COUNTRY','DATE','VALUE']).dropna().drop_duplicates()
topics=df['TOPIC'].value_counts()[df['TOPIC'].value_counts()>200].index
df=df[df['TOPIC'].isin(topics)]

#%%

import pandas as pd
import geopandas as gpd
import folium
from branca.colormap import linear
import pycountry

def convert_country_name_to_english(country_name):
    try:
        country = pycountry.countries.get(name=country_name)
        if country:
            return country.name
        else:
            return country_name
    except:
        return country_name

df_ = df[df['TOPIC'] == 'Children in employment, total (% of children ages 7-14)']
df_['DATE'] = pd.to_datetime(df_['DATE'])
df_['VALUE'] = round(df_['VALUE'], 2)
df_ = df_.loc[df_.groupby('COUNTRY')['DATE'].idxmax()]
df_['COUNTRY'] = df_['COUNTRY'].apply(convert_country_name_to_english)

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
world = world.merge(df_, how='left', left_on='name', right_on='COUNTRY')

m = folium.Map(location=[20, 0], zoom_start=2)
colormap = linear.YlOrRd_09.scale(df_['VALUE'].min(), df_['VALUE'].max())
colormap.caption = 'Value by Country'
for _, row in world.iterrows():
    if pd.notna(row['VALUE']):
        geo_json = folium.GeoJson(
            row['geometry'],
            style_function=lambda x, value=row['VALUE']: {
                'fillColor': colormap(value),
                'color': 'black',
                'weight': 0.5,
                'fillOpacity': value / df_['VALUE'].max()
            }
        )
        geo_json.add_child(folium.Tooltip(f"{row['name']} ({row['DATE'].year}): {row['VALUE']}%"))
        geo_json.add_to(m)
colormap.add_to(m)
m.save('heatmap_mundial.html')



















































