import matplotlib.pyplot as plt
from data import load_population
from station import SBBGraph
#from usmod import USA_Air_Graph
from map import Map
fig,ax = plt.subplots()
fig.set_size_inches(16,8)
#fig2, ax2 = plt.subplots()
def main():
    sbb_graph = SBBGraph()
    CH_raster, population_map = load_population("CH")

    border = CH_raster.bounds 
    CH_map = Map(population_map,sbb_graph, border, "CH")
    image_shape = CH_map.resolution[::-1]

    sbb_graph.border = border 
    sbb_graph.image_size = image_shape
    
    #ax.imshow(CH_map.get_map_array('i'),cmap="Reds" , alpha= 0.3)

    #sbb_graph.plot_sbb_graph_from_raw(ax, border, image_shape)
    #sub_graph = sbb_graph.getGraphConnection("ZUE","GRIG")
    #sbb_graph.plot_sub_sbb_graph_connection(sub_graph[0], ax,  color='red', markersize=2,marker='.', alpha = 0.6)
    zurich = sbb_graph.get_img_pos('ZUE')
    CH_map.model_array[zurich[1]][zurich[0]].i = 0.5 * CH_map.model_array[zurich[1]][zurich[0]].population
    CH_map.model_array[zurich[1]][zurich[0]].s = 0.5* CH_map.model_array[zurich[1]][zurich[0]].population
    #plot_list = []
    number_of_iteration = 100
    for i in range(number_of_iteration):
        ax.clear()
        ax.set_title("Day: {}".format(i))
        #sbb_graph.plot_sub_sbb_graph(sbb_graph.get_ID_name(), ax,  color='green', markersize=0.9,marker='.', alpha = 0.6)
        ax.imshow(CH_map.get_map_array('p'),cmap="PRGn" , alpha= 0.8)
        CH_map.update_map()
        ax.imshow(CH_map.get_map_array('i'),cmap="bwr" , alpha= 0.6)
        #ax.imshow(CH_map.get_map_array('d'), cmap="Greens", alpha=0.3)
        #plot_list.append(CH_map.model_array[zurich[1]][zurich[0]].i)
        plt.pause(0.1)
    #ax2.plot(range(number_of_iteration), plot_list)
    #print(plot_list)
    plt.show()

if __name__ == "__main__":
    main()
