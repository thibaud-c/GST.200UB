# 7. Learn SQL and spatial queries with DuckDB

[Tutorial index](README.md) · Previous: [Python](06_python.md) · Next: [Code practices](08_code_practices.md)

## What is DuckDB?

DuckDB is a modern, open-source **analytical database**: software designed to answer questions across many rows, such as “what is the total park area in each district?” Its column-oriented processing handles batches of values efficiently, making it very fast for many filtering, grouping, and joining tasks. Speed still depends on the query, data layout, hardware, and network.

In this course, DuckDB runs inside marimo. You write SQL, a language for querying tables. You can query CSV, JSON, and Parquet files directly, including remote files over HTTPS or in cloud storage. Extensions add more formats and spatial operations.

| Benefits | Limits to keep in mind |
| --- | --- |
| Fast analytical queries without setting up a database server | It is aimed at analysis, rather than a busy application's many small record updates |
| Query files directly, without importing everything first | Remote queries still depend on network speed and file layout |
| Works with Python tables and SQL in the same notebook | Your computer's memory, disk space, and processing power still matter |
| Select just the fields and records you need | File support varies; some sources require an extension |

See [DuckDB's design goals](https://duckdb.org/why_duckdb) for the reasoning behind these tradeoffs.

## What is SQL?

**SQL** means Structured Query Language. It lets you ask questions about tables. A table has rows and named columns. A row might describe one park; its columns might hold a name, an area, and a district. Each column has a data type, such as text, a number, or a Boolean value.

A database organises tables and provides tools to work with them. DuckDB is a database engine; SQL is the language you use to ask it questions. Other engines, including PostgreSQL and SQLite, also use SQL. Much of the basic syntax transfers between them, although file readers and spatial functions differ.

In Python, you might loop through parks and add their areas. In SQL, you describe the result you want, such as a total for each district. The engine decides how to compute it. This is called **declarative programming**.

We will use `SELECT` queries. Each returns a table without changing the source data. SQL can also create tables, add records, and update or delete them, but those operations are outside this lesson.

> [!TIP]
> Say your question out loud before writing SQL. "Which publicly accessible parks cover at least one hectare?" tells you which rows to keep. "What is their total area?" tells you which calculation to use.

## Cheatsheet

Write queries in **SQL cells** inside marimo. Give each result a different output name in the cell's output-variable field.

| SQL | Use |
| --- | --- |
| `SELECT name, area_ha FROM parks` | Choose columns |
| `WHERE area_ha >= 1.0` | Filter rows |
| `ORDER BY area_ha DESC` | Largest first |
| `COUNT(*)`, `SUM(area_ha)`, `AVG(area_ha)` | Count, total, mean |
| `GROUP BY district` | Summarise each district |
| `AS total_area` | Give a result column a readable name |
| `INNER JOIN ... ON ...` | Combine rows with a matching key |
| `LEFT JOIN ... ON ...` | Keep all rows from the left table, including unmatched ones |
| `IS NULL` / `IS NOT NULL` | Find missing / supplied values |
| `read_csv('data/parks.csv')` | Read a local CSV |
| `read_parquet('https://.../file.parquet')` | Read remote Parquet |
| `LIMIT 20` | Return at most 20 rows |

Use the course environment prepared in [uv section 2](01_uv.md#2-install-the-course-packages). It includes marimo's SQL support. Allow two sessions of about 60 minutes, with time for the exercises.

- [Sections 1–4](#1-create-the-data) introduce SQL cells, filtering, and summaries.
- [Section 5](#5-join-two-tables) combines tables using a shared attribute.
- [Section 6](#6-work-with-spatial-sql) works with geometry and spatial relationships.
- [Section 7](#7-connect-a-python-slider-to-sql) adds a slider; [sections 8–10](#8-try-a-tiny-remote-parquet-file) query remote Parquet and Overture buildings.

## 1. Create the data

In VS Code, create `practice/data/parks.csv`, using the file-creation steps in [VS Code section 4](02_vscode.md#4-create-a-file-and-preview-it):

```csv
park_id,name,district,area_ha,public_access
1,Mur Meadow,North,0.5,true
2,Hill Garden,North,1.2,false
3,River Park,North,2.0,true
4,Oak Square,South,0.8,true
5,School Garden,South,1.5,false
6,South Meadow,South,3.0,true
```

Save it. Each row describes a park; each column holds an attribute. CSV means comma-separated values. The first row names the columns. Use decimal points and no thousands separators.

Create a marimo notebook called `practice/duckdb_parks.py` through the VS Code Command Palette, as in [marimo section 2](05_marimo.md#2-open-or-create-a-notebook). Select the course `.venv` kernel. The examples assume its working folder is `practice`, so the CSV path is `data/parks.csv`. See [how to check relative paths, CLI section 3](03_cli.md#relative-paths-in-a-notebook).

If `.venv` is missing from the kernel picker after `uv sync`, follow [the VS Code interpreter-path fallback, section 5](02_vscode.md#5-install-python-and-marimo-support).

## 2. Create and run a SQL cell

Before adding SQL examples, enter this in a **Python setup cell** and run it:

```python
import marimo as mo
```

If the notebook already contains this import in a Python cell, run that cell instead. Keep only one cell defining `mo`.

Before running the first SQL cell, open marimo's settings in the top right of the notebook. Set **SQL output type** to `pandas`. This makes query results pandas **DataFrames**, tables with rows and columns. Keep this setting for the whole lesson and rerun existing SQL cells if you change it. See [marimo's SQL output settings](https://docs.marimo.io/guides/working_with_data/sql/#sql-output-types).

SQL expresses questions about tables. DuckDB executes them, and marimo displays the results.

1. Add an empty cell and select **SQL** from its language selector or cell menu. In marimo's browser editor, the **SQL** button at the bottom also creates one.
2. Keep the default DuckDB engine. No connection setup is needed.
3. In the output-variable field, replace the default private name, often `_df`, with `parks`. A name starting with `_` is local to that cell.
4. Enter only this SQL and run the cell:

```sql
SELECT * FROM read_csv('data/parks.csv');
```

Expect six rows and five columns. `FROM` identifies the input, `SELECT *` requests all columns, and the semicolon ends the statement. `read_csv` detects the column types. Paths and text values use single quotes.

> [!IMPORTANT]
> Give every SQL cell in this lesson its own output variable name. The first cell owns `parks`; later cells can read `FROM parks`, but must use another output name, such as `large_parks` or `parks_count`. If marimo reports **This cell redefines variables**, change the new cell's output-variable field. To change the original `parks` query, edit its existing cell. This rule also applies to shared names defined in Python cells.

> [!TIP]
> If your VS Code extension has no SQL cell option, update it. You can also use marimo's browser editor for this lesson: from the separate terminal, enter `practice` and run `uv run marimo edit duckdb_parks.py`. Its SQL cells use the same saved notebook. Avoid editing the file in two editors at once.

### What happens under the hood?

marimo saves a SQL cell as Python resembling this:

```python
parks = mo.sql("SELECT * FROM read_csv('data/parks.csv');")
# This is why we imported marimo as mo before
```

This is an explanation of the saved file, **not another cell to add**. Adding it again would define `parks` twice. The editor writes this wrapper for you. All query examples below belong in SQL cells.

> [!NOTE]
> DuckDB runs inside the notebook's Python process. The default database is in memory, so there is no database server or password to configure. A named query result can be used by later cells. Restarting the kernel clears these results; rerun the notebook to recreate them. Saving the notebook saves code, not a permanent database or a copy of its input files.

With the `pandas` output setting, each small query result is a DataFrame in memory. Later summaries can use that downloaded sample without querying the remote file again. In a Python cell, try `parks.head()` to inspect its first rows. `df` is a common name for a DataFrame; here `parks` names the particular table. A GeoPandas GeoDataFrame, often named `gdf`, adds a geometry column and a coordinate system. These SQL results are ordinary DataFrames.

## 3. Select, filter, and sort

Add a SQL cell with output name `large_parks`:

```sql
SELECT name, district, area_ha
FROM parks
WHERE area_ha >= 1.0
ORDER BY area_ha DESC, name;
```

`WHERE` keeps matching rows. `DESC` sorts largest first; `name` breaks ties. Expect:

| name | district | area_ha |
| --- | --- | --- |
| South Meadow | South | 3.0 |
| River Park | North | 2.0 |
| School Garden | South | 1.5 |
| Hill Garden | North | 1.2 |

### Read a query one clause at a time

A **clause** is a part of the query, such as `WHERE area_ha >= 1.0`. To understand the query above, ask:

| Clause | Question | In this example |
| --- | --- | --- |
| `FROM` | Which table supplies the records? | `parks` |
| `WHERE` | Which records should remain? | Area of at least 1 hectare |
| `SELECT` | Which columns should appear? | Name, district, area |
| `ORDER BY` | In which order? | Area from largest to smallest, then name |
| `LIMIT` | How many result rows at most? | No limit in this query |

This is a way to reason through the question. Write the clauses in the SQL order shown in the examples, starting with `SELECT`. Without `ORDER BY`, the result order is not guaranteed.

SQL keywords such as `SELECT` can be lowercase. We use uppercase so they stand out from column names. New lines make a query easier to read; they do not end it. A semicolon ends a statement. Start a SQL comment with `--`, for example `-- Keep parks of at least one hectare`.

Change the threshold to `2.0`, predict the rows, run, then restore `1.0`. This changes the result, not the CSV.

Add another SQL cell, output `public_parks`:

```sql
SELECT name, area_ha
FROM parks
WHERE public_access = true AND area_ha >= 1.0
ORDER BY area_ha DESC;
```

`AND` requires both conditions. Expect South Meadow and River Park, totalling 5 hectares. Why is Hill Garden excluded?

> [!IMPORTANT]
> SQL compares equality with `=`; Python uses `==`. SQL text needs quotes, such as `district = 'North'`. Boolean values such as `true` do not.

Other useful conditions are `area_ha < 1.0`, `district IN ('North', 'South')`, and `NOT public_access`. `OR` keeps a row when either condition is true. Use parentheses when combining `AND` and `OR`, so your intention is clear.

## 4. Group and summarise

An **aggregate function** combines several rows into one result. `COUNT` counts records, `SUM` adds values, and `AVG` calculates their mean. With `GROUP BY district`, each district gets its own result.

In a SQL cell, output `district_summary`:

```sql
SELECT district,
       COUNT(*) AS park_count,
       ROUND(SUM(area_ha), 2) AS total_area_ha,
       ROUND(AVG(area_ha), 2) AS mean_area_ha
FROM parks
GROUP BY district
ORDER BY district;
```

`AS` names a result column. `ROUND(..., 2)` rounds a number to two decimal places. Each selected column must either identify a group, as `district` does here, or be part of an aggregate calculation.

| district | park_count | total_area_ha | mean_area_ha |
| --- | --- | --- | --- |
| North | 3 | 3.7 | 1.23 |
| South | 3 | 5.3 | 1.77 |

Check the North total by hand. These summaries include parks without public access. Add a filter to see how that changes the question.

> [!NOTE]
> Missing values are `NULL`, not zero. `COUNT(*)` counts rows; `COUNT(area_ha)` counts non-missing areas. `AVG` ignores missing values. Test for missing data with `IS NULL`, not `= NULL`.

## 5. Join two tables

Suppose maintenance teams are stored separately from the parks. A **join** combines records from two tables using a condition. Here, the shared district name is the **join key**.

Create `practice/data/districts.csv` in VS Code, as in [section 1](#1-create-the-data):

```csv
district,maintenance_team
North,Team A
South,Team B
East,Team C
```

In a SQL cell, output `districts`:

```sql
SELECT * FROM read_csv('data/districts.csv');
```

### Match records with INNER JOIN

Add a SQL cell, output `park_teams`:

```sql
SELECT p.park_id, p.name, p.district, d.maintenance_team
FROM parks AS p
INNER JOIN districts AS d ON p.district = d.district
ORDER BY p.park_id;
```

`p` and `d` are short names, called **table aliases**. `p.district` means the district column from `parks`; `d.district` means the column from `districts`. `ON` supplies the matching rule. This join adds a team to each park.

Expect six rows. The three North parks get Team A, and the three South parks get Team B. East has no matching park, so an `INNER JOIN` leaves it out. Trace the match for River Park by hand before running the query.

### Keep unmatched records with LEFT JOIN

Now start from `districts`, so every district appears. In a SQL cell, output `district_parks`:

```sql
SELECT d.district, d.maintenance_team, p.name AS park_name
FROM districts AS d
LEFT JOIN parks AS p ON d.district = p.district
ORDER BY d.district, p.name;
```

Expect seven rows. North and South each match three parks. East remains as one row with a missing `park_name`. A `LEFT JOIN` keeps every row from the table written to the left of the join, even when the other table has no match. See [DuckDB's JOIN documentation](https://duckdb.org/docs/current/sql/query_syntax/from#joins).

> [!IMPORTANT]
> A join can increase the number of rows. Here, one district matches several parks. If you accidentally list North twice in `districts.csv`, every North park gets two matches. Check the key and row counts before calculating totals; removing duplicates afterward may hide the problem. Real datasets often use stable district IDs instead of names.

Try replacing `LEFT JOIN` with `INNER JOIN` in the same cell. Which district disappears, and why? Restore `LEFT JOIN` before continuing.

## 6. Work with spatial SQL

Spatial SQL applies the same querying ideas to geometry. You can measure polygons, transform coordinates, and match points to areas. The `ST_` prefix is used for spatial functions. If you have used GeoPandas, the underlying GIS questions are the same.

### Load the spatial extension

Add a SQL cell, output `spatial_setup`, and run it before the geometry queries:

```sql
INSTALL spatial;
LOAD spatial;
```

`INSTALL` downloads the extension the first time; `LOAD` makes its functions available in the current DuckDB session. After a kernel restart, run this cell again. It may show no table, which is expected. You do not need another Python package or a database connection. See [the spatial extension setup](https://duckdb.org/docs/current/core_extensions/spatial/overview).

### Create and inspect geometry

A geometry can describe a point, a line, or a polygon. **WKT**, Well-Known Text, writes a geometry as readable text. For example, `POINT (15.44 47.07)` contains an x and a y coordinate. A polygon lists its boundary coordinates and closes the ring by repeating the first coordinate at the end.

We will use two adjacent squares. Their coordinates are in **EPSG:32633**, WGS 84 / UTM zone 33N, a projected coordinate reference system suitable for local work around Graz. Coordinates are eastings and northings in metres. Each square is 1,000 metres wide and 1,000 metres high.

In a SQL cell, output `district_shapes`:

```sql
SELECT *
FROM (VALUES
    ('North', 'POLYGON ((500000 5210000, 501000 5210000, 501000 5211000, 500000 5211000, 500000 5210000))'),
    ('South', 'POLYGON ((500000 5209000, 501000 5209000, 501000 5210000, 500000 5210000, 500000 5209000))')
) AS shapes(district, wkt);
```

`VALUES` creates a small table directly in SQL. Each pair of values becomes a row; `shapes(district, wkt)` gives the table and its columns names. The result has two rows. Sketch the squares using their coordinates. Where do they touch?

> [!NOTE]
> We pass geometry between these SQL cells as WKT text, so the results remain ordinary pandas DataFrames. Inside a query, `ST_GeomFromText(wkt)` converts that text to DuckDB geometry; `ST_AsText(...)` converts a geometry result back to text. WKT alone does not record its CRS. Keep track of the CRS yourself, and use the same CRS for geometries you compare.

### Measure area and find a point inside

In a SQL cell, output `measured_districts`:

```sql
SELECT district,
       ST_GeometryType(ST_GeomFromText(wkt)) AS geometry_type,
       ST_Area(ST_GeomFromText(wkt)) AS area_m2,
       ST_AsText(
           ST_PointOnSurface(ST_GeomFromText(wkt))
       ) AS inside_point_wkt
FROM district_shapes
ORDER BY district;
```

Read a nested expression from the inside out. `ST_GeomFromText` first creates the geometry, `ST_PointOnSurface` finds a point on it, then `ST_AsText` displays that point as text.

Expect `POLYGON` and `1000000` square metres for each row. For a valid, non-empty polygon, `ST_PointOnSurface` gives an interior point. It is useful for a label or a representative location. A centroid can fall outside a concave polygon, and neither method identifies an entrance.

> [!IMPORTANT]
> `ST_Area` uses the geometry's coordinate units squared. Here they are square metres. Computing it directly on longitude and latitude would produce square degrees, not square metres. Choose an appropriate projected CRS before measuring area; projection distortion still matters.

### Reproject a point

Longitude and latitude are useful for locating Graz on Earth. We need projected coordinates for local measurements in metres. In a SQL cell, output `projected_point`:

```sql
SELECT ST_AsText(
    ST_Transform(
        ST_Point(15.44, 47.07),
        'EPSG:4326', 'EPSG:32633', always_xy := true
    )
) AS projected_wkt;
```

`ST_Point(x, y)` creates the point. `ST_Transform` takes its source CRS and target CRS and calculates new coordinates. With `always_xy := true`, we explicitly use longitude then latitude, and easting then northing. Expect approximately `POINT (533407.5 5213036.9)`. The location stays the same; its coordinate values and units change.

### Test overlap and calculate the intersection

`ST_Intersects` answers a yes/no question. `ST_Intersection` returns the shared geometry. They do different jobs.

`ST_MakeEnvelope(xmin, ymin, xmax, ymax)` makes a rectangle. Use one that overlaps the top-right quarter of the North square. In a SQL cell, output `north_overlap`:

```sql
SELECT district,
       ST_Intersects(
           ST_GeomFromText(wkt),
           ST_MakeEnvelope(500500, 5210500, 501500, 5211500)
       ) AS overlaps,
       ST_Area(
           ST_Intersection(
               ST_GeomFromText(wkt),
               ST_MakeEnvelope(500500, 5210500, 501500, 5211500)
           )
       ) AS shared_area_m2
FROM district_shapes
WHERE district = 'North';
```

Expect `true` and `250000` square metres. The shared rectangle is 500 metres by 500 metres. Wrap the `ST_Intersection(...)` expression in `ST_AsText(...)` instead of `ST_Area(...)` to inspect its boundary coordinates.

### Join points to districts

A **spatial join** matches records using a spatial relationship rather than an equal attribute. Let's ask which districts each site falls in or touches.

In a SQL cell, output `site_points`. These coordinates also use EPSG:32633:

```sql
SELECT *
FROM (VALUES
    ('School', 500200, 5210400),
    ('Clinic', 500800, 5209500),
    ('Border', 500500, 5210000),
    ('Outside', 502000, 5210500)
) AS sites(name, x, y);
```

Predict the matches from your sketch. Then add a SQL cell, output `sites_by_district`:

```sql
SELECT p.name, d.district
FROM site_points AS p
LEFT JOIN district_shapes AS d
    ON ST_Intersects(ST_Point(p.x, p.y), ST_GeomFromText(d.wkt))
ORDER BY p.name, d.district;
```

| name | district |
| --- | --- |
| Border | North |
| Border | South |
| Clinic | South |
| Outside | NULL |
| School | North |

There are five result rows for four sites. Border touches both districts, so it matches twice. Outside has no match; the `LEFT JOIN` keeps it. Missing district values may appear as `None` in pandas.

> [!TIP]
> The spatial relationship is part of your research decision. `ST_Intersects` includes touching boundaries. Replacing it with `ST_Within(point, polygon)` excludes a point on the polygon boundary, so Border would have no match here. Neither choice automatically assigns a boundary point to exactly one district. Decide how to handle this before counting sites by district.

### Make a buffer

`ST_Buffer` creates an area around a geometry. In a SQL cell, output `site_buffers`:

```sql
SELECT name,
       ST_AsText(ST_Buffer(ST_Point(x, y), 250)) AS buffer_wkt
FROM site_points
ORDER BY name;
```

The radius is 250 metres because these coordinates use metres. The output polygons approximate circles. This is straight-line proximity; it does not account for streets, crossings, or walking routes. See how [Lab 01](../lab_01/README.md) uses buffers to study access to supermarkets.

The [spatial function reference](https://duckdb.org/docs/current/core_extensions/spatial/functions) documents these functions. Start with their signatures and small examples; you do not need the whole list.

## 7. Connect a Python slider to SQL

Use the `mo` imported in your setup cell. Add another **Python cell**:

```python
min_area = mo.ui.slider(0.0, 3.0, step=0.5, value=1.0,
                        label="Minimum area in hectares", show_value=True)
min_area
```

In a **SQL cell**, output `selected_parks`:

```sql
SELECT name, area_ha
FROM parks
WHERE area_ha >= {min_area.value}
ORDER BY area_ha DESC, name;
```

The braces insert the slider's numeric value through marimo. They are not ordinary SQL syntax. At `1.0`, expect four parks. At `2.5`, expect one. In automatic execution mode, the query updates as the slider changes. Keep this pattern for bounded numeric inputs; arbitrary user text needs bound query parameters.

## 8. Try a tiny remote Parquet file

**Apache Parquet** is an open, binary file format for tables. Within each group of rows, it stores values by column: names together, areas together, and so on. It records data types, so an area can remain numeric instead of being inferred from text as in CSV. Parquet is a file format; DuckDB is an engine that reads and queries it.

| Benefits | Drawbacks |
| --- | --- |
| Compression often makes files smaller than CSV | You need software to inspect it; a text editor cannot show its rows |
| Readers can fetch only the columns a query needs | Updating one record usually means rewriting a file or part of a dataset |
| Types and nested fields can travel with the data | Different files may have incompatible schemas, which still need checking |
| Metadata can let a reader skip irrelevant blocks | Skipping depends on the file layout and filters; a small result can still require substantial reading |

For example, querying only building heights need not read every building name. A geographic filter helps most when the file's metadata can rule out blocks outside the area. Read the [Apache Parquet overview](https://parquet.apache.org/docs/overview/) for more detail.

DuckDB can query a remote Parquet file without you downloading it manually. Internet access is required.

This small file comes from Apache's Parquet test-data repository. Its artificial column names make it useful for learning the file-reading step before a geographic query. In a SQL cell, output `remote_example`:

```sql
SELECT id, int_col, double_col
FROM read_parquet(
    'https://raw.githubusercontent.com/apache/parquet-testing/master/data/alltypes_plain.parquet'
)
ORDER BY id;
```

Expect eight rows. Compare the selected columns with `SELECT *` in the same cell. Then query `remote_example` in a new SQL cell and count its rows.

> [!NOTE]
> DuckDB normally installs and loads its `httpfs` extension automatically for remote files. It handles HTTP requests inside the notebook. If automatic loading is disabled, run `INSTALL httpfs; LOAD httpfs;` in a SQL cell once, then rerun the query. No Python connection object is needed.

Selecting columns and filtering rows can reduce data transfer, but `LIMIT` caps returned rows, not network traffic. DuckDB still reads file metadata and relevant data blocks.

## 9. Find Overture releases through STAC

**STAC** means SpatioTemporal Asset Catalog. It is a standard way to describe geographic datasets and link to their files. A catalog groups datasets, a collection describes a related set, an item describes a spatial asset's footprint and metadata, and an asset link points to a data file. Catalog JSON is metadata, not the building geometries themselves.

Open [Overture's catalog](https://stac.overturemaps.org/catalog.json). Its `latest` field is an Overture-specific convenience, not a required STAC field. Read it in a SQL cell with output name `release_catalog`:

```sql
SELECT latest
FROM read_json_auto('https://stac.overturemaps.org/catalog.json');
```

In a **Python cell**, build a path using that result:

```python
overture_release = release_catalog["latest"].iloc[0]
buildings_path = (
    "s3://overturemaps-us-west-2/release/"
    f"{overture_release}/theme=buildings/type=building/*"
)
overture_release
```

`release_catalog["latest"]` selects the pandas column, and `.iloc[0]` reads its first value by position. The `*` selects the building files in the release. This avoids a hard-coded release date and a particular file identifier.

> [!TIP]
> Record the displayed release in your notes. For a repeatable comparison, replace the catalog lookup in the Python assignment with that recorded release string. "Latest" can change between two runs. A new schema may still require changing the query; finding the release automatically does not guarantee schema compatibility.

## 10. Query a small area of Graz

In a SQL cell, set the public bucket's region:

```sql
SET s3_region = 'us-west-2';
```

Run it before the next query. This is a session setting; repeat it after restarting the kernel. Then add a SQL cell with output name `graz_buildings`:

```sql
SELECT id, names.primary AS name, height, bbox
FROM read_parquet('{buildings_path}', hive_partitioning = true)
WHERE bbox.xmin <= 15.445 AND bbox.xmax >= 15.435
  AND bbox.ymin <= 47.076 AND bbox.ymax >= 47.070
LIMIT 20;
```

The rectangle runs from longitude 15.435 to 15.445 and latitude 47.070 to 47.076. These are WGS 84 degrees. The conditions find building bounding boxes that overlap it. A bounding-box match is a candidate spatial filter, not an exact footprint intersection.

`names.primary` reads a nested name field. `hive_partitioning` recognises folder labels such as `theme=buildings`. Expect at most 20 rows; names and heights may be missing. Height is in metres when supplied. There is no row ordering, so the sample can vary.

> [!NOTE]
> `None` in Python, or `NULL` in a SQL table, means an attribute is missing. Many buildings have no recorded name or height; even a sample with every height missing is normal. It does not mean the query failed. A missing height is unknown, so do not replace it with zero. Use `COUNT(height)` to count supplied heights and `height IS NULL` to find missing ones.

> [!WARNING]
> Allow tens of seconds to several minutes for this wildcard query: DuckDB inspects metadata across the release before returning the small sample.
>
> If you see `RuntimeError: Query interrupted`, wait until the previous run has stopped, then rerun the same query cell. If you restarted the kernel, rerun the setup, release lookup, path, and region-setting cells first. If interruptions continue, keep the error message and ask for help. You can practise remote SQL with the small Parquet example while troubleshooting.

For larger work, follow the catalog's links to the building collection and inspect item footprints to select files overlapping your area. Use their asset URLs instead of guessing file identifiers. The [Overture DuckDB guide](https://docs.overturemaps.org/getting-data/duckdb/) explains the full-release pattern; the [catalog guide](https://docs.overturemaps.org/getting-data/) explains discovery. Check [attribution](https://docs.overturemaps.org/attribution/) when sharing Overture data.

## If something fails

| Symptom | First check |
| --- | --- |
| CSV not found | Check `Path.cwd()` and the relative path |
| `NameError: name 'mo' is not defined` | Run the Python setup cell containing `import marimo as mo` from [section 2](#2-create-and-run-a-sql-cell) |
| A SQL result does not support pandas methods | Set the SQL output type to `pandas` and rerun its cell, as in [section 2](#2-create-and-run-a-sql-cell) |
| `parks` is missing | Name the first result `parks` and run its cell |
| A result cannot be reused | Remove the leading underscore from its output name |
| `This cell redefines variables` | Rename the new cell's output, such as `parks_count`; keep `parks` defined only in its original cell |
| A CSV edit is not reflected | Save the CSV and rerun its reading cell |
| A join returns more rows than expected | Inspect matching keys and boundary points; see [section 5](#5-join-two-tables) and [spatial joins](#join-points-to-districts) |
| An `ST_` function is missing | Run the `spatial_setup` SQL cell before the query, including after a restart; see [section 6](#load-the-spatial-extension) |
| A geometry argument has the wrong type | Use `ST_GeomFromText(wkt)` for the WKT column; plain text is not geometry |
| Spatial results have implausible areas or no matches | Check CRS, units, and coordinate order; see [reprojection](#reproject-a-point) |
| Remote access fails | Check internet access and the URL; allow the extension installation to complete |
| S3 path fails | Rerun the region setting and inspect `buildings_path` and the catalog |
| `RuntimeError: Query interrupted` | Let the previous run stop, then rerun the cell; see [section 10](#10-query-a-small-area-of-graz) |
| Names or heights show `None` / `NULL` | These are missing attributes; see [section 10](#10-query-a-small-area-of-graz) |
| Overture field missing | Check the selected release's schema |

## Documentation and a video

- [marimo SQL cells](https://docs.marimo.io/guides/working_with_data/sql/) and [SQL/Python video](https://www.youtube.com/watch?v=IHEf5HwU7R0).
- [pandas introduction](https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html): inspecting and selecting rows in DataFrames.
- [DuckDB CSV](https://duckdb.org/docs/current/data/csv/overview), [SELECT](https://duckdb.org/docs/current/sql/query_syntax/select), and [aggregates](https://duckdb.org/docs/current/sql/functions/aggregates).
- [DuckDB SQL introduction](https://duckdb.org/docs/current/sql/introduction) and [JOIN documentation](https://duckdb.org/docs/current/sql/query_syntax/from#joins): the language basics and matching rules.
- [Introducing DuckDB's spatial extension](https://duckdb.org/2023/04/28/spatial): a worked blog introduction. Its Python connection examples use a different interface; use SQL cells for this course. Keep the [current spatial function reference](https://duckdb.org/docs/current/core_extensions/spatial/functions) beside the lesson.
- [DuckDB remote Parquet](https://duckdb.org/docs/current/core_extensions/httpfs/https) and [Apache's test datasets](https://github.com/apache/parquet-testing).
- [STAC introduction](https://stacspec.org/en/about/stac-spec/) and [Overture building schema](https://docs.overturemaps.org/schema/reference/buildings/building/).

## Exercise: predict, query, explain

1. In SQL cells, count publicly accessible parks of at least `1.0` hectare and total their area. Give each result a unique output name (see [section 2](#2-create-and-run-a-sql-cell), [section 3](#3-select-filter-and-sort), and [section 4](#4-group-and-summarise)).
2. Predict the result at `0.5`, then run it (see [section 3](#3-select-filter-and-sort)).
3. Add `7,Canal Pocket,South,0.4,true` to the CSV. Save and rerun its reading cell. Does either filtered summary change? What happens to the South total (see [section 1](#1-create-the-data) and [section 4](#4-group-and-summarise))?
4. Use a `LEFT JOIN` and `GROUP BY` to count parks in every district, including East. First remove the extra CSV row, save, and rerun the reading cell. Should you count `*` or `p.park_id` to get zero for East? Explain your choice (see [section 1](#1-create-the-data), [section 4](#4-group-and-summarise), and [section 5](#5-join-two-tables)).
5. In the spatial join, replace `ST_Intersects` with `ST_Within`. Predict Border's result and the total number of output rows before running. Why is checking only the row count insufficient (see [section 6, spatial joins](#join-points-to-districts))?
6. Change the overlap rectangle so it covers the whole North square. Predict its intersection area, then check it. Explain why measuring the same polygon in longitude/latitude would not give square metres (see [section 6, intersection](#test-overlap-and-calculate-the-intersection) and [area units](#measure-area-and-find-a-point-inside)).
7. Transform `projected_point` back to EPSG:4326 in a new SQL cell. Use `ST_GeomFromText(projected_wkt)`, swap source and target CRS, and keep `always_xy := true`. Which coordinate should come first (see [section 6, reprojection](#reproject-a-point))?
8. Query `remote_example` to check its row count. Explain what changed when the input moved from a local CSV to remote Parquet (see [section 4](#4-group-and-summarise) and [section 8](#8-try-a-tiny-remote-parquet-file)).
9. If you completed Overture, change the limit to `10`. In a new SQL cell, compare `COUNT(*)` with `COUNT(height)` from the `graz_buildings` DataFrame. Explain why these are sample counts, not totals for Graz. Record the release (see [section 4](#4-group-and-summarise), [section 9](#9-find-overture-releases-through-stac), and [section 10](#10-query-a-small-area-of-graz)).

<details>
<summary>Check your results</summary>

At `1.0`, two accessible parks total 5 hectares. At `0.5`, four total 6.3 hectares. The new park changes neither result; the South total for all parks becomes 5.7 hectares.

With the original six parks, the joined district counts are North 3, South 3, East 0. Use `COUNT(p.park_id)`; `COUNT(*)` would count East's unmatched row as one. With the extra park, South becomes 4.

With `ST_Within`, Border has a missing district. The left join returns four rows, but both Border and Outside are unmatched. The original `ST_Intersects` query has five rows because Border matches twice. Counts alone cannot tell you whether every site has a suitable assignment.

The whole North square covers 1,000,000 square metres. The round-trip point is approximately `POINT (15.44 47.07)`, longitude first. The Apache sample has eight rows. `COUNT(height)` excludes `NULL` and cannot exceed `COUNT(*)`.

</details>
