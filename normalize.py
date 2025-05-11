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

fileAdr = './Hackathon/merged/allAdresses.csv'
adrDF = pd.read_csv(fileAdr, delimiter=',')
adrDF['latInt'] = pd.to_numeric(40*adrDF['latitude'], downcast='integer').round()
adrDF['lngInt'] = pd.to_numeric(40*adrDF['longitude'], downcast='integer').round() 
adrDF = adrDF.groupby(['latInt','lngInt']).agg({'count_adr':np.sum}).sort_values(['latInt','lngInt']).reset_index()  


#rivers_10m = cfeature.NaturalEarthFeature('physical', 'rivers_lake_centerlines', '10m')
#rivers_europe_10m = cfeature.NaturalEarthFeature('physical', 'rivers_europe', '10m')

fileSolar = './Hackathon/merged/nexigoSolar.csv'
locationsDF = pd.read_csv(fileSolar, delimiter=',')
locationsDF = locationsDF.rename(columns={'vereinbarte Anschlusswirkleistung [kW]': "power"})
locationsDF[locationsDF['year_solar'].isna()]['year_solar'] = 1900
locationsDF[locationsDF['power'].isna()]['power'] = 0
print(locationsDF.columns.values) 

solarDF = locationsDF.groupby(['year_solar','month_solar']).agg({'power':np.sum}).sort_values(['year_solar','month_solar']).reset_index()
print(solarDF)

locationsDF['power_rel'] = 0.0
for index, column in locationsDF.iterrows():
  total = solarDF[np.logical_and(solarDF['year_solar']==column['year_solar'], solarDF['month_solar']==column['month_solar'])]['power'].sum()
  powerRel = 0.0
  if(total>0.0):
    powerRel = column['power']/total
  locationsDF.loc[index,'power_rel'] = powerRel
  

locationsDF['latInt'] = pd.to_numeric(40*locationsDF['latitude'], downcast='integer').round()
locationsDF['lngInt'] = pd.to_numeric(40*locationsDF['longitude'], downcast='integer').round()
  
  
  
nexigoDF = locationsDF.groupby(['latInt','lngInt']).agg({'count_nexiga':np.sum, 'kk_mio':np.sum}).sort_values(['latInt','lngInt']).reset_index()
print(nexigoDF)   
lcgcharDF = locationsDF.groupby(['latInt','lngInt','lcgchar']).agg({'count_nexiga':np.sum}).sort_values(['latInt','lngInt']).reset_index()
print(lcgcharDF)    
lcschichtDF = locationsDF.groupby(['latInt','lngInt','lcschicht']).agg({'count_nexiga':np.sum}).sort_values(['latInt','lngInt']).reset_index()
print(lcgcharDF)   

'''
for i in arange(1,10):
  locationsDF['lcgchar_'+str(i)+'_rel'] = 0.0
for i in arange(1,5):
  locationsDF['lcschicht_'+str(i)+'_rel'] = 0.0
locationsDF['kk_mio_rel'] = 0.0  
for index, column in locationsDF.iterrows():
   nexLatLongDF = nexigoDF[np.logical_and(nexigoDF['latInt']==column['latInt'], nexigoDF['lngInt']==column['lngInt'])]
   nTotal = nexLatLongDF['count_nexigo'].sum()
   kkTotal = nexLatLongDF['kk_mio'].sum()
   kkRel = 0.0
   if(kkTotal>0):
      kkRel = column['kk_mio']/kkTotal
   locationsDF.loc[index,'kk_mio_rel'] = kkRel  
   for i in arange(1,10):  
     relLcgcha = 0.0  
     nLcgchar = nexLatLongDF[nexLatLongDF['lcgchar']==i]['count_nexigo'].sum()
     if(nTotal>0):
        relLcgcha = nLcgchar/nTotal 
     locationsDF.loc[index,'lcgchar_'+str(i)+'_rel'] = relLcgcha    
   for i in arange(1,5):  
     relLcschicht = 0.0  
     nLcschicht = nexLatLongDF[nexLatLongDF['lcschicht']==i]['count_nexigo'].sum()
     if(nTotal>0):
        relLcschicht = nLcschicht/nTotal 
     locationsDF.loc[index,'lcschicht_'+str(i)+'_rel'] = relLcschicht  
'''
     
collectedNorm = {}        
counter = 0
for latI in np.arange(locationsDF['latInt'].min(),1+locationsDF['latInt'].max()):
  for lngI in np.arange(locationsDF['lngInt'].min(),1+locationsDF['lngInt'].max()):
    nexLatLongDF = nexigoDF[np.logical_and(nexigoDF['latInt']==latI, nexigoDF['lngInt']==lngI)]
    
    cgCharLatLongDF = lcgcharDF[np.logical_and(lcgcharDF['latInt']==latI, lcgcharDF['lngInt']==lngI)]
    cgSchichtLatLongDF = lcschichtDF[np.logical_and(lcgcharDF['latInt']==latI, lcgcharDF['lngInt']==lngI)]
    
    
    adrLatLongDF = adrDF[np.logical_and(adrDF['latInt']==latI, adrDF['lngInt']==lngI)]
    locLatLongDF = locationsDF[np.logical_and(locationsDF['latInt']==latI, locationsDF['lngInt']==lngI)]
    kkRel = nexLatLongDF['kk_mio'].sum()/nexigoDF['kk_mio'].sum()
    nRel = adrLatLongDF['count_adr'].sum()/adrDF['count_adr'].sum()
    nTotal = nexLatLongDF['count_nexiga'].sum()
    baseData = {'latI':latI,'lngI':lngI,'latitude':latI/40,'longitude':lngI/40,'kk_mio_rel':kkRel, 'nRel':nRel, 'nAbs':adrLatLongDF['count_adr'].sum()}
    print(nexLatLongDF.columns.values)
    for i in np.arange(1,10):  
     relLcgcha = 0.0  
     nLcgchar = cgCharLatLongDF[cgCharLatLongDF['lcgchar']==i]['count_nexiga'].sum()
     if(nTotal>0):
        relLcgcha = nLcgchar/nTotal 
     baseData['lcgchar_'+str(i)+'_rel'] = relLcgcha    
    for i in np.arange(1,5):  
     relLcschicht = 0.0  
     nLcschicht = cgSchichtLatLongDF[cgSchichtLatLongDF['lcschicht']==i]['count_nexiga'].sum()
     if(nTotal>0):
        relLcschicht = nLcschicht/nTotal 
     baseData['lcschicht_'+str(i)+'_rel'] = relLcschicht     
    
    
    for year in np.arange(1990,2025):
       baseData['year'] = year
       locYearPresent = locLatLongDF[locLatLongDF['year_solar']==year]
       locYearPast = locLatLongDF[locLatLongDF['year_solar']<year]
       powerNew = locYearPresent['power_rel'].sum()
       baseData['power_new'] = powerNew
       powerExist = locYearPast['power_rel'].sum()
       baseData['power_exist'] = powerExist    
       collectedNorm[counter] = baseData.copy()
       counter += 1  
       
print(collectedNorm)              
collectedDF = pd.DataFrame.from_dict(collectedNorm, orient='index')   #columns=[]
print(collectedDF)
collectedDF.to_csv(DATA_PATH / "collectedNorm.csv", index=True)          

