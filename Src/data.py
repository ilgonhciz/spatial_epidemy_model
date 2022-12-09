import json
import rasterio
import pandas
from utils import timeit
from file import parameters_config

@timeit
def load_sbb_data():
    with open("Data/switzerland_data/linie-mit-polygon.json") as f:
        sbb_data = json.load(f)
    return sbb_data

@timeit
def load_population(country = "CH"):
    population = None 
    if country == "CH":
        CH_raster = rasterio.open('Data/switzerland_data/che_ppp_2020_UNadj.tif')
        CH_population = CH_raster.read(1)
        CH_population[CH_population<parameters_config['data']['cutoff_density']] = 0
        population = CH_population 
    elif country == "China":
        CH_raster = rasterio.open('Data/china/chn_ppp_2020_1km_Aggregated_UNadj.tif')
        CH_population = CH_raster.read(1)
        CH_population[CH_population<parameters_config['data']['cutoff_density']] = 0
        population = CH_population 
    elif country == "USA":
        CH_raster = rasterio.open('Data/USA/usa_ppp_2020_1km_Aggregated_UNadj.tif')
        CH_population = CH_raster.read(1)
        CH_population[CH_population<parameters_config['data']['cutoff_density']] = 0
        population = CH_population 

    return CH_raster,population 

def load_USA_airport_data(): #loads the CSV for major U.S. airports including location (city + coordinates), name, and IATA code
    USA_airport_data = pandas.read_csv("Data/USA/major_airports_USA.csv")
    return USA_airport_data

def load_USA_airroutes_data(): #loads the CSV for air routes between major U.S. airports including source and destination IATA codes
    USA_airroutes_data = pandas.read_csv("Data/USA/major_routes_USA.csv")
    return USA_airroutes_data

if __name__ == "__main__":
    us_airport_pos = load_USA_airport_data()
    us_flight_route = load_USA_airroutes_data()
    print("Finish loading")
    
