import geopandas
import fiona
import pandas as pd
#from geodatasets import get_path

#path_to_data = get_path("nybb")
#gdf = geopandas.read_file("Hackathon/Wärmepumpen.xlsx")
wp = pd.read_excel("Hackathon/Wärmepumpen.xlsx", sheet_name='Tabelle1')
wp = wp[['Typ','Einbaudatum','Gemeinde','Leistung']]

# typ,Einbaudatum,Gemeinde,Leistung


print(wp)


gdf = geopandas.read_file("Hackathon/Strom ST MS-Freileitungsabschnitt BP Position.shp")
#gdf = gdf.to_crs(epsg=4326)
print('gdf')
print(gdf.columns.values)
print(gdf.crs)
print(gdf)

print(gdf['ORT'])

nexiga = geopandas.read_file("Hackathon/Datenquellen/Nexiga Daten/nexiga_all.shp")
print('nexiga')
print(nexiga.columns.values)
print(nexiga)


#3_uid_' 'id' 'v_lfd' 'v_dat_adm' 'v_dat_post' 'kgs44' 'his' 'kgs36'
# 'kgs22' 'ags' 'kgs22_name' 
# 'kgs8_name'   Gemeinde
# 'plz' 'mplz' 'po_name' 'pot_name'
# 'str_name' 'hnr' 'hnr_zs' 'hnr_kompl' 'hnr_typ' 
# 'lcew'  
# 'lchh'    Haushalte
# 'kk_mio'   kaufkraft?
# 'lcewewa'   Wechsel Waerme Wahrscheinlichkeit 0 .. 100
# 'lcewb' Waermebedarf  kWh


# 'nx_x_etrsu', 'nx_y_etrsu', 'nx_kenn'   Koordinaten ?

# 'kk_kat' 'dskz' 'kk_idx' 
# 'lcgchar' Haustyp                 int
# 'lcbjkl'  Baujahr                 int
# 'lcschicht' 'lcalter'
# 'lckumw'     Umweltaffinitaet    int
# 'lckpre'     Preisaffinitaet     int
# 'lckneu' 'lcewb' 
# 'lceemob'   Affinitaet electro   int
# 'geometry'
# '''


nexiga = nexiga[['kgs8_name', 'str_name', 'hnr', 'geometry', 'lcewewa', 'lcewb', 'lchh', 'kk_mio', 'lcgchar', 'lcbjkl', 'lcschicht', 'lckumw', 'lckpre', 'lceemob']] 
##nexiga = nexiga.to_crs(epsg=4326)
print(nexiga[['kgs8_name', 'str_name', 'hnr', 'geometry',  ]])

for col in ['lchh', 'hnr', 'lcgchar', 'lcbjkl', 'lcschicht', 'lckumw', 'lckpre', 'lceemob']:
  nexiga[col] = pd.to_numeric(nexiga[col], downcast='integer')


#https://gis.stackexchange.com/questions/222315/finding-nearest-point-in-other-geodataframe-using-geopandas


adr = pd.read_csv("Hackathon/Datenquellen/Hauskoordinaten/adressen_bw.txt", sep=";")
print('adressen')

print(adr)
print(adr.columns.values)
print(adr[['gmd','str','hnr','ostwert','nordwert']])

allAdresses = adr[['gmd','str','hnr','ostwert','nordwert']]


allAdresses = geopandas.GeoDataFrame(
    allAdresses, geometry=geopandas.points_from_xy(allAdresses.ostwert, allAdresses.nordwert), crs="EPSG:25832"
)


##allAdresses = allAdresses.to_crs(epsg=4326)
print(allAdresses.dropna())


allAdresses = geopandas.sjoin_nearest(allAdresses, nexiga, how='left', max_distance=20.0, lsuffix='adr', rsuffix='nexiga', distance_col='dist_adr_nexiga')

print(allAdresses.columns.values)
print(allAdresses[['gmd','str','hnr_adr', 'str_name', 'hnr_nexiga', 'dist_adr_nexiga']])

allAdresses['valid_adr_nexiga'] = allAdresses['hnr_adr'] == allAdresses['hnr_nexiga']

notna = allAdresses.dropna()
print(notna[['gmd','str','hnr_adr', 'str_name', 'hnr_nexiga', 'dist_adr_nexiga', 'valid_adr_nexiga']])



solar = geopandas.read_file("Hackathon/Strom-Einspeiser-Export 1.csv", sep=';', encoding='latin_1', crs='4326', geometry='B Position')
print(solar['B Position'])
##solar = geopandas.GeoDataFrame(solar, geometry = 'B Position', crs="EPSG:4326")

coords = solar['B Position'].str.replace('POINT(', '', regex=False)
coords = coords.str.replace(')', '', regex=False)
coords = coords.str.split(' ',expand=True)
print(coords)
solar['longitude'] = pd.to_numeric(coords[0], downcast='float')
solar['latitude'] = pd.to_numeric(coords[1], downcast='float')
solar = geopandas.GeoDataFrame(solar, geometry = geopandas.points_from_xy(solar.longitude, solar.latitude), crs="EPSG:4326")
solar = solar.to_crs(epsg=25832)
print('solar')
print(solar.columns.values)
print(solar)

solar = solar[['Einbaudatum', 'Gemeinde', 'Straße', 'Hausnummer', 'Betriebsspannung [kV]', 'vereinbarte Anschlusswirkleistung [kW]', '(Peak-)Leistung [kW]', 'Umspannwerke (versorgend)', 'geometry']]

solar = solar.rename(columns={'Einbaudatum': "date_solar"})
dates = solar['date_solar'].str.split('.',expand=True)
print(dates)
solar['year_solar'] = pd.to_numeric(dates[2], downcast='integer')
solar['Hausnummer'] = pd.to_numeric(solar['Hausnummer'], downcast='integer', errors='coerce')

allAdresses = geopandas.sjoin_nearest(allAdresses, solar, how='left', max_distance=20.0, lsuffix='adr', rsuffix='solar', distance_col='dist_adr_solar')

print(allAdresses.columns.values)
print(allAdresses)

print(allAdresses[['gmd','str','hnr_adr', 'Straße', 'Hausnummer', 'dist_adr_solar']])

allAdresses['valid_adr_solar'] = allAdresses['hnr_adr'] == allAdresses['Hausnummer']

notna = allAdresses.dropna()
print(notna[['gmd','str','hnr_adr', 'Straße', 'Hausnummer', 'dist_adr_solar', 'valid_adr_solar']])



allAdresses = allAdresses[['gmd', 'str', 'hnr_adr', 'geometry', 'index_nexiga', 'lcewewa', 'lcewb', 'lchh', 'kk_mio', 'lcgchar', 'lcbjkl', 'lcschicht', 'lckumw', 'lckpre', 'lceemob', 'dist_adr_nexiga', 'valid_adr_nexiga','date_solar', 'Betriebsspannung [kV]', 'vereinbarte Anschlusswirkleistung [kW]', '(Peak-)Leistung [kW]', 'Umspannwerke (versorgend)', 'year_solar', 'dist_adr_solar']]
 
allAdresses.to_csv("allAdresses.csv")

notna = allAdresses.dropna()
notna.to_csv("validAdresses.csv")
notna.to_file("validAdresses.geojson", driver='GeoJSON')

