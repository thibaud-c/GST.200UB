# Spatial Accessibility Metrics for Urban Green Spaces 🌳


## 💡 Objectives

By the end of this exercise, you will be able to:

- Extract and preprocess large geospatial datasets using DuckDB for efficient querying.
- Perform spatial buffering to analyze proximity relationships between green spaces and population points.
- Assign population data to administrative districts through spatial joins.
- Aggregate and normalize population data to derive density and accessibility metrics.
- Visualize geospatial analysis results using various mapping techniques.


## 💾 Data Gathering

- 👥 Population data: [data for good](https://dataforgood.fb.com/tools/population-density-maps/) 
> other options: [WorldPop](https://www.worldpop.org/geodata/listing?id=29)
- 🌳 Green space data: [Vienna](https://www.data.gv.at/) and [Berlin](https://www.govdata.de/)
> other options: [OpenStreetMap](https://www.openstreetmap.org/) or [OSMnx](https://osmnx.readthedocs.io/en/stable/)
- 🗺️ Administrative boundaries: [Vienna](https://www.data.gv.at/) and [Berlin](https://daten.odis-berlin.de/en/dataset/bezirksgrenzen/)

<br>

Berlin green places is a wfs service, **how to access it?**
<details>
  <summary><em>🚧 Show the url...</em></summary>
  
```python
'https://fbinter.stadt-berlin.de/fb/wfs/data/senstadt/s_gruenanlagenbestand?service=WFS&version=2.0.0&request=GetFeature&outputFormat=application/json&typeNames=fis:s_gruenanlagenbestand'
```
</details>
<br>

ℹ️ The pre-clipped population data is available in the data folder. You can try to download the data from the above source and clip it to the study area using [duckdb](https://duckdb.org/docs/extensions/spatial/overview.html).

To use duckdb in jupyter notebook, you can use the following code
```python
# duckdb should be already installed, if not you can use the following command
## !pip install duckdb

# install and load the spatial extension
duckdb.sql('INSTALL spatial')
duckdb.sql('LOAD spatial')

query = """ WRITE ANY SQL QUERY HERE """
result = duckdb.sql(query)

# save the result to a df
df = result.df()
```

<br>
<details>
  <summary><em>🚧 Steps to transform your raw data...</em></summary>

1. load the population data (`CREATE TABLE` & `read_csv`)
2. load the administrative boundaries (`CREATE TABLE` & `ST_Read(.. *.shp)`)
3. check the spatial reference system of the data (SELECT ST_ASText(geom) FROM ... LIMIT 1)
3. reproject the data if needed (`ST_Transform ( ST_FlipCoordinates (...), 'EPSG:31256','EPSG:4326') AS ...`) 
4. clip the population data to the study area ( `ST_Intersects(..., ...)`)
5. copy to output of the query to a parquet file (`COPY (...) TO 'output.parquet' WITH (FORMAT 'parquet');`)

</details>
<br>


## ⚙️ Data Processing

1. Load and Plot the Data: Understand the spatial distribution of green spaces and population points.
<details>
  <summary><em>🚧 function to use...</em></summary>

Here you can use matplotlib or kepler to explore your data
```python
from keplergl import KeplerGl
from IPython.display import IFrame
# create map
kepler_map = KeplerGl()
# add data 
kepler_map.add_data(data=gdf, name=...)
# save the map
kepler_map.save_to_html(file_name='explore_map.html')
# visualize the map within the notebook
IFrame(src='./explore_map.html', width=800, height=1000)
```
</details>
<br>

2. Create Buffers Around Green Spaces: Generate buffer zones of 500m around each green space to analyze proximity.
<details>
  <summary><em>🚧 function to use...</em></summary>

```python
gdf.buffer(...)
```
</details>
<br>

3. Assign Population Points to Districts: Assign each population point to its respective administrative district using spatial joins.
<details>
  <summary><em>🚧 function to use...</em></summary>

```python
gpd.sjoin(...)
```
</details>
<br>

4. Determine Proximity to Green Spaces: Identify population points within the buffered green space zones. (Flag each population point as either inside or outside the green space buffer)
<details>
  <summary><em>🚧 function to use...</em></summary>

```python
gpd.sjoin(...)
gdf['...'] = gdf['...'].notna() # to flag the data in a new column
```
</details>
<br>

5. Aggregate Population Data by District: Aggregate population statistics at the district level.
<details>
  <summary><em>🚧 function to use...</em></summary>

```python
gdf.groupby(...) # + agg function
pd.merge(...)
```
</details>
<br>

6. Merge Aggregated Data with Districts
<details>
  <summary><em>🚧 function to use...</em></summary>

```python
gdf.merge(...)
gdf['...'].fillna(...) # to fill data if the missing values
```
</details>
<br>


7. Normalize Population Data: Derive density and accessibility metrics
8. Visualize your data with a choropleth map and a stacked bar chart


## 🥊 Challenges
- Estimate the accessibility of green spaces for each district by calculating the average distance for each population to the nearest green space.
- Implement the Two-step floating catchment area (2SFCA) method for assessing the accessibility of green spaces.


Congratulations! 🎉 You have successfully completed the exercise. 