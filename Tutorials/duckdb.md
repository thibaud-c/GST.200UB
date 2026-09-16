# 7. Query tables and Overture data with DuckDB

[Tutorial index](README.md) · Previous: [Python](python.md)

## Cheatsheet

Run queries through `mo.sql(...)` in Python cells in your VS Code marimo notebook.

| SQL | Use |
| --- | --- |
| `SELECT name, area_ha FROM parks` | Choose columns |
| `WHERE area_ha >= 1.0` | Filter rows |
| `ORDER BY area_ha DESC` | Put the largest areas first |
| `COUNT(*)`, `SUM(area_ha)` | Count rows or add values |
| `GROUP BY district` | Summarize separately for each district |
| `read_csv('path.csv')` | Query a CSV file |
| `read_parquet('https://.../file.parquet')` | Query remote Parquet data |
| `LIMIT 20` | Return at most 20 rows |

The snippets are a reference, not complete cells. The full examples below include the Python wrapper and real paths.

Allow about 60 to 90 minutes. Complete the uv, marimo, and Python tutorials first. You will query local park records, then read a small selection of Overture buildings from remote Parquet files. No previous SQL knowledge is assumed.

## 1. The question and the tools

Suppose you have a park survey and want to know which parks cover at least one hectare. Later, you want a total for each district.

A **table** has rows and columns. Here, each row describes a park and each column holds an attribute, such as its name or area. **SQL**, Structured Query Language, expresses questions about tables. **DuckDB** executes those questions. **marimo** provides the notebook editor and displays the results.

We will call `mo.sql` from Python cells in marimo. It runs SQL through an in-memory DuckDB connection and displays the result. The notebook stays inside VS Code. The [marimo SQL guide](https://docs.marimo.io/guides/working_with_data/sql/) explains that integration.

> [!NOTE]
> All names, districts, and measurements below are fictional teaching data. The table has attributes but no geometry. Area summaries are useful practice, but this dataset cannot answer which park is nearest to a home or whether access is equitable.

## 2. Create the dataset in VS Code

In the course's `practice` folder, create a folder called `data`. Inside it, create `parks.csv` and paste:

```csv
park_id,name,district,area_ha,public_access
1,Mur Meadow,North,0.5,true
2,Hill Garden,North,1.2,false
3,River Park,North,2.0,true
4,Oak Square,South,0.8,true
5,School Garden,South,1.5,false
6,South Meadow,South,3.0,true
```

Save the file. CSV means comma-separated values. The first line gives column names; the next six lines are records. Use commas between fields and decimal points inside numbers. Do not add thousands separators.

| Column | Meaning | Example |
| --- | --- | --- |
| `park_id` | An identifier that distinguishes each park | `1` |
| `name` | Park name, stored as text | `Mur Meadow` |
| `district` | A fictional district label | `North` |
| `area_ha` | Park area in hectares | `0.5` |
| `public_access` | Whether the survey marks public access as available | `true` |

> [!TIP]
> Use VS Code for this small CSV. Spreadsheet applications may change separators or decimal formatting according to regional settings.

## 3. Open a marimo notebook in VS Code

Use the Command Palette to run **Create: New marimo notebook**. Save it as `practice/duckdb_parks.py` and select the course `.venv` kernel. To reopen it later, choose **marimo: Open as marimo notebook**.

In a Python cell, run:

```python
import marimo as mo
```

Keep only one copy of this import if the editor already supplied it. In a second cell:

```python
csv_path = (mo.notebook_dir() / "data" / "parks.csv").as_posix()
print(csv_path)
```

This locates `data/parks.csv` beside the notebook. `.as_posix()` writes the path with forward slashes, which work in this DuckDB query on Windows too. Check that the printed path identifies your saved CSV.

## 4. Read your first SQL result

Add a Python cell:

```python
parks = mo.sql(f"""
    SELECT *
    FROM read_csv('{csv_path}');
""")
```

The three quotes enclose a multiline string containing SQL. `mo.sql` executes it, displays the table, and assigns the result to `parks`. The `f` lets Python insert the path from the previous cell. Later cells can query the named `parks` result.

You should see six rows and five columns:

- `read_csv(...)` reads the file and infers its column types.
- `FROM` identifies the data being queried.
- `SELECT *` returns every column.
- The semicolon ends the SQL statement.

Use single quotes around SQL text and paths. In these examples, the inserted paths and numeric controls are values you create yourself. For arbitrary text supplied by other users, use bound query parameters rather than inserting it into SQL.

> [!IMPORTANT]
> These examples go in **Python cells**, including the `mo.sql` wrapper. 

> [!TIP]
> Marimo notebooks provide a SQL type cell that allows you to write SQL queries directly. In these cells you don't need to use the `mo.sql` wrapper.

The [DuckDB CSV guide](https://duckdb.org/docs/current/data/csv/overview) explains type detection. For this file, expect an integer ID, text names and districts, a numeric area, and Boolean access values.

## 5. Choose columns, filter rows, and sort

Add this query in a new Python cell:

```python
large_parks = mo.sql(f"""
    SELECT name, district, area_ha
    FROM parks
    WHERE area_ha >= 1.0
    ORDER BY area_ha DESC, name;
""")
```

`SELECT` now names the columns to show. `WHERE` keeps rows meeting a condition. `ORDER BY` sorts the result. `DESC` means descending, so the largest area comes first. `name` breaks ties alphabetically.

Expected result:

| name | district | area_ha |
| --- | --- | --- |
| South Meadow | South | 3.0 |
| River Park | North | 2.0 |
| School Garden | South | 1.5 |
| Hill Garden | North | 1.2 |

Try changing `>= 1.0` to `>= 2.0` in the same cell. Predict which rows remain, run it, then restore `>= 1.0`.

The [SELECT reference](https://duckdb.org/docs/current/sql/query_syntax/select) explains expressions and result columns. Filtering changes the query result; it does not edit the CSV.

## 6. Combine conditions

Create another Python cell:

```python
public_parks = mo.sql(f"""
    SELECT name, area_ha
    FROM parks
    WHERE public_access = true AND area_ha >= 1.0
    ORDER BY area_ha DESC;
""")
```

`AND` requires both conditions to be true. Expect South Meadow at `3.0` hectares and River Park at `2.0` hectares.

> [!IMPORTANT]
> SQL uses `=` for equality comparisons. Python uses `==`. SQL text values such as `'North'` need quotes; Boolean values such as `true` do not.

Before running a more complex filter, compare it with the source rows. Hill Garden is large enough, but its access value is `false`, so it is excluded.

## 7. Summarize by district

Create another Python cell:

```python
district_summary = mo.sql(f"""
    SELECT
        district,
        COUNT(*) AS park_count,
        ROUND(SUM(area_ha), 2) AS total_area_ha,
        ROUND(AVG(area_ha), 2) AS mean_area_ha
    FROM parks
    GROUP BY district
    ORDER BY district;
""")
```

An **aggregate** combines several values into a summary. `COUNT(*)` counts rows, `SUM` adds areas, and `AVG` calculates the arithmetic mean. `GROUP BY district` makes one summary per district. `AS` gives a result column a name, and `ROUND(..., 2)` limits the displayed number to two decimal places.

Expected result:

| district | park_count | total_area_ha | mean_area_ha |
| --- | --- | --- | --- |
| North | 3 | 3.7 | 1.23 |
| South | 3 | 5.3 | 1.77 |

Check the first total by hand: `0.5 + 1.2 + 2.0 = 3.7`. Both districts have three records, so a count alone hides their difference in total area. These are totals for all listed parks, including those marked without public access. See [DuckDB's aggregate functions](https://duckdb.org/docs/current/sql/functions/aggregates).

> [!WARNING]
> Missing data is not zero. SQL represents missing values as `NULL`; test for them with `IS NULL`. `AVG(area_ha)` ignores missing areas, while `COUNT(*)` still counts their rows. Check completeness before interpreting an average.

## 8. Make the filter interactive

In a new **Python cell**, add:

```python
min_area = mo.ui.slider(
    start=0.0,
    stop=3.0,
    step=0.5,
    value=1.0,
    label="Minimum park area in hectares",
)
min_area
```

In a new **Python cell**:

```python
selected_parks = mo.sql(f"""
    SELECT name, area_ha
    FROM parks
    WHERE area_ha >= {min_area.value}
    ORDER BY area_ha DESC, name;
""")
```

marimo inserts the slider's numeric value where the braces appear and reruns the dependent query. At `1.0`, expect four parks; at `2.5`, expect only South Meadow. The braces are marimo's Python integration, not ordinary SQL syntax.

Use this pattern for this bounded numeric input. For queries accepting arbitrary text from users, use the database client's bound query parameters instead of building SQL by inserting text.

## 9. Save and reproduce the local analysis

Save `practice/duckdb_parks.py`, use **marimo: Restart notebook kernel**, and rerun its cells in VS Code. The notebook reconstructs its results by reading the CSV and running its cells.

> [!NOTE]
> Saving a notebook does not copy its input files into it. Keep `practice/data/parks.csv` with the notebook and preserve the relative path. If you change the CSV while marimo is open, rerun its reading cell; external file edits do not necessarily trigger reactive updates.

The named SQL results used here are query outputs in memory. We have not created a persistent `.duckdb` database file. Saving the notebook saves the instructions to reproduce the results.

## 10. Read remote Parquet files from Overture

CSV is a text format. **Parquet** stores typed columns in a binary format designed for data analysis. **GeoParquet** adds information describing geometry columns. DuckDB can query remote Parquet files without first saving the complete dataset to your laptop.

Selecting a few columns and filtering a small area can reduce the data read. This is often called **projection and filter pushdown**. DuckDB still needs file metadata and matching data blocks. `LIMIT 20` limits the returned rows, not the amount of network traffic. See [DuckDB's Parquet guide](https://duckdb.org/docs/current/data/parquet/overview) and [remote-file documentation](https://duckdb.org/docs/current/core_extensions/httpfs/overview).

### Prepare a separate notebook

Create `practice/overture_buildings.py` through the VS Code marimo command. Select the course `.venv` and add this Python cell:

```python
import marimo as mo
import duckdb
```

In a second Python cell, prepare the connection:

```python
remote_conn = duckdb.connect()
remote_conn.execute("INSTALL httpfs")
remote_conn.execute("LOAD httpfs")
remote_conn.execute("SET s3_region = 'us-west-2'")
```

`httpfs` gives DuckDB access to HTTP and Amazon S3, the storage service hosting this public data. The first install needs an internet connection; `LOAD` makes the extension available to this connection. No AWS account or key is needed for this public bucket. We pass `remote_conn` to each query so it uses the connection we prepared.

### Select a release and an area

Add a Python cell:

```python
overture_release = "2026-08-19.0"
overture_path = (
    "https://overturemaps-us-west-2.s3.us-west-2.amazonaws.com/"
    f"release/{overture_release}/theme=buildings/type=building/"
    "part-00206-f3991e83-a1e1-520f-b6b1-be1e59982002-c000.zstd.parquet"
)
```

This is one remote GeoParquet file from the selected release. Its [catalog entry](https://stac.overturemaps.org/2026-08-19.0/buildings/building/00206/00206.json) gives its coverage and download URL. The coverage includes Graz, so it is useful for this first query. A file is only part of a release; do not assume an arbitrary file contains every feature in an area.

Available releases and storage paths are listed in the [Overture catalog](https://docs.overturemaps.org/getting-data/cloud-sources/). We keep both the release and the file URL fixed for this example.

We will inspect a small rectangle in central Graz:

| Boundary | Coordinate in degrees |
| --- | --- |
| West | Longitude `15.435` |
| East | Longitude `15.445` |
| South | Latitude `47.070` |
| North | Latitude `47.076` |

A **bounding box** is a rectangle described by minimum and maximum coordinates. Here `x` means longitude and `y` means latitude in WGS 84. These coordinates are degrees, not metres.

### Check remote access first

Add a Python cell:

```python
remote_sample = mo.sql(f"""
    SELECT id, height
    FROM read_parquet('{overture_path}')
    LIMIT 3;
""", engine=remote_conn)
```

Expect three records from that file. This checks that the connection and Parquet reading work before adding a spatial filter. The sample is not restricted to Graz yet.

### Query buildings around Graz

Add a Python cell and run it once:

```python
graz_buildings = mo.sql(f"""
    SELECT id, names.primary AS name, height, bbox
    FROM read_parquet('{overture_path}', hive_partitioning = true)
    WHERE bbox.xmin <= 15.445 AND bbox.xmax >= 15.435
      AND bbox.ymin <= 47.076 AND bbox.ymax >= 47.070
    LIMIT 20;
""", engine=remote_conn)
```

`hive_partitioning` lets DuckDB interpret folder names such as `theme=buildings`. `names.primary` accesses the main name inside a nested field. `bbox` contains each building's bounding coordinates.

The four conditions select bounding boxes that overlap our rectangle. Testing only `xmin` and `ymin` would miss buildings crossing a boundary. Bounding-box overlap is a candidate filter; it is not an exact test of whether a building footprint intersects the rectangle.

Expect at most 20 rows with IDs and bounding boxes. Names and heights can be missing. Height is in metres when supplied. The query has no ordering, so do not expect the same first rows every time. This small preview is not a count of all buildings in Graz. See the [building schema](https://docs.overturemaps.org/schema/reference/buildings/building/) and [Overture's DuckDB examples](https://docs.overturemaps.org/getting-data/duckdb/).

> [!WARNING]
> Remote queries can still read substantial data. Keep the bounding-box filter and selected columns, and run the query manually. Avoid putting a remote query behind a slider that issues a new request for every movement.

This first query reads building attributes. A map also needs the `geometry` column. For geometry operations and exporting a spatial subset, follow [Overture's GeoParquet example](https://docs.overturemaps.org/getting-data/duckdb/) using DuckDB's spatial extension.

### Expand from one file to the release

For an area that may span several files, query the building partition using the path `s3://overturemaps-us-west-2/release/2026-08-19.0/theme=buildings/type=building/*`. The `*` wildcard selects all files in that partition.

To try this, replace the **existing** `overture_path` value with that S3 path and rerun the filtered query. Keep all four bounding-box conditions. This is the general pattern used in [Overture's DuckDB guide](https://docs.overturemaps.org/getting-data/duckdb/).

> [!NOTE]
> The wildcard query may take several minutes because it must inspect metadata across the release. `LIMIT` does not remove that work. For this introductory exercise, keep the single-file URL above. For larger analyses, use the catalog to identify relevant files before querying them.

### Find the current release when needed

In a separate Python cell, you can inspect the small public catalog:

```python
release_catalog = mo.sql("""
    SELECT latest
    FROM read_json_auto('https://stac.overturemaps.org/catalog.json');
""", engine=remote_conn)
```

Read its `latest` value when you want to compare a new release. For a single-file query, obtain a matching file URL from that release's catalog too; changing the date alone does not update the file identifier. For a partition query, change the release segment in the wildcard path. Keeping the release explicit makes it easier to explain differences between two runs. The [Overture quickstart](https://docs.overturemaps.org/getting-data/#get-the-latest-release) describes this catalog.

Record the release, rectangle, selected columns, and query in your notebook. If you later export a subset, keep that file and check [Overture's attribution and licensing guidance](https://docs.overturemaps.org/attribution/).

## If a query fails

| Symptom | What to check |
| --- | --- |
| No files match the CSV path | Check `csv_path` and the file in Explorer; save the notebook in `practice` |
| `parks` does not exist | Run the cell that assigns `parks = mo.sql(...)` and check for errors |
| Column not found | Compare the name with the CSV header, including underscores |
| SQL produces a Python syntax error | Keep the SQL inside the triple-quoted string passed to `mo.sql` |
| Comparison fails because area is text | Check decimal points and stray unit labels in the CSV |
| Several cells define the same variable | Give each query result the distinct output name specified above |
| Updated CSV values are not visible | Save the CSV and rerun the reading cell before checking downstream results |
| Remote query fails with a network error | Check internet access, the selected release, and extension installation |
| S3 reports no files or access denied | Check the public bucket path and release; do not add credentials for this public example |
| Remote query takes time | Keep the small rectangle and avoid launching duplicate queries; use the notebook interrupt control if needed |

## Documentation and a video

- [marimo SQL documentation](https://docs.marimo.io/guides/working_with_data/sql/): creating SQL cells, naming results, and querying them from other cells.
- [DuckDB CSV import](https://duckdb.org/docs/current/data/csv/overview), [SELECT](https://duckdb.org/docs/current/sql/query_syntax/select), and [aggregates](https://duckdb.org/docs/current/sql/functions/aggregates): look up the operations used here.
- [marimo's "Mix SQL with Python code, no problem!" on YouTube](https://www.youtube.com/watch?v=IHEf5HwU7R0): a demonstration of the same Python/SQL notebook workflow.
- [Overture's DuckDB guide](https://docs.overturemaps.org/getting-data/duckdb/): remote GeoParquet queries and exports.
- [Overture's beta-release blog walkthrough](https://docs.overturemaps.org/blog/2024/04/22/beta-release/): why spatial filtering matters. It uses an older release and schema; keep the current path and `bbox.xmin` field names from this lesson.

## Exercise: check a local result and a remote sample

Use new Python cells with `mo.sql` and new output names. Keep your worked examples.

1. List publicly accessible parks of at least `1.0` hectare, largest first.
2. Write a summary query returning their count and total area. Use `WHERE` to filter before aggregating.
3. Change the cutoff to `0.5`. Predict the count and total before running.
4. Add this record to the end of the CSV in VS Code, save, and rerun the reading cell:

   ```csv
   7,Canal Pocket,South,0.4,true
   ```

5. Predict whether the new row changes either filtered summary. Check the district summary too.
6. Add a Markdown cell explaining why "South has more park area" does not establish that residents of South have better access to parks. Name one additional dataset you would need.

In `practice/overture_buildings.py`, finish with a small remote-data task:

7. Change the output limit to `10`. Keep the original release and rectangle, and run the query once.
8. In a new cell, query the local `graz_buildings` result to count the returned rows and the non-missing heights. Use `COUNT(*)` and `COUNT(height)`. This queries the result already in memory, not the remote files again.
9. Explain why the second count may be smaller and why neither count describes all buildings in the rectangle. Record the release used.

You are done when the park summaries match the checks below, the remote sample has at most ten rows, and your notes explain both limits of interpretation.

<details>
<summary>Show a hint</summary>

Combine the filter from section 6 with `COUNT(*)` and `SUM(area_ha)` from section 7. Without `GROUP BY`, those aggregates summarize all rows that pass the filter. Round the total to two decimal places if needed.

</details>

<details>
<summary>Check your results</summary>

At `1.0` hectare, two accessible parks total `5.0` hectares. At `0.5`, four total `6.3` hectares. The new `0.4`-hectare park falls below both cutoffs, so neither result changes. The South district summary becomes four parks and `5.7` hectares, with a mean of `1.43` after rounding.

`COUNT(height)` excludes `NULL` heights. Its result cannot exceed `COUNT(*)`. The `LIMIT` makes these sample counts rather than totals for the rectangle.

Park area alone does not describe walking distance, entrances, opening times, or how many people need access. Population data and a walkable street network would help answer a different, more specific question about access.

</details>
