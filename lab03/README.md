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


## 🪹  Null values

### Q0: How many null values are in the dataset?

- Count the number of null values for the column "location"


#### <u>ℹ️ Tips</u>:
<details>
    <summary>💡 Need Help?</summary>
    <br>

> You will need the following SQL keyword:
> - `COUNT(col)` to count the number of null values
> - `col IS NULL` to filter null values in a column

</details>
<details>
  <summary>👀 Wanna verify the answer you found?</summary>
    <br>

>  89945 ≈ 1.1% of the data

</details>

<br>

## ⏰ Temporal Analysis

### Q1: What is the most dangerous year in Chicago?

- Group data by year and count the number of crimes per year
- Visualize the distribution using a bar chart

#### __ℹ️ Tips__:
<details>
    <summary>💡 Need Help?</summary>
    <br>

> You will need the following SQL keyword:
> - `COUNT(col)` to count the number of crimes
> - `ORDER BY col DESC` to order the data in descending order
> - `GROUP BY col` to group the data by year

</details>
<details>
  <summary>👀 Wanna verify the answer you found?</summary>
    <br>

> 2001 (if the empty locations are not considered) </br>
> 2003 (if the empty locations are considered)

</details>

<br>
_ _ _ _ _

### Q2: What is the general trend of crime per year?

- Plot a line chart to observe trends over time
- Analyze whether crime is increasing or decreasing
- Identify the impact of COVID-19 on crime rates

#### <u>ℹ️ Tips</u>:
<details>
    <summary>💡 Need Help?</summary>
    <br>

> You can depict the data with a bar chart to visualize the peak crime years
>
> `px.bar(df, x='df_col_x', y='df_col_y'` to create a bar chart with Plotly

</details>

<br>

_ _ _ _ _

### Q3: What is the most dangerous day of the week and hour of the day?

- Extract day of the week and hour from the Date column </br>
> You can use [STRFTIME](https://strftime.org/) to extract the day of the week and hour from the date column
- Group and visualize the data to find peak crime times
- Identify if there is a strange pattern in the data

#### <u>ℹ️ Tips</u>:
<details>
    <summary>💡 Need Help?</summary>
    <br>

> You will need the following SQL keyword:
> - `STRFTIME('%H', col)` to extract the hour from the date column
> - `STRFTIME('%A', col)` to extract the week day from the date column
> - `GROUP BY col` to group the data by hour
> - `ORDER BY col ASC` to order the data in ascending order
> - To reorganize your days in a correct order you can reindex your dataframe with the following code:
> ```python
> cats= ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
> df= df.set_index('day').reindex(cats).reset_index()
> ```

</details>
<details>
  <summary>👀 Wanna verify the answer you found?</summary>
<br>

> Friday - 12pm

</details>

<br>

_ _ _ _ _

### Q4: How many crimes have been committed for NYE?

- Extract crimes that occurred on New Year's Eve
> You can use [STRFTIME](https://strftime.org/) to specify an exact date
- Count the number of crimes that occurred on New Year's Eve

#### <u>ℹ️ Tips</u>:
<details>
    <summary>💡 Need Help?</summary>
    <br>

> You will need the following SQL keyword:
> - `WHERE strftime('%Y-%m-%d %H:%M:%S', Date) == strftime('%Y-01-01 00:00:00', Date)` to filter the data for New Year's Eve
> 
> this filter your data at a specific date and time with a variable year

</details>
<details>
  <summary>👀 Wanna verify the answer you found?</summary>
    <br>

> 2455 crimes

</details>

<br> 


## 🍱  Crime Type Analysis

### Q5: What is the most common crime type that leads to an arrest?

- Filter records where an arrest was made
- Count occurrences of each Primary Type
- Visualize the top crime types leading to arrests

#### <u>ℹ️ Tips</u>:
<details>
    <summary>💡 Need Help?</summary>
    <br>

> You will need the following SQL keyword:
> - `col IS TRUE` to filter records where an arrest was made
> - `GROUP BY col` to group the data by crime type
> - `ORDER BY col DESC` to order the data in descending order

</details>
<details>
  <summary><em>👀 Wanna verify the answer you found?</em></summary>
<br>
Narcotics > Battery > Theft
</details>

<br>
_ _ _ _ _

### Q6: What is the trend of each crime type over the years?

- Group data by Primary Type and year
- Create line charts to show evolution over the years

#### <u>ℹ️ Tips</u>:
<details>
    <summary>💡 Need Help?</summary>
    <br>

> To create a line graph with Plotly you can use: 
> ``` python
> px.line(df, x='df_col_x', y='df_col_y', color="category")
> ```

</details>

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
- Join with the community areas geojson file
- Plot a choropleth map showing crime types per community area.

#### <u>ℹ️ Tips</u>:
<details>
    <summary>💡 Need Help?</summary>
    <br>

> You will need the following SQL keyword:
> - `FROM t1 JOIN t2 ON t1.common_col = t2.common_col` to join (merge) two tables
> - `PARTITION BY col` to group the data by community area
> - `ROW_NUMBER() OVER (PARTITION BY col ORDER BY COUNT(col) DESC) as rn` to rank the data
>
> You will need the geometry of the community areas to plot the choropleth map
> - `ST_AsHexWKB(ca.geometry)` to extract the geometry of the community areas that you will be able to load in a geopandas dataframe
> ```python 
> # you can load the data directly in a geopandas dataframe with the following code
> gdf = gpd.GeoDataFrame(df, geometry=gpd.GeoSeries.from_wkb(df['geometry']), crs="EPSG:4326")
> ```
>
> To create a choropleth map with Plotly you can use: 
> ``` python
> px.choropleth_map(gdf, geojson=gdf['geometry'], locations=gdf.index, color=gdf['category'])
> ```

</details>

<br>
_ _ _ _ _

### Q8: Which is the most dangerous Community Area?

- Group data by Community Area and count crimes
- Join with the community areas geojson file
- Plot a choropleth map showing crime counts per community area.


#### <u>ℹ️ Tips</u>:
<details>
  <summary>👀 Wanna verify the answer you found?</summary>
<br>

> AUSTIN

</details>

<br>
_ _ _ _ _

### Q9: Explore the spatial distribution of crime with keplerGL

- Extract 1-5% of the data to visualize with keplerGL
```sql
-- To extract 1% of the data you can use 
TABLESAMPLE(1 percent)
```
- Create a heatmap to visualize the spatial distribution of crime
- Add a temporal filter within keplerGL to animate the data over time

<br>


## 🫠  KDE Analysis

### Q10: Create a KDE for 2001, 2012, and 2023 for the crime type: `Narcotics` 

- Filter data for `Narcotics`
- Further filter data for the years 2001, 2012, and 2023 separately
- Use matplotlib and scipy to create KDE plots for each year
> 👀 look at the documentation of [gaussian_kde](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.gaussian_kde.html) from scipy, re-apply the logic 
- Compare the KDE plots to observe changes in crime hotspots over time

#### <u>ℹ️ Tips</u>:
<details>
    <summary>💡 Need Help?</summary>
    <br>

> Step by Step guide to create the KDE plot via python:
> ```python
> from scipy.stats import gaussian_kde
>
> ## 1. Calculate the KDE for the data
> # gaussian_kde takes an array of shape (N, D) where N is the number of points and D is the number of dimensions 
> # i.e., 2 rows (latitude, longitude) and N columns (number of points)
> kde = gaussian_kde(df[['latitude', 'longitude']].T)
>
> ## 2. create a grid of points to evaluate the KDE
> # linspace creates an array of evenly spaced numbers over a specified interval here 100 points
> x = np.linspace(df['latitude'].min(), df['latitude'].max(), 100)
> y = np.linspace(df['longitude'].min(), df['longitude'].max(), 100)
> # meshgrid creates a grid of points from the x and y arrays
> X, Y = np.meshgrid(x, y)
> # evaluate the KDE at each point in the grid -> gives a Z score to the data
> Z = kde(np.vstack([X.ravel(), Y.ravel()]))
> Z = Z.reshape(X.shape)
> 
> ## 3. plot the KDE
> plt.contourf(X, Y, Z, cmap='viridis')
> plt.show()
> ```

</details>

<br>

## 🥊 Challenges
- Create a KDE for other crime types

Congratulations! 🎉 You have successfully completed the exercise. 