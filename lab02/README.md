# Spatial Accessibility Metrics for Urban Green Spaces


## Objectives

By the end of this exercise, you will be able to:

- Extract and preprocess large geospatial datasets using DuckDB for efficient querying.
- Perform spatial buffering to analyze proximity relationships between green spaces and population points.
- Assign population data to administrative districts through spatial joins.
- Aggregate and normalize population data to derive density and accessibility metrics.
- Visualize geospatial analysis results using various mapping techniques.


## Data Gathering

- 👥 Population data: [data for good](https://dataforgood.fb.com/tools/population-density-maps/) 
> other options: [WorldPop](https://www.worldpop.org/geodata/listing?id=29)
- 🌳 Green space data: [Vienna](data.gov.at) and [Berlin](govdata.de)
> other options: [OpenStreetMap](https://www.openstreetmap.org/) or [OSMnx](https://osmnx.readthedocs.io/en/stable/)
- 🗺️ Administrative boundaries: [Vienna](data.gov.at) and [Berlin](https://daten.odis-berlin.de/en/dataset/bezirksgrenzen/)

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

query = """ WRITE ASQL QUERY HERE """
result = duckdb.sql(query)

# save the result to a df
df = result.df()
```

<br>
<details>
  <summary><em>🚧 Steps to transform your raw data...</em></summary>

1. load the population data
2. load the administrative boundaries
3. check the spatial reference system of the data
4. clip the population data to the study area (use ST_Intersects)
5. copy to output of the query to a parquet file

</details>
<br>


## Data Processing

1. Load and Plot the Data: Understand the spatial distribution of green spaces and population points.
2. Create Buffers Around Green Spaces: Generate buffer zones of 500m around each green space to analyze proximity.
<details>
  <summary><em>🚧 function to use...</em></summary>

```python
gdf.buffer(...)
```
</details>
<br>

2. Assign Population Points to Districts: Assign each population point to its respective administrative district using spatial joins.
<details>
  <summary><em>🚧 function to use...</em></summary>

```python
gpd.sjoin...()
```
</details>
<br>

3. Determine Proximity to Green Spaces: Identify population points within the buffered green space zones. (Flag each population point as either inside or outside the green space buffer)
<details>
  <summary><em>🚧 function to use...</em></summary>

```python
gpd.sjoin...()
gdf['...'] = gdf['...'].notna() # to flag the data in a new column
```
</details>
<br>

4. Aggregate Population Data by District: Aggregate population statistics at the district level.
<details>
  <summary><em>🚧 function to use...</em></summary>

```python
gdf.groupby(...) # + agg function
pd.merge(...)
```
</details>
<br>

5. Merge Aggregated Data with Districts
<details>
  <summary><em>🚧 function to use...</em></summary>

```python
gdf.merge(...)
gdf['...'].fillna(...) # to fill data if the missing values
```
</details>
<br>


6. Normalize Population Data: Derive density and accessibility metrics
7. Visualize your data with a choropleth map and a stacked bar chart
