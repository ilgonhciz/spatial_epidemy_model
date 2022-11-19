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
    sbb_graph = SBBGraph()
    CH_raster, population_map = load_population()
    CH_map = Map(population_map)
    
    ax.imshow(CH_map.get_map_array(),cmap="YlGn" )
    #sbb_graph.plot_sbb_graph_from_raw(ax,CH_raster.bounds, CH_map.resolution[::-1])
    sub_graph = sbb_graph.getGraphConnection("ZUE","ZERM")
    sbb_graph.plot_sub_sbb_graph(sbb_graph.get_ID_name(), ax,CH_raster.bounds, CH_map.resolution[::-1],  color='green', markersize=0.9,marker='.', alpha = 0.6)
    sbb_graph.plot_sub_sbb_graph_connection(sub_graph[0], ax,CH_raster.bounds, CH_map.resolution[::-1],  color='red', markersize=2,marker='.', alpha = 0.6)
    plt.show()

if __name__ == "__main__":
    main()