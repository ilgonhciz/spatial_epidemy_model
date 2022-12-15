import matplotlib.pyplot as plt
from data import load_population
from file import parameters_config, File
from station import SBBGraph
from usmod import USA_Air_Graph
from map import Map
fig,ax = plt.subplots()
fig2,ax2 = plt.subplots()
ax2b = ax2.twinx()
size_label = [14, 18, 16, 16] 
ax2.grid(visible=True, alpha=0.5)
ax2.xaxis.set_tick_params(labelsize=size_label[3])
ax2.yaxis.set_tick_params(labelsize=size_label[3])
ax2b.yaxis.set_tick_params(labelsize=size_label[3])


#ax2.yaxis.set_major_formatter(lambda x, pos: "%.f"%((x)/1e6 ))

plot_color = {'p':'limegreen', 's':'green', 'i':'red', 'r':'blue', 'v':'deepskyblue', 'd':'black'}

fig.set_size_inches(16,7)
fig2.set_size_inches(16,3)

file = File()
file.create_result_folder()
file.append_fig(fig, name = 'map')
file.append_fig(fig2, name = 'total')
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
    for i in range(number_of_iteration):
        ax.clear()
        ax2.clear()
        ax2.set_xlabel("Days", fontsize=size_label[2])
        ax2.set_ylabel("Number in Mio", fontsize=size_label[2])
        ax2b.set_ylabel("Deaths", fontsize=size_label[2])
        lines = []
        for key, item in map.full_statistic['total'].items():
            if key in ['p']:
                continue
            if key == "d":
                lines += ax2b.plot(range(len(item)), item, label=key, color= plot_color[key], linewidth=2)
            else:
                lines += ax2.plot(range(len(item)), item, label=key, color= plot_color[key])
        
        ax2.legend(lines, [line.get_label() for line in lines], fontsize=size_label[3],bbox_to_anchor=(0, 0.9), loc="upper left")
        ax.set_title("Day: {}".format(i))
        if country == "USA":
            alpha = 0.02
        else:
            alpha = 0.07
        graph.plot_sub_sbb_graph(graph.get_ID_name(),ax, color='green', markersize=0.9,marker='.', alpha = alpha)
        ax.imshow(map.get_map_array('p_raw'),cmap="PRGn" , alpha= 0.9)
        map.update_map()
        #ax.imshow(map.get_map_array('i'),cmap="bwr" , alpha= 0.6)
        ax.imshow(map.get_map_array('i'), cmap="bwr", alpha=0.6)
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
