# 👮  Alert In Chicago II

## Data to use
- [Chicago Crimes - 2001 to Present](https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-Present/ijzp-q8t2)
- [Chicago Community Areas](https://data.cityofchicago.org/d/cauq-8yn6)


##### 💡 Pro tip 
> You can transform your crime data in parquet to reduce its size
```python
# import duckdb

query = """
COPY (
    SELECT * 
    FROM 'data/Crimes.csv'
    WHERE Location IS NOT NULL
) TO 'crimes.parquet' (FORMAT PARQUET);
"""

duckdb.sql(query)
```

<br> 

## Libraries to use:

- [duckdb 🦆](https://duckdb.org/docs/api/python/overview)

  - see [h3 library for duckDB](https://community-extensions.duckdb.org/extensions/h3.html)

```python
# add h3 extension
# import duckdb
duckdb.sql('INSTALL h3')
duckdb.sql('LOAD h3')
```

- [PySAL](https://pysal.org/packages/)

```python
!pip install pysal
```
```python
# we will use the libraries lib and explore 
import pysal
```

<br>

## 💡 Objectives

By the end of this exercise, you will be able to:

- Understand and apply spatial statistical methods to detect patterns
- Utilize the H3 hexagonal grid system for spatial aggregation
- Create informative maps to visualize spatial data and analysis results
- Draw meaningful conclusions from statistical outputs and visualizations

<br>

## 📚 Import Crimes and Community Areas Data 

_( if not already done in the previous exercise )_

```sql
-- SQL query to create tables

-- create com_areas
CREATE OR REPLACE TABLE com_areas AS
    SELECT *
    FROM ST_Read('../lab03/data/Com_Areas.geojson');

-- update geometry column name
ALTER TABLE com_areas 
RENAME COLUMN geom to geometry;

-- create crimes from parquet
CREATE OR REPLACE TABLE crimes AS
    SELECT *, ST_Point2D(Longitude, Latitude) as geometry 
    FROM Read_Parquet('../lab03/data/Crimes.parquet')
    WHERE Location IS NOT NULL;
```

> ℹ️ Seen at the previous exercise..
> - ST_Read: Reads spatial data into DuckDB from a GeoJSON file
> - ST_Point2D: Creates a point geometry from longitude and latitude
> - read_parquet: Reads Parquet files into DuckDB

<br>

## 📍 Calculate Mean Center of Crimes per Year

- Calculate the mean center of crimes per year to understand the evolution of crimes distribution over time
- Visualize the evolution using a [scatter map](https://plotly.com/python/tile-map-layers/) from Plotly 


#### <u>ℹ️ Tips</u>:
<details>
    <summary>💡 Need Help?</summary>
    <br>

> The mean center is the average location of crime points

> You will need the following SQL keyword:
> - `AVG(col)` to get the average (= mean) of a column (do it for all Latitude and all Longitude)
> - `GROUP BY col` to group the data by type and year

</details>

<br>

## 🕸️ Create and Visualize an H3 Index Grid

- Create an H3 hexagonal grid to aggregate crimes
- Visualize the grid using KeplerGL

> #### 💡 Pro Tip: you don't need geometries, KeplerGL can read h3 index out-of-the-box 

🆘 I'll give you the SQL code to create an empty h3 grid based on the community areas. To better understand what is happening here you can execute the queries one by one and look at the intermediary results

```SQL
-- create a table with h3 grid
CREATE OR REPLACE TABLE h3_grid AS (
    -- The WITH clause is used to create a CTE (Common Table Expression), 
    -- which is very useful to store temporary results from a query
    WITH hex_strs AS (
        -- for each com_areas geometries, get h3 string identifiers
        SELECT
            -- need to separate the multipolygon in simple polygons
            -- ST_Dump is used to separate the multipolygon in simple polygons
            -- UNNEST is used to flatten the array of simple polygons
            UNNEST(ST_Dump(geometry)).geom.h3_polygon_wkt_to_cells_string(8) as strs
        FROM  
            com_areas
    )
    SELECT 
        -- create a long unique tuple with all h3 str
        UNNEST(strs) h3_str
        , UNNEST(strs).h3_cell_to_boundary_wkt() as h3_geom 
    FROM 
        hex_strs
);
```

🫵 Now you need to:
- add a column to the table crimes for the h3 index
- update the column with the h3 string at level 8 for each crime (assign a h3 string to the crimes)
- SELECT all crimes of of a specific type 
  - JOIN the crimes to the h3 grid 

#### <u>ℹ️ Tips</u>:
<details>
    <summary>💡 Need Help?</summary>
    <br>

> You will need the following SQL keyword:
> - `ALTER TABLE table ADD COLUMN IF NOT EXISTS col type;` to create a new column (think about the type, here it is a string -> VARCHAR in SQL)
> - `UPDATE table SET old_col = new_col` to update the values of the new column
> - `h3_latlng_to_cell_string(lat, lon, h3_level)` to create the h3 id
> - `FROM tab1 JOIN tab2 ON tab1.col = tab2.col` to join two tables

</details>

<br>

## 🎲 Is the spatial distribution of crime counts random?

- calculate the spatial autocorrelation from Moran's I

#### <u>ℹ️ Tips</u>:
<details>
    <summary>💡 Need Help?</summary>
    <br>

> You will need the following functions:  <br>
> 1. calculate the [weights](https://pysal.org/libpysal/generated/libpysal.weights.Rook.html) of the hexagons <br>
> 2. transpose your weights in rows <br>
> 3. calculate the [Moran](https://pysal.org/esda/generated/esda.Moran.html) value from the package esda
> 
> you can find an example [here 👀](https://kazumatsuda.medium.com/exploratory-spatial-data-analysis-esda-spatial-autocorrelation-71b5782c19d6)
</details>
<details>
  <summary>👀 Wanna verify the answer you found?</summary>
    <br>

> Moran's I: 0.662 <br>
> p-value: 0.001 <br>
> => it is significantly  clustered

</details>

<br>

## 👓 Visualize the local spatial autocorrelation with LISA (Local Moran's I) 

- use the same weights calculated before 
- calculate the local spatial autocorrelation with [Moran_Local](https://pysal.org/esda/generated/esda.Moran_Local.html#esda.Moran_Local.__init__)

#### <u>ℹ️ Tips</u>:
<details>
    <summary>💡 Need Help?</summary>
    <br>

> You can follow the same example as before [here 👀](https://kazumatsuda.medium.com/exploratory-spatial-data-analysis-esda-spatial-autocorrelation-71b5782c19d6)
</details>

<br>

## 🥊 Challenges
- Try to calculate and visualize [Getis-Ord Gi*](https://pysal.org/esda/generated/esda.G_Local.html) values
- Create a h3 grid with another level and compare the results

<br>

Congratulations! 🎉 You have successfully completed the exercise. 