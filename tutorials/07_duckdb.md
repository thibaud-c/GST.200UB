# 7. Query tables and remote data with DuckDB

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

## Cheatsheet

Write queries in **SQL cells** inside marimo. Give each result a different output name in the cell's output-variable field.

| SQL | Use |
| --- | --- |
| `SELECT name, area_ha FROM parks` | Choose columns |
| `WHERE area_ha >= 1.0` | Filter rows |
| `ORDER BY area_ha DESC` | Largest first |
| `COUNT(*)`, `SUM(area_ha)`, `AVG(area_ha)` | Count, total, mean |
| `GROUP BY district` | Summarise each district |
| `read_csv('data/parks.csv')` | Read a local CSV |
| `read_parquet('https://.../file.parquet')` | Read remote Parquet |
| `LIMIT 20` | Return at most 20 rows |

Allow 60 to 90 minutes. Use the course environment prepared in [uv section 2](01_uv.md#2-install-the-course-packages). It includes marimo's SQL support. You will query park records, try a tiny remote Parquet file, then query Overture buildings.

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

## 4. Group and summarise

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

`GROUP BY` makes one summary per district. `AS` names a column. `ROUND` controls displayed precision.

| district | park_count | total_area_ha | mean_area_ha |
| --- | --- | --- | --- |
| North | 3 | 3.7 | 1.23 |
| South | 3 | 5.3 | 1.77 |

Check the North total by hand. These summaries include parks without public access. Add a filter to see how that changes the question.

> [!NOTE]
> Missing values are `NULL`, not zero. `COUNT(*)` counts rows; `COUNT(area_ha)` counts non-missing areas. `AVG` ignores missing values. Test for missing data with `IS NULL`, not `= NULL`.

## 5. Connect a Python slider to SQL

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

## 6. Try a tiny remote Parquet file

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

## 7. Find Overture releases through STAC

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

## 8. Query a small area of Graz

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
| `NameError: name 'mo' is not defined` | Run the Python setup cell containing `import marimo as mo` from section 2 |
| A SQL result does not support pandas methods | Set the SQL output type to `pandas` and rerun its cell, as in section 2 |
| `parks` is missing | Name the first result `parks` and run its cell |
| A result cannot be reused | Remove the leading underscore from its output name |
| `This cell redefines variables` | Rename the new cell's output, such as `parks_count`; keep `parks` defined only in its original cell |
| A CSV edit is not reflected | Save the CSV and rerun its reading cell |
| Remote access fails | Check internet access and the URL; allow the extension installation to complete |
| S3 path fails | Rerun the region setting and inspect `buildings_path` and the catalog |
| `RuntimeError: Query interrupted` | Let the previous run stop, then rerun the cell; see section 8 |
| Names or heights show `None` / `NULL` | These are missing attributes; see section 8 |
| Overture field missing | Check the selected release's schema |

## Documentation and a video

- [marimo SQL cells](https://docs.marimo.io/guides/working_with_data/sql/) and [SQL/Python video](https://www.youtube.com/watch?v=IHEf5HwU7R0).
- [pandas introduction](https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html): inspecting and selecting rows in DataFrames.
- [DuckDB CSV](https://duckdb.org/docs/current/data/csv/overview), [SELECT](https://duckdb.org/docs/current/sql/query_syntax/select), and [aggregates](https://duckdb.org/docs/current/sql/functions/aggregates).
- [DuckDB remote Parquet](https://duckdb.org/docs/current/core_extensions/httpfs/https) and [Apache's test datasets](https://github.com/apache/parquet-testing).
- [STAC introduction](https://stacspec.org/en/about/stac-spec/) and [Overture building schema](https://docs.overturemaps.org/schema/reference/buildings/building/).

## Exercise: predict, query, explain

1. In SQL cells, count publicly accessible parks of at least `1.0` hectare and total their area. Give each result a unique output name (see [section 2](#2-create-and-run-a-sql-cell), [section 3](#3-select-filter-and-sort), and [section 4](#4-group-and-summarise)).
2. Predict the result at `0.5`, then run it (see [section 3](#3-select-filter-and-sort)).
3. Add `7,Canal Pocket,South,0.4,true` to the CSV. Save and rerun its reading cell. Does either filtered summary change? What happens to the South total (see [section 1](#1-create-the-data) and [section 4](#4-group-and-summarise))?
4. Query `remote_example` to check its row count. Explain what changed when the input moved from a local CSV to remote Parquet (see [section 4](#4-group-and-summarise) and [section 6](#6-try-a-tiny-remote-parquet-file)).
5. If you completed Overture, change the limit to `10`. In a new SQL cell, compare `COUNT(*)` with `COUNT(height)` from the `graz_buildings` DataFrame. Explain why these are sample counts, not totals for Graz. Record the release (see [section 4](#4-group-and-summarise), [section 7](#7-find-overture-releases-through-stac), and [section 8](#8-query-a-small-area-of-graz)).

<details>
<summary>Check your results</summary>

At `1.0`, two accessible parks total 5 hectares. At `0.5`, four total 6.3 hectares. The new park changes neither result; the South total for all parks becomes 5.7 hectares. The Apache sample has eight rows. `COUNT(height)` excludes `NULL` and cannot exceed `COUNT(*)`.

</details>
