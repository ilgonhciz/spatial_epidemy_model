import json
import rasterio


def load_sbb_data():
    with open("Data/switzerland_data/linie-mit-polygon.json") as f:
        sbb_data = json.load(f)
    return sbb_data

def load_population(country = "CH"):
    population = None 
    if country == "CH":
        CH_raster = rasterio.open('Data/switzerland_data/che_ppp_2020_UNadj.tif')
        CH_population = CH_raster.read(1)
        CH_population[CH_population<0] = -0.9
        population = CH_population 
    return CH_raster,population 