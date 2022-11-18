""" import geopandas
switzerland_administrative_boundaries = geopandas.read_file('Data/switzerland_data/che_ppp_2020_UNadj.shp')

vietnam_worldpop_raster_tot = vietnam_worldpop_raster.read(1)
vietnam_worldpop_raster_tot[vietnam_worldpop_raster_tot<0] = None
plt.rcParams['figure.figsize'] = 14, 14
plt.imshow(np.log10(vietnam_worldpop_raster_tot+1),)
bar = plt.colorbar(fraction=0.5)

print("hellopai") """   

import numpy as np
import matplotlib.pyplot as plt
from data import load_sbb_data, load_population
from station import SBBGraph
from map import Map
fig,ax = plt.subplots()
fig.set_size_inches(20,10)
def main():
    sbb_graph = SBBGraph(load_sbb_data())
    CH_raster, _ = load_population()
    CH_map = Map()
    
    ax.imshow(CH_map.get_map_array(),cmap="YlGn" )
    sbb_graph.plot_sbb_graph(ax,CH_raster.bounds, CH_map.resolution[::-1])
    plt.show()

if __name__ == "__main__":
    print(x)
    main()