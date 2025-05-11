import pandas as pd
import numpy as np
import geopandas
import fiona

from pathlib import Path
import os.path
import io
import math
import requests

import matplotlib.pyplot as plt

DATA_PATH = Path.cwd()


fileSolar = './Hackathon/merged/nexigoSolar.csv'
solarDF = pd.read_csv(fileSolar, delimiter=',')
print(solarDF)


solarDF['year_solar'] = pd.to_numeric(solarDF['year_solar'], downcast='integer')
solarDF['lcschicht'] = pd.to_numeric(solarDF['lcschicht'], downcast='integer')
solarDF = solarDF[solarDF['year_solar']>1980]
solarDF = solarDF.rename(columns={'vereinbarte Anschlusswirkleistung [kW]': "power"})
print(solarDF['power'])
print(solarDF.columns.values)

prm = 'lcschicht'

solarDF = solarDF.groupby(['year_solar',prm]).agg({'power':np.sum}).sort_values(['year_solar',prm]).reset_index()
print(solarDF)



years = np.arange(solarDF['year_solar'].min(), 1+solarDF['year_solar'].max())
params = np.arange(solarDF[prm].min(), solarDF[prm].max())

print(params)

power = np.zeros((len(params), len(years)))
print(power)
y = 0
for year in years:
  p = 0
  for param in params:
    #print(solarDF[np.logical_and(solarDF['year_solar']==year, solarDF[prm]==param)])
    power[p,y] = solarDF[np.logical_and(solarDF['year_solar']==year, solarDF[prm]==param)]['power'].sum()
    p += 1
  y += 1   

print(power)

print(params.astype(str))

#seasonColors = addOpacity(['#555555','#FF8800','#0066cc'],0.7)
#seasonsAbs = {'Unknown':absBoth,'Summer':absSummers,'Winter':absWinters}
plt.rcdefaults()
fig, ax = plt.subplots(figsize=(40, 20))
ax.stackplot(years, power, labels=params.astype(str))
plt.xticks(fontsize=36)
plt.yticks(fontsize=36)
ax.set_title("Installed Power per year and param", fontsize=48)
ax.legend(fontsize=24, loc="center right", bbox_to_anchor=(1.1, 0.70) )
ax.set_xlabel('Year', fontsize=48)
ax.set_ylabel('Power', fontsize=48)
plt.legend(loc='upper left', bbox_to_anchor=(0.5,0.5))
plt.savefig(DATA_PATH / "img" / "years_solar.png", dpi=300)
#plt.show()
plt.close('all')  

