""" import geopandas
switzerland_administrative_boundaries = geopandas.read_file('Data/switzerland_data/che_ppp_2020_UNadj.shp')

vietnam_worldpop_raster_tot = vietnam_worldpop_raster.read(1)
vietnam_worldpop_raster_tot[vietnam_worldpop_raster_tot<0] = None
plt.rcParams['figure.figsize'] = 14, 14
plt.imshow(np.log10(vietnam_worldpop_raster_tot+1),)
bar = plt.colorbar(fraction=0.5)

print("hellopai") """   
import rasterio
import numpy as np
import matplotlib.pyplot as plt
import pySBB

switzerland_worldpop_raster = rasterio.open('Data/switzerland_data/che_ppp_2020_UNadj.tif')

switzerland_worldpop_raster_tot = switzerland_worldpop_raster.read(1)
switzerland_worldpop_raster_tot[switzerland_worldpop_raster_tot<0] = None
#plt.rcParams['figure.figsize'] = 14, 14
plt.imshow(np.log10(switzerland_worldpop_raster_tot+1),)
bar = plt.colorbar(fraction=0.05)
#plt.show()


connection = pySBB.get_connections("Brugg", "Basel", limit=1)[0]
for section in connection.sections:
    for passList in section.journey.passList:
        station = passList.station
        print("   {} {}".format(station.name, station.coordinate))

pySBB.ListParameter