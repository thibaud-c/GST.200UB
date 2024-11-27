# 🛣️ Network Analysis with Python: Shortest Path Exploration

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


<br>


## 💡 Objectives

By the end of this exercise, you will:

- **Acquire** and **process** real-world street network data using OSMnx
- **Geocode** addresses to obtain precise coordinates
- **Calculate** the shortest path between two points using Dijkstra's algorithm (and other shortest path algorithms)
- **Visualize** the computed route, and network graph

<br>

## 🎯 Goal of the exercise

Create a notebook that can calculate the shortest path between two points in a city. The notebook should be able to:
- Take as input two addresses
- Calculate the shortest path between the two addresses
- Visualize the route on a map

<br>

## 🛝 Step-by-step guide

### 1. **Collect street network data** of a city using OSMnx
1. define a city name (e.g., _Graz, Austria_)
2. retrieve the street network data using `osmnx.graph_from_place()` (see documentation [here](https://osmnx.readthedocs.io/en/stable/osmnx.html#osmnx.graph.graph_from_place))
> 💡 Pro tip 
>
> You can use the `network_type` parameter to specify the type of street network to retrieve. The default is `drive`, but you can also use `walk`, `bike`, `all`, etc.
>
> You can use the `simplify` parameter to simplify the street network graph. This can help reduce the size of the graph and speed up computations

3. reproject the graph to a projected coordinate system (e.g., UTM) using `osmnx.project_graph()` (see documentation [here](https://osmnx.readthedocs.io/en/stable/osmnx.html#osmnx.projection.project_graph))
4. plot the street network using `osmnx.plot_graph()` (see documentation [here](https://osmnx.readthedocs.io/en/stable/osmnx.html#osmnx.plot.plot_graph))
> 💡 Pro tip 
>
> You can make the node disappear by setting the `node_size` parameter to 0

### 2. **Geocode** a source address and a target address

1. define an address source (origin) (e.g., "_Europapl. 7, 8020 Graz, Austria_")
2. define an address target (destination) (e.g., "_Heinrichstrasse 36, 8010 Graz, Austria_")
3. geocode both addresses using `osmnx.geocode()` (see documentation [here](https://osmnx.readthedocs.io/en/stable/osmnx.html#osmnx.geocoder.geocode_to_gdf))
4. because we have reprojected our graph, we need to reproject the geocoded addresses to the same coordinate system using `pyproj.Transformer` (see documentation [here](https://pyproj4.github.io/pyproj/stable/api/transformer.html))
> 💡 Pro tip 
>
> You can create a transformer object using the `from_crs` and `to_crs` parameters. You can then use the `transform()` method to transform coordinates
> example:
> ```python
> from pyproj import Transformer # only if not already imported
> transformer = Transformer.from_crs("epsg:4326", "epsg:TARGET_CRS")
> x, y = transformer.transform(X_COORD, Y_COORD)
> ```
#### <u>ℹ️ Tips</u>:
<details>
    <summary>💡 Need More Help?</summary>
    <br>

Below is a helper function to transform coordinates from one CRS to another.
```python
from pyproj import Transformer # only if not already imported
def to_crs(x, y, target_crs, source_crs):
    transformer = Transformer.from_crs(source_crs, target_crs)
    return transformer.transform(x, y)
```

</details>

### 3. **Select** the related nodes in the graph

1. find the nearest node in the graph to the source and target addresses using `osmnx.distance.nearest_nodes()` (see documentation [here](https://osmnx.readthedocs.io/en/stable/osmnx.html#osmnx.distance.nearest_nodes))
> 💡 Pro tip 
>
> You can use the `return_dist` parameter to return the distance between the source/target address and the nearest node
> example:
> ```python
> node_source, dist_source = ox.distance.nearest_nodes(graph, X_SOURCE, Y_SOURCE, return_dist=True)
> ```

### 4. **Calculate** the shortest path between the two points using Dijkstra's algorithm

1. calculate the shortest path between the source and target nodes using `networkx.dijkstra_path()` (see documentation [here](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.shortest_paths.weighted.dijkstra_path.html))
> 💡 Pro tip 
>
> You can use the `weight` parameter to specify the edge attribute to use as the edge weight, in this case, the `length` of the edge
2. What is the distance of the shortest path?
> 💡 Pro tip
>
> You can also you the function `dijkstra_path_length` (see documentation [here](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.shortest_paths.weighted.dijkstra_path_length.html)) to get the length of the shortest path
> ℹ️ don't forget to specify the `weight` parameter if you want the length of the path to be calculated based on the edge attribute `length`

**❓What happened to the shortest path if `weight` is not defined?**


### 5. **Visualize** the route on a map

1. plot the street network using `osmnx.plot_graph_route()` (see documentation [here](https://osmnx.readthedocs.io/en/stable/osmnx.html#osmnx.plot.plot_graph_route))


## 🥊 Challenges
a. generate and visualize random routes within Graz: 
    - select two random nodes from your graph
    - calculate the shortest path between the random points
    - visualize the route on a map

b. calculate the shortest path using other algorithms (e.g., A* algorithm, Bellman-Ford algorithm, etc.)
    - look at the documentation of [networkx](https://networkx.org/documentation/stable/reference/algorithms/shortest_paths.html#) to find the right function to use

c. don't use data from osmnx to create the graph, but use the data from [ouverture maps foundation](https://docs.overturemaps.org/) <br>
> Ouverture Maps data is stored on a s3 bucket (aws) as a geoparquet file, so you can use duckdb 🦆 to get the data directly! <br>
> 🚧 Caution the hosted parquet files are very BIG, you need to filter it _before_ getting the data. <br>
> 👀 look at this great [example](https://docs.overturemaps.org/getting-data/duckdb/), you don't have to copy the data and write a file, you can use it directly in memory. <br>
> Here are the steps you need to follow:
> - look at the [division](https://docs.overturemaps.org/guides/divisions/) documentation, try to get the geometry of Graz from `division_area`
> - look at the [transportation](https://docs.overturemaps.org/guides/transportation/) documentation, try to get the `segment` and `connector` of Graz
> - download and load the data in geodataframes, you have have 2, one for connectors = nodes and one for segments = edges
> - initialize a graph `nx.MultiGraph(...)` - it should be a multigraph because osmnx uses multigraphs
> - loop over the `segment` dataframe to create the edges `G.add_edge(u,v, length=1)`, remember `u` is the starting node and `v` the ending node 
> - for each segment you need to: 
>     - find the nodes of the segment (it is in the `connectors` parameter or your segments)
>     - for each node collect its geometry from the `connector` geodataframe
>     - create for each subdivision of your segment the nodes with `G.add_node(id, x, y)`, and the edges (see above)
> 
> **❓How your network looks like compare to the one from osmnx?**

<br>

Congratulations! 🎉 You have successfully completed the exercise. 
