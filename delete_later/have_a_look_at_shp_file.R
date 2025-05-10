# ______________________________________________________
# Packages, workspace, data for general purposes etc.
library(tidyverse)
library(rgdal) # for readOGR()
library(leaflet)
library(sf)

# Import
# ______________________________________________________
path_grid <- 
  "C:/Projekte/studium/08_SS2025/blackforesthackaton/internetzoblackforesthackathon25/Hackathon/Strom ST MS-Kabelabschnitt BP Position.shp"
path_nexiga <- 
  "C:/Projekte/studium/08_SS2025/blackforesthackaton/internetzoblackforesthackathon25/Hackathon/Daten Hackaton (ALKIS,Nexiga,PV,HK)/Datenquellen/Nexiga Daten/nexiga_all.shp"

nexiga <-
  rgdal::readOGR(dsn = path_nexiga,
                 layer = "nexiga_all",
                 use_iconv = TRUE,
                 encoding = "UTF-8")

grid <-
  rgdal::readOGR(dsn = path_grid,
                 layer = "Strom ST MS-Kabelabschnitt BP Position",
                 use_iconv = TRUE,
                 encoding = "UTF-8")

grid@data %>% View()

# look at the data
# ______________________________________________________
nexiga@data %>% head() %>% View()

nexiga@data %>% 
  filter(
    str_detect(str_name, "Harriet-Straub"),
    hnr == 27
  ) %>% 
  select(lchh) %>% 
  View()

# change the crs
# ______________________________________________________
nexiga_crs <- 
  spTransform(nexiga, CRS("+proj=longlat +datum=WGS84 +no_defs +ellps=WGS84 +towgs84=0,0,0"))

# look at the data
# ______________________________________________________
nexiga %>% 
  leaflet() %>%
  addTiles() %>%
  addCircles(
    lng = nexiga$nx_x_etrsu,
    lat = nexiga$nx_y_etrsu,
  ) %>% 
  addHeatmap(
    lng = .$nx_x_etrsu,
    lat = .$nx_y_etrsu,
    radius = 25,
    blur = 15
  )

