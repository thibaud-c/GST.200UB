# 🛣️ Network Analysis with Python: Centrality, Clustering and Isochrones

## Libraries to use:

- [osmnx](https://osmnx.readthedocs.io/en/stable/user-reference.html#osmnx.geocoder.geocode)
> Used to retrieve, construct, analyze, and visualize street networks from OpenStreetMap

- [networkx](https://networkx.org/documentation/stable/index.html)
> Used to create, manipulate, and study the structure, dynamics, and functions of complex networks
```python
# if not already install, you can install it with
!pip install networkx[default]
```

- [pyproj](https://pyproj4.github.io/pyproj/stable/)
> Used to perform cartographic transformations and geodetic computations

- [python-louvain](https://python-louvain.readthedocs.io/en/latest/)
> Used to perform community detection on networks 
```python
# if not already install, you can install it with
!pip install python-louvain
import community as community_louvain
```

<br>

## 💡 Objectives

By the end of this exercise, you will:
- Learn and apply **critical concepts** in network analysis.
- Identify the **most important nodes** in a street network using centrality measures.
- **Cluster** the street network to identify district divisions.
- Analyze the **15-minute city** concept by calculating walking isochrones from a specific address. Evaluate whether all essential amenities are accessible within a 15-minute walk.

<br>

## 🎯 Goal of the exercise

Create a notebook that can calculate the **centrality measures** of a street network, **cluster** the street network to identify district divisions, and **calculate isochrones** from a specific address to evaluate the 15-minute city concept.

<br>

## 🛝 Step-by-step guide

### 1. **Collect the street network data** of a city using OSMnx

> ℹ️ This first is similar to the previous exercise, so you can copy the code from the previous exercise and adapt it to this one. 

1. define a city name (e.g., _Graz, Austria_)
2. retrieve the street network data using `osmnx.graph_from_place()` (see documentation [here](https://osmnx.readthedocs.io/en/stable/osmnx.html#osmnx.graph.graph_from_place)) focus first on `network_type = 'drive'` to limit the amount of data retrieved

> [!TIP]
> Collect the network in a separate jupyter cell to avoid re-collecting the network each time you run the cell

3. reproject the graph to a projected coordinate system (e.g., UTM) using `osmnx.project_graph()` (see documentation [here](https://osmnx.readthedocs.io/en/stable/osmnx.html#osmnx.projection.project_graph))
4. plot the street network using `osmnx.plot_graph()` (see documentation [here](https://osmnx.readthedocs.io/en/stable/osmnx.html#osmnx.plot.plot_graph)) to see if the network is correctly loaded,

> [!TIP]
> You can make the node disappear by setting the `node_size` parameter to 0

### 2. 📌 Centrality Analysis

> ℹ️ Centrality measures are used to identify the most important nodes in a network. They can help you understand the structure of the network and identify key nodes that are important for the network's connectivity.

1. Compute the shortest-path betweenness centrality using `networkx.degree_centrality()` (see documentation [here](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.centrality.degree_centrality.html))

> [!IMPORTANT] 
> You should add a weight to the edges of the graph to calculate the centrality based on the length of the edges. You can use the `length` attribute of the edges as the weight
> The operation is quite costly and should run for around 1min for all Graz.

2. The result of the centrality analysis is a dictionary where the key is the node and the value is the centrality measure. You have to add the centrality measure as a node attribute to the graph using `networkx.set_node_attributes()` (see documentation [here](https://networkx.org/documentation/stable/reference/generated/networkx.classes.function.set_node_attributes.html))

> [!TIP]
> Don't forget to add a name to the attribute you are adding to the nodes 

3. Plot the street network using `osmnx.plot_graph()` and color the nodes based on the centrality measure using the `node_color` parameter

> [!IMPORTANT] 
> To apply different colors to your nodes `node_color` can be a list of values. You can use the `values()` method of the centrality dictionary to get a list of the centrality values. Also because your updated the node values with the centrality measure, you can use `networkx.get_node_attributes()` (see documentation [here](https://networkx.org/documentation/stable/reference/generated/networkx.classes.function.get_node_attributes.html) to get specific node attributes. Once the attributes are collected you should also convert them to a list, with the `values()` method.

4. Create an interactive visualization of the street network using `folium` or `KeplerGL`
Both of the libraries works with dataframes, so you need to convert the graph to a dataframe using `osmnx.graph_to_gdfs()` (see documentation [here](https://osmnx.readthedocs.io/en/stable/osmnx.html#osmnx.save_load.graph_to_gdfs))

---
##### ❓ Are the results as expected? What do you observe?
---


### 3. 🏘️ Community Detection within your network

> ℹ️ Community detection is a method to identify groups of nodes that are more connected to each other than to the rest of the network.
>
> We will use the Louvain algorithm to detect communities in the street network.
> You are lucky because there is a library that exactly do that, `python-louvain`.

1. By default osmnx graph is directed. Unfortunately, the algorithm works best with undirected graphs, so you need to convert the graph to an undirected graph using `networkx.Graph()` (see documentation [here](https://networkx.org/documentation/stable/reference/classes/graph.html))

> [!TIP]
> Don't override your graph, create a new graph to keep the original graph

2. Compute the communities in the street network using the Louvain algorithm `community_louvain.best_partition()` (see documentation [here](https://python-louvain.readthedocs.io/en/latest/api.html#python-louvain))

3. Add the community as a node attribute to the graph using `networkx.set_node_attributes()`

4. Plot the street network using `osmnx.plot_graph()` and color the nodes based on the community using the `node_color` parameter

5. Create an interactive visualization of the street network using `folium` or `KeplerGL`

---
##### ❓ Are the results fitting the municipality districts? What do you observe?
---

### 4. 🚶‍♂️ Isochrones Analysis

> ℹ️ Isochrones are lines that connect points that can be reached within a certain amount of time. They are used to visualize accessibility and can help you understand how long it takes to reach different parts of a city. The isochrones are critical for the concept of the 15-minute city.
>
> The concept of the 15-min city is that all essential amenities should be accessible within a 15-minute walk. To evaluate this concept, you need to calculate the isochrones from a specific address.

1. Download the street network data of a city using OSMnx. You can use the same city as before or a different one, but make sure to use the type of network that is suitable for walking (e.g., `network_type = 'walk'`)

2. Define a source address (e.g., _"Heinrichstrasse 36, 8010 Graz"_) and get the corresponding node in the graph.

> ℹ️ We already did the exercise last week, so you can copy the code from the previous exercise and adapt it to this one. 

3. Add the travel time to the graph as an edge attribute for walking. You can use the formula `time = distance / speed` to calculate the travel time for each edge. You can loop on the edges of the graph using `graph.edges(data=True)`. In the loop your can calculate the travel time for each edge and add it to the graph as an edge attribute.

#### <u>ℹ️ Tips</u>:
<details>
    <summary>💡 If you face some issues to find the solution?</summary>
    <br>

Below is a helper function to add a `travel_time` attribute to your graph.
```python
def add_travel_time(G, speed, attribute_name='travel_time'):
    # Compute travel time for all edges and set as attribute
    # use an inline for loop to calculate the travel time for each edge
    for _, _, data in G.edges(data=True):
        data[attribute_name] = data['length'] / speed
```

</details>
<br>
4. Create an isochrone 15-min from the source node. You can use the `networkx.ego_graph()` (see documentation [here](https://networkx.org/documentation/stable/reference/generated/networkx.generators.ego.ego_graph.html)) function. The function creates a subgraph of the graph centered at the source node and includes all nodes that are reachable within a certain distance from the source node. 

> [!TIP]
> You can use the `radius` parameter to specify the time distance from the source node. Don't forget to also specify the `distance` parameter to use the `travel_time` attribute as the edge weight 

5. Create a polygon from the subgraph. One idea can be to collect all points of the subgraph and to create a polygon. To create a polygon you can apply `unary_union.convex_hull` directly to a geoDataFrame.

6. Plot the street network using `osmnx.plot_graph()` and overlay the isochrone polygon on the map. To plot a polygon you can use a gpd.GeoSeries wrapper around the polygon and use the `plot()` method. You can also use the matplotlib `fill()` function to fill the polygon with a color (🚧 fill takes only a list of coordinates in input and not a Polygon geometry). 


## 🥊 Challenges
**Centrality**

- Delete the 10 most important nodes (check at the library `heapq` to identify the highest values in a dictionary) of your graph (look at `remove_nodes_from()`). See how these deletions affect the network structure by comparing a shortest path calculation between the normal and reduced graph.

**Community Detection**
    
- Compare the results of the Louvain algorithm with the actual district divisions of the city. Are the results similar? What are the differences?

**Isochrones**

- Calculate the isochrones for different time intervals (e.g., 5, 10, 20 minutes) and compare the results. What do you observe?
- Identify the amenities that are accessible within a 15-minute walk from the source address. Are all essential amenities accessible within a 15-minute walk?

<br>

Congratulations! 🎉 You have successfully completed the exercise. 
