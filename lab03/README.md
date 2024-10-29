# 👮  Alert In Chicago I

## Data to use
- [Chicago Crimes - 2001 to Present](https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-Present/ijzp-q8t2/about_data)
- [Chicago Community Areas](https://data.cityofchicago.org/d/cauq-8yn6)

## Libraries to use:

- [duckdb 🦆](https://duckdb.org/docs/api/python/overview)
```
# install duckdb if needed
!pip install duckdb

import duckdb
# install and load the spatial extension
duckdb.sql('INSTALL spatial')
duckdb.sql('LOAD spatial')

# execute a query
query = """ WRITE ANY SQL QUERY HERE """
duckdb.sql(query)

# save the result to a df
df = duckdb.sql(query).df()
```
- [pandas & geopandas 🐼](https://geopandas.org/en/stable/docs/advanced_guide.html)
```python
import pandas as pd
import geopandas as gpd
```
- [plotly 📊](https://plotly.com/python/)
```python
# install plotly if needed
!pip install plotly

import plotly.express as px

# create a simple plot
fig = px.scatter_mapbox(data_frame=df, lat='latitude', lon='longitude', zoom=10)
```
- [keplergl 🌍](https://docs.kepler.gl/docs/keplergl-jupyter)
```python
from keplergl import KeplerGl

# create map
kepler_map = KeplerGl()
# add data
kepler_map.add_data(data=gdf, name=...)
# save the map
kepler_map.save_to_html(file_name='explore_map.html')
# visualize the map within the notebook
IFrame(src='./explore_map.html', width=800, height=1000)
```

## 💡 Objectives

By the end of this exercise, you will be able to:

- Load and efficiently handle large datasets using DuckDB
- Perform temporal analysis to identify trends and patterns over time
- Create interactive visualization with Plotly
- Conduct spatial analysis to map and visualize crime distribution
- Apply Kernel Density Estimation (KDE) to identify crime hotspots


## ⏰ Temporal Analysis

### Q1: What is the most dangerous year in Chicago?

- Group data by year and count the number of crimes per year
- Visualize the distribution using a bar chart
<details>
  <summary><em>ℹ️ expected answer...</em></summary>
<br>
2001 (if the empty locations are not considered) </br>
2003 (if the empty locations are considered)
</details>

<br>

### Q2: What is the general trend of crime per year?

- Plot a line chart to observe trends over time
- Analyze whether crime is increasing or decreasing
- Identify the impact of COVID-19 on crime rates

<br>

### Q3: What is the most dangerous day of the week and hour of the day?

- Extract day of the week and hour from the Date column </br>
> You can use [STRFTIME](https://strftime.org/) to extract the day of the week and hour from the date column
- Group and visualize the data to find peak crime times
- Identify if there is a strange pattern in the data
<details>
  <summary><em>ℹ️ expected answer...</em></summary>
<br>
Friday - 12pm
</details>

<br>

### Q4: How many crimes have been committed for NYE?

- Extract crimes that occurred on New Year's Eve
> You can use [STRFTIME](https://strftime.org/) to specify an exact date
- Count the number of crimes that occurred on New Year's Eve
<details>
  <summary><em>ℹ️ expected answer...</em></summary>
<br>
2455 crimes
</details>

<br> 


## 🍱  Crime Type Analysis

### Q5: What is the most common crime type that leads to an arrest?

- Filter records where an arrest was made
- Count occurrences of each Primary Type
- Visualize the top crime types leading to arrests
<details>
  <summary><em>ℹ️ expected answer...</em></summary>
<br>
Narcotics
</details>

<br>

### Q6: What is the trend of each crime type over the years?

- Group data by Primary Type and year
- Create line charts to show evolution over the years

<br>


## 🌍 Spatial Analysis

### Q7: Which is the most typical crime in 2023 per community areas?

- Group data by Community Area, crime type
- Filter data for the year 2023
- Count the number of crimes and rank them per row
```sql
-- to rank the row you can use
ROW_NUMBER() OVER (PARTITION BY ca.area_numbe ORDER BY COUNT(c.ID) DESC) as rn
-- here you consider each area_numbe as a partition
-- and you order by the count of crimes in descending order
-- the result will be a column with the rank of each crime type per community area
```
- join with the community areas geojson file
- Plot a choropleth map showing crime types per community area.

<br>

### Q8: Which is the most dangerous Community Area?

- Group data by Community Area and count crimes
- join with the community areas geojson file
- Plot a choropleth map showing crime counts per community area.
<details>
  <summary><em>ℹ️ expected answer...</em></summary>
<br>
AUSTIN
</details>

<br>

### Q9: Explore the spatial distribution of crime with keplerGL

- Extract 1-5% of the data to visualize with keplerGL
```sql
-- To extract 1% of the data you can use 
TABLESAMPLE(1 percent)
```
- Create a heatmap to visualize the spatial distribution of crime
- add a filter to animate the data over time

<br>


## 🫠  KDE Analysis

### Q10: Create a KDE for 2001, 2012, and 2023 for the crime type: `Narcotics` 

- Filter data for `Narcotics`
- Further filter data for the years 2001, 2012, and 2023 separately
- Use matplotlib and scipy to create KDE plots for each year
> 👀 look at the documentation of [kde_gaussian](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.gaussian_kde.html) from scipy, re-apply the logic 
- Compare the KDE plots to observe changes in crime hotspots over time

<br>

Congratulations! 🎉 You have successfully completed the exercise. 