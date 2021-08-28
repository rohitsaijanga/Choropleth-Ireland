import pandas as pd
path = '~/Projects/Choropleth-map-Ireland/'
shppath = '~/Projects/Choropleth-map-Ireland/shp/'
df = pd.read_csv(path+'WindDataAggregated.csv')
import fiona as fio
import geopandas as gpd
ROI_map= gpd.read_file(shppath+'IrelandMap.shp')
ROI_map.head()
ROI_map=ROI_map.set_index('DIVISION')
df=df.set_index('County')
df2= ROI_map.join(df)
# we need to replace NaN rows with 0 since there are some counties without any wind turbines 
df2['Installed Capacity (MW)']=df2['Installed Capacity (MW)'].fillna(value=0)
df2['No of Turbines']=df2['No of Turbines'].fillna(value=0)
df2['name1'] = df2.index
MAP=df2
#MAP['test2']=MAP['No of Turbines']/189
variable = 'Installed Capacity (MW)'
vmin, vmax = 0, 700
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(8,10),facecolor='lightsteelblue')
fig=MAP.plot(column='Installed Capacity (MW)', cmap='YlGn', linewidth=0.8, ax=ax, edgecolor='#140656',facecolor='lightslategray',vmin=vmin, vmax=vmax, legend=True, norm=plt.Normalize(vmin=vmin, vmax=vmax))
ax.axis('off')
ax.annotate('Installed Capacity (MW)',xy=(0.9, .65),rotation=270, xycoords='figure fraction', horizontalalignment='left', verticalalignment='top', fontsize=12, color='black')

#Getting the lan and lat here from geometry data    
MAP['coords']=MAP['geometry'].apply(lambda x: x.representative_point().coords[:])
MAP['coords']=[coords[0] for coords in MAP['coords']]

from random import gauss

# Add turbine numbers here
for _, row in df2.iterrows():
    if row['No of Turbines']!=0:
        s=row['No of Turbines']
        ss=int(s)
        for i in list(range(ss)):
            DFF=plt.scatter(x=row['coords'][0]+gauss(0, 0.1),y=gauss(0, 0.3)+row['coords'][1],c='#ec1313',alpha=0.5,s=ss*3)

# Add names of county here
for _, row in MAP.iterrows():
    switcher = {
        "Galway":"Galway",
        "DMR East": "",
        "DMR North": "",
        "DMR North Central": "",
        "DMR South":"",
        "DMR South Central":"",
        "DMR West":'Dublin',
        "Kildare":"Kildare",
        "Laois/Offaly":"Laois/Offaly",
        "Meath":"Meath",
        "Westmeath":"Westmeath",
        "Wicklow":"Wicklow",
        "Cavan/Monaghan":"Cavan/Monaghan",
        "Donegal":"Donegal",
        "Louth":"Louth",
        "Sligo/Leitrim":"Sligo/Leitrim",
        "Kilkenny/Carlow":"Kilkenny/Carlow",
        "Tipperary":"Tipperary",
        "Waterford":"Waterford",
        "Wexford":"Wexford",
        "Cork City":"Cork",
        "Cork North":"",
        "Cork West":"",
        "Kerry":"Kerry",
        "Limerick":"Limerick",
        "Clare":"Clare",
        "Mayo":"Mayo",
        "Roscommon/Longford":"Roscommon/Longford",
    }
    plt.annotate(text=switcher.get(row['name1']), xy=row['coords'],
                 horizontalalignment='center', color='black',fontsize=10, fontweight='light')

#Add legend to red circles i.e. wind turbines
plt.legend([DFF, DFF], ["Wind turbines"],loc='upper left')
    
import os 
filepath = os.path.join(path,'IrishMapNew.jpg')
chart = fig.get_figure()
chart.savefig(filepath, dpi=300)