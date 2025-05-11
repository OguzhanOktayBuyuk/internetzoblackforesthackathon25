import pandas as pd
import numpy as np
import numbers
import math
import random

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns

import cartopy
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.img_tiles as cimgt
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

import io
from urllib.request import urlopen, Request
from PIL import Image

import folium
import webbrowser
from folium.plugins import HeatMap

from pathlib import Path
import os.path

DATA_PATH = Path.cwd()


from cartopy.io.img_tiles import OSM


#adapt limits and zoom-level (scale) according to data
limits = {'latMin':35.0, 'latMax':65.0, 'lonMin':-10.0, 'lonMax':30.0}
scale = 10

labels = [{'lon':6.08342, 'lat':50.77664,  'name':"Aachen"},
          {'lon':6.95,'lat':50.93333,'name':"Cologne"},
          {'lon':7.09549,'lat':50.73438,'name':"Bonn"},
          {'lon':7.14816,'lat':51.25627,'name':"Wuppertal"},
          {'lon':7.466,'lat':51.51494,'name':"Dortmund"}, 
          {'lon':7.62571,'lat':51.96236,'name':"Münster"}, 
          {'lon':6.79387,'lat':50.81481,'name':"Erftstadt"}, 
          {'lon':6.95,'lat':50.33333,'name':"Nürburg"}, 
          {'lon':7.57883,'lat':50.35357,'name':"Koblenz"},
          {'lon':6.66667,'lat':50.25,'name':"Eifel"}, 
          {'lon':7.09549,'lat':50.54169,'name':"Ahrweiler"}
]

#rivers_10m = cfeature.NaturalEarthFeature('physical', 'rivers_lake_centerlines', '10m')
#rivers_europe_10m = cfeature.NaturalEarthFeature('physical', 'rivers_europe', '10m')

fileSolar = './Hackathon/merged/nexigoSolar.csv'
locationsDF = pd.read_csv(fileSolar, delimiter=',')
locationsDF = locationsDF.rename(columns={'vereinbarte Anschlusswirkleistung [kW]': "power"})
print(locationsDF.columns.values) 
locationsDF = locationsDF[locationsDF['power'].notna()]

filterYear = 1990

locationsDF = locationsDF[locationsDF['year_solar']>1980]

print(locationsDF['year_solar'].min())
print(locationsDF['year_solar'].max())

print(locationsDF['power'].min())
print(locationsDF['power'].max())
maxPower = locationsDF['power'].max()
locationsDF = locationsDF[locationsDF['year_solar']<=filterYear].sort_values(['year_solar']).reset_index()
print(locationsDF)


print(locationsDF['latitude'].min())
print(locationsDF['latitude'].max())
print(locationsDF['longitude'].min())
print(locationsDF['longitude'].max())


limits = {'latMin':47.6, 'latMax':48.3, 'lonMin':7.5, 'lonMax':8.4}

def image_spoof(self, tile): 
    url = self._image_url(tile) 
    req = Request(url) 
    req.add_header('User-agent','Anaconda 3') 
    fh = urlopen(req) 
    im_data = io.BytesIO(fh.read()) 
    fh.close() 
    img = Image.open(im_data) 
    img = img.convert(self.desired_tile_form) 
    return img, self.tileextent(tile), 'lower' 

#cartopy OSM
osm_tiles = OSM()

plt.figure(figsize=(16, 16))

# Use the tile's projection for the underlying map.
ax1 = plt.axes(projection=osm_tiles.crs)

ax1.set_title('Photo Voltaic Density Map '+str(filterYear),fontsize=18)
extent = [limits['lonMin'], limits['lonMax'], limits['latMin'], limits['latMax']] 
ax1.set_extent(extent)
ax1.set_xticks(np.linspace(limits['lonMin'],limits['lonMax'],9),crs=ccrs.PlateCarree()) 
ax1.set_yticks(np.linspace(limits['latMin'],limits['latMax'],7)[1:],crs=ccrs.PlateCarree()) 
lon_formatter = LongitudeFormatter(number_format='0.2f',degree_symbol='',dateline_direction_label=True)
lat_formatter = LatitudeFormatter(number_format='0.2f',degree_symbol='') 
ax1.xaxis.set_major_formatter(lon_formatter) 
ax1.yaxis.set_major_formatter(lat_formatter) 
ax1.xaxis.set_tick_params(labelsize=14)
ax1.yaxis.set_tick_params(labelsize=14)
# add OSM with zoom specification
ax1.add_image(osm_tiles, scale)

#maxCount = np.max(locationsDF['count'])
lat1,long1,size1 = [],[],[]

for index, column in locationsDF.iterrows():
  if(isinstance(column['longitude'], numbers.Number) and isinstance(column['latitude'], numbers.Number)):
    if((limits['latMin']<column['latitude']<limits['latMax']) and (limits['lonMin']<column['longitude']<limits['lonMax'])):
        delta = 0.0
        counter = 1
        factor = 0.5 + (pow(column['power'],1/3)/pow(maxPower,1/3))
        for i in range(counter):
          x=column['longitude']
          y=column['latitude']
          lat1.append(x)
          long1.append(y)
          if(column['year_solar']<filterYear):
            ax1.plot(x, y, markersize=int(1+factor*12),marker='o',
                    linestyle='', markeredgecolor=None,
                    color='#2233aa', alpha=factor*0.6,transform=ccrs.PlateCarree()) 
          else:
            ax1.plot(x, y, markersize=int(1+factor*10),marker='o',
                    linestyle='', markeredgecolor=None,
                    color='#aa3322', alpha=factor*0.8,transform=ccrs.PlateCarree())                                        
 
                    
#contour-plot
##  sns.kdeplot(x=lat1, y=long1, fill=False,  levels=10, thresh=.0005, color='grey', transform=ccrs.PlateCarree()  )  
## ax1.add_feature(rivers_10m, facecolor='None', edgecolor='cyan', linewidth=1.5, zorder=2)
## ax1.add_feature(rivers_europe_10m, facecolor='None', edgecolor='red', linewidth=1.5, zorder=2)

if(not os.path.exists(DATA_PATH / 'img')):
    os.mkdir(DATA_PATH / 'img')
plt.savefig(DATA_PATH / 'img' / ('solar_heatmap_'+str(filterYear)+'.png'), dpi=300)


