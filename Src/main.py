import matplotlib.pyplot as plt
from data import load_population
from file import parameters_config, File
from station import SBBGraph
from usmod import USA_Air_Graph
from map import Map
fig,ax = plt.subplots()
fig.set_size_inches(16,8)

file = File()
file.create_result_folder()
file.append_fig(fig)
#fig2, ax2 = plt.subplots()

def main():
    #graph = SBBGraph()
    country = parameters_config['main']['country']
    number_of_iteration = parameters_config['main']['iteration']
    if country == "USA":
        graph = USA_Air_Graph()
    elif country == "CH":
        graph = SBBGraph()
    CH_raster, population_map = load_population(country)

    map = Map(population_map, graph, CH_raster.bounds, country)
    image_shape = map.resolution[::-1]

    graph.border = map.border 
    graph.image_size = image_shape
    
    
    #sbb_graph.plot_sbb_graph_from_raw(ax, border, image_shape)
    #sub_graph = sbb_graph.getGraphConnection("ZUE","GRIG")
    #sbb_graph.plot_sub_sbb_graph_connection(sub_graph[0], ax,  color='red', markersize=2,marker='.', alpha = 0.6)
    city = graph.get_img_pos(parameters_config['main']['outbreak'])
    map.model_array[city[1]][city[0]].i = parameters_config['main']['outbreak_percentage'] * map.model_array[city[1]][city[0]].population
    map.model_array[city[1]][city[0]].s = (1 - parameters_config['main']['outbreak_percentage']) * map.model_array[city[1]][city[0]].population
    #plot_list = []
    for i in range(number_of_iteration):
        ax.clear()
        ax.set_title("Day: {}".format(i))
        #graph.plot_sub_usa_air_graph(graph.get_ID_name(),ax, color='green', markersize=0.9,marker='.', alpha = 0.2)
        ax.imshow(map.get_map_array('p'),cmap="PRGn" , alpha= 0.8)
        map.update_map()
        #ax.imshow(map.get_map_array('i'),cmap="bwr" , alpha= 0.6)
        ax.imshow(map.get_map_array('d'), cmap="bwr", alpha=0.3)
        #plot_list.append(CH_map.model_array[zurich[1]][zurich[0]].i)
        if parameters_config['main']['savefig']:
            file.save_results(i, country = country)
        else:
            plt.pause(0.1)
    #ax2.plot(range(number_of_iteration), plot_list)
    #print(plot_list)
    if not parameters_config['main']['savefig']:
        plt.show()

if __name__ == "__main__":
    main()
