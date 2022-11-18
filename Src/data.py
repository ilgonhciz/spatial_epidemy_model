import json
import rasterio


def load_sbb_data():
    with open("Data/switzerland_data/linie-mit-polygon_short.json") as f:
        sbb_data = json.load(f)
    return sbb_data

def load_population(country = "CH"):
    population = None 
    if country == "CH":
        CH_raster = rasterio.open('Data/switzerland_data/che_ppp_2020_UNadj.tif')
        CH_population = CH_raster.read(1)
        CH_population[CH_population<0] = None
        population = CH_population 
    elif country == "China":
        CH_raster = rasterio.open('Data/china/chn_ppp_2020_1km_Aggregated_UNadj.tif')
        CH_population = CH_raster.read(1)
        CH_population[CH_population<0] = None
        population = CH_population 
    elif country == "USA":
        CH_raster = rasterio.open('Data/USA/usa_ppp_2020_1km_Aggregated_UNadj.tif')
        CH_population = CH_raster.read(1)
        CH_population[CH_population<0] = None
        population = CH_population 

    return CH_raster,population 

