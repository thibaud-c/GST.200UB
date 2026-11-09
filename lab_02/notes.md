# Lab 02 study notes: crime data, EDA, and hotspots

[Lab overview and setup](README.md) · [Exercise file](exercise.py) · [Live demo](demo.py)

Read one chapter when you need it. These notes keep the longer explanations,
paper comparisons, worked interpretations, and optional practice from the notebook.
The section labels match `exercise.py`; references to cells and outputs mean the
cells in that notebook. Keep it open and return to the same section after reading.
For a local copy, open this file in VS Code and use **Open Preview to the Side**.

## Find a chapter

- [Overview](#overview) and [quick reference](#quick-reference).
- [A1. EDA begins with questions about the records](#a1).
- [A2. Time, denominators, and misleading summaries](#a2).
- [A3. Clean deliberately and keep future records separate](#a3).
- [A4. Geometry, distances, and a fixed study area](#a4).
- [Worked exclusion audit](#exclusion-audit).
- [A5. H3 and discrete global grids](#a5).
- [A6. DBSCAN: density-connected points](#a6).
- [Cluster attributes and empty results](#cluster-schema).
- [A7. PAI: distinguish hits from area covered](#a7).
- [Python guards and `None`](#none-guard).
- [A8. Explore with Leafmap's Kepler backend](#a8).
- [B1. Audit the extract with DuckDB](#b1).
- [Task 1. Select the analysis records in SQL](#task-1).
- [Task 2. Prepare points and account for exclusions](#task-2).
- [Inspect training geography before choosing hotspots](#training-geography).
- [Task 3. Build H3 hotspots from training points](#task-3).
- [Task 4. Turn DBSCAN clusters into hotspot polygons](#task-4).
- [Task 5. Calculate and interpret PAI](#task-5).
- [Task 6. Inspect maps and challenge your conclusion](#task-6).
- [Reflection and further learning](#reflection).

<a name="overview"></a>

## Overview

Can concentrations of **recorded incidents** in one period help locate incidents
in a later period? Before choosing an algorithm, we need to understand what the
records contain, what is missing, and what would count as a useful result.

Read [Chainey, Tompson & Uhlig (2008), *The utility of hotspot mapping for
predicting spatial patterns of crime*](https://discovery.ucl.ac.uk/id/eprint/112873/).
Look at Figure 1 and the evaluation equation. Propose a comparison in three sentences:

- What makes a place a hotspot, and how will you draw its boundary?
- Which observations should be kept out of the map-building step?
- Why might a map covering the entire city catch many incidents but tell us little?

Keep that proposal. Part A is a worked training notebook; Part B asks you to adapt
it to Chicago. Budget two practical sessions: EDA and methods first, then the
reproduction and interpretation. Finish the core tasks before trying extensions.

If there are updates, save your work and run `git pull` and `uv sync` in the course
folder in a separate terminal. Open `exercise.py` as marimo in VS Code with the course
`.venv`. See the [Git tutorial](https://github.com/thibaud-c/GST.200UB/blob/main/tutorials/04_git.md)
for help. Each function stub returns `None` until you replace its body.

### What we reproduce, change, and leave out

The paper compares administrative areas, grids, spatial ellipses, and kernel
density estimation (KDE), using earlier records to locate later incidents and
PAI to account for hotspot area. Its study used Camden and Islington, London.

Our **method reproduction** downloads all of calendar year 2025 for Chicago and
uses January–November for training and December for held-out evaluation.
We retain temporal separation and PAI to assess how well earlier hotspots locate
December's recorded incidents.
We do not reproduce the paper's data or exact numerical results.
H3 replaces its grid implementation; DBSCAN with convex hulls is our additional
cluster method, not the paper's ellipse method. We add a DuckDB data audit and
explicit EDA before modelling.

KDE is important in the paper, but is outside this core exercise.
Administrative maps, Moran's I, and Gi* are optional follow-up topics, not
prerequisites for this notebook.

<a name="quick-reference"></a>

### Quick reference

| Question | Tool | Documentation |
| --- | --- | --- |
| How many rows or missing values? | `COUNT(*)`, `COUNT(column)` | [DuckDB aggregates](https://duckdb.org/docs/stable/sql/functions/aggregates.html) |
| Can this string become a date? | `TRY_CAST(date AS TIMESTAMP)` | [DuckDB casting](https://duckdb.org/docs/stable/sql/expressions/cast.html) |
| Which records should I keep? | `WHERE`, `.loc[mask]` | [SQL filtering](https://duckdb.org/docs/stable/sql/query_syntax/where.html) |
| Where are my points? | `points_from_xy`, `.to_crs()` | [GeoPandas introduction](https://geopandas.org/en/stable/getting_started/introduction.html) |
| What is this point's grid cell? | `h3.latlng_to_cell(lat, lon, resolution)` | [H3 Python API](https://uber.github.io/h3-py/api_quick.html) |
| Which points form dense groups? | `DBSCAN(...).fit_predict(xy)` | [scikit-learn DBSCAN](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html) |
| Which future points fall in a hotspot? | `.intersects(hotspot_union)` | [GeoPandas predicates](https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoSeries.intersects.html) |
| How do I inspect the result? | Plotly, `.plot()`, `leafmap.Map` | [Visualization tutorial](https://github.com/thibaud-c/GST.200UB/blob/main/tutorials/09_visualization.md) |

## Part A. Learn the operations on small examples

<a name="a1"></a>

### A1. EDA begins with questions about the records

Use this section for [B1: the DuckDB audit](#b1-audit-the-extract-with-duckdb)
and [Task 1: selecting records](#task-1-select-the-analysis-records-in-sql).

**Exploratory data analysis (EDA)** is a cycle: ask a question, inspect a table or
plot, identify a possible explanation, and check it against the data. It is not
just making every available chart.

Start with the **unit of observation**: what does one row represent? An incident,
a victim, and an arrest are different units. A row count is not automatically a
count of people or events. Next check identifiers, dates, categories, coordinates,
and the population of records your extract actually covers.

Run this table and inspect it before reading the audit. Predict the number of
rows, distinct IDs, unusable dates, and missing latitudes.

The next cells are **SQL cells**: edit the SQL in marimo, give each output a unique
name, and run it. DuckDB works inside the notebook; no server or connection object
is needed. In the saved `.py` file, marimo represents each SQL cell with `mo.sql`.
The [DuckDB tutorial](https://github.com/thibaud-c/GST.200UB/blob/main/tutorials/07_duckdb.md)
explains that wrapper and the SQL editor.

`COUNT(column)` skips missing values. `TRY_CAST` returns `NULL` when conversion
fails, allowing us to count errors before deciding what to exclude.

Expect 8 rows, 7 distinct IDs, 1 unusable date, and 1 missing latitude. Notice that
999 was not counted as missing. **Present does not mean valid.** A duplicate ID
needs investigation; two different IDs at the same coordinates may be legitimate
separate incidents at a block-level location.

A useful audit records counts **before and after** every exclusion. Missingness
can vary by category or period, changing which incidents your map represents.

Try: calculate the missing-latitude percentage for each category. The denominator
is the number of rows in that category, not the whole table. What would change if
you removed missing coordinates before making this summary?

<a name="a2"></a>

### A2. Time, denominators, and misleading summaries

Use the calendar example for [B1: daily training counts](#b1-audit-the-extract-with-duckdb)
and the denominator discussion for [Task 6: interpreting maps](#task-6-inspect-maps-and-challenge-your-conclusion).

The query below counts distinct incidents before 3 January. Then it joins those
counts onto a calendar. Without the calendar, days with zero records disappear.
Do not assume a missing day means zero until you have checked the extract's coverage.

Expect 2 incidents on 1 January and 0 on 2 January. Hover over the bars. Explain
why counting rows would have changed the first bar.

Use a **count** for volume, a **density** for count per area, and a **rate** for
count per relevant exposure. Twenty incidents in 1 km² and twenty in 10 km² have
equal counts but different densities. Neither tells us an individual's risk:
residents, visitors, shops, vehicles, and time spent there are different possible
exposure denominators.

For weekday comparisons, divide by how many Mondays, Tuesdays, etc. occur in the
observed window. For month comparisons, check days of coverage. Eleven months
from one year cannot establish a repeating annual seasonal pattern. An event timestamp may be an estimate
of when something happened; it is not automatically the report timestamp.

**Practice:** one period has 40 records over 20 observed days; another has 45 over
30 days. Which has the higher count? Which has the higher daily average? Expect
45 versus 40 for counts, but 1.5 versus 2.0 records per day.

<a name="a3"></a>

### A3. Clean deliberately and keep future records separate

Use this section for [Task 1: date selection](#task-1-select-the-analysis-records-in-sql),
[Task 2: record exclusions](#task-2-prepare-points-and-account-for-exclusions),
and [the training-geography inspection](#inspect-training-geography-before-choosing-hotspots).

Here is a small cleaning example. Read each condition before running it. We keep
one copy of an ID only after confirming that the duplicate represents the same
record. In a real extract, conflicting duplicates need investigation.

Expect 4 clean records: training IDs 1, 2, 6 and test ID 7. The cutoff belongs to
the test period. Use explicit start-inclusive, end-exclusive windows, rather than
“the last seven days” relative to whichever row happens to be newest.

**Leakage** means using information that would not have been available when a
prediction was made. Fitting DBSCAN to test points, choosing a grid after looking
at test hotspots, or selecting parameters that maximise the test PAI leaks information.
Use January–October for fitting and November for validation if you want to choose
parameters. Then refit on January–November and evaluate once on December.

Explore training patterns first. Mechanical checks of the test file's coverage and
format are allowed; its spatial concentrations must not guide model choices.

<a name="a4"></a>

### A4. Geometry, distances, and a fixed study area

Use this section for [Task 2: preparing points](#task-2-prepare-points-and-account-for-exclusions)
and [Task 5: measuring hotspot coverage](#task-5-calculate-and-interpret-pai).

GeoPandas attaches geometry and a CRS to a table. A4 separates two operations:

1. Create the GeoDataFrames. `points_from_xy` takes longitude first, then latitude.
   `crs=4326` describes those values as WGS84 coordinates in degrees. It labels
   the existing coordinates; it does not transform them. Inspect the points table
   and its `.crs` before continuing.
2. Estimate and apply a local projection. `estimate_utm_crs()` uses the dataset's
   bounds to suggest a UTM CRS. It returns a CRS object, not new geometry. Pass
   that result to `to_crs()` for both the points and boundary. Chicago's estimate
   is UTM zone 16N, **EPSG:32616**, whose coordinates use metres. Areas then use
   square metres.

Compare coordinate values before and after projection. The places are the same,
but their geometry coordinates and units change. `to_crs()` leaves the original
longitude/latitude attribute columns unchanged. Compare `.geometry.x` and
`.geometry.y` in the two GeoDataFrames to inspect the transformed values.
UTM is suitable for this local example;
an estimated UTM zone is not a universal projection for global data.
See [GeoPandas' CRS estimation](https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoDataFrame.estimate_utm_crs.html)
and [coordinate transformations](https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoDataFrame.to_crs.html).

The seven-point example uses a fixed rectangular study boundary. Keep it fixed
when comparing methods; changing it changes PAI's denominator. Part B applies
the same estimation and projection steps to Chicago's published boundary,
rather than using the convex hull of observed incidents.

Before modelling, inspect coordinate ranges, repeated locations, and points outside
the study area. Drop duplicate **IDs**, not duplicate coordinates. Use
`points.intersects(boundary.geometry.union_all())` to include points on the boundary.
Compare excluded records with retained ones; a valid coordinate can still lie in
the wrong city.

If `to_crs` fails because PROJ data are missing, or plotting reports missing font
files, follow the [Windows package repair steps](README.md#windows-known-issue-package-repair).
Close Python sessions before reinstalling the affected packages.

<a name="exclusion-audit"></a>

#### Worked exclusion audit

The notebook's A4 table starts with eight supplied filtering outcomes. Each row
belongs to one period and has one outcome. `pd.crosstab` counts combinations of
period and outcome. Both periods start with four rows; training retains two,
while test retains one. Their exclusion percentages are 50% and 75%.

For Task 2, work from the selected 2025 records, whose dates have already been checked:

- Label January–November as training and December as test before spatial exclusions.
- Assign each excluded row its first reason: missing/invalid coordinates,
  duplicate ID after coordinate checks, or outside the boundary after projection.
- Count retained rows and each exclusion reason by period. Their sum must equal
  the input row count in that period. Divide excluded rows by that input count.
- Keep this audit separate from the function's return value, which remains a
  GeoDataFrame. You may print the audit inside the function or build it in a separate cell.

Do not count a missing-coordinate row again as outside the boundary. A valid
location outside Chicago is also different from a missing location. Compare the
periods before interpreting a change in mapped counts.

<a name="a5"></a>

### A5. H3 and discrete global grids

Use this section for [the training count histogram](#inspect-training-geography-before-choosing-hotspots)
and [Task 3: H3 hotspots](#task-3-build-h3-hotspots-from-training-points).

A **discrete global grid system (DGGS)** divides the Earth's surface into indexed
cells. An index lets us group observations without inventing a new local grid for
every city. H3 uses mostly hexagons; S2 is another system and uses quadrilateral
cells. A grid index is not a replacement for a CRS or a measure of risk.

H3 resolutions run from 0 to 15; higher values give smaller cells. Most cells have
six neighbours, but there are twelve pentagons at every resolution. Cell areas
vary, even at one resolution. H3's parent-child indexing is exact logically, but
child boundaries do not exactly nest inside parent boundaries geographically.

A grid avoids dependence on police district boundaries, but it is not neutral:
resolution and boundaries still change the pattern (**MAUP**, the modifiable areal
unit problem). Fine cells can reveal detail or amplify imprecise coordinates.
See [H3's introduction](https://h3geo.org/docs/),
[cell sizes](https://h3geo.org/docs/core-library/restable/), and
[hierarchy](https://h3geo.org/docs/highlights/indexing/).

Notice the order: **H3 takes latitude, longitude**. To turn a cell back into a
Shapely polygon, swap the boundary pairs to longitude, latitude.

For mapping counts, build the grid over the **whole study area**, including cells
with zero incidents. A map of occupied cells alone hides zeros and changes any
“top percentage of cells” threshold. This provided function uses H3's experimental
**overlap** option to include boundary-crossing cells, then clips them. The default
centre-based polygon fill can miss edge cells.

Compare the mean, median, and maximum count. A few high values can pull the
mean above the typical cell. The histogram shows how many cells have each count;
it does not show where those cells are. Use the map for that question.

Change the resolution once and predict whether the number of occupied cells will
increase. Compare counts with densities, especially in clipped edge cells. Tiny
slivers can get very high density from a single point: inspect their areas.

To select hotspots we use a **study-area budget**, not a percentage of cells. Rank
cells by training density, breaking ties by H3 ID; keep the leading cells whose
cumulative area fits the budget. The actual area may be below the target because
we keep whole clipped cells. This simple prefix rule can leave spare budget.

If no cell fits a small budget, an empty selection is an honest result. Do not
silently add a larger cell or change the budget after looking at test performance.

<a name="a6"></a>

### A6. DBSCAN: density-connected points

Use this section for [Task 4: DBSCAN hotspot polygons](#task-4-turn-dbscan-clusters-into-hotspot-polygons).

DBSCAN builds clusters from dense neighbourhoods. `eps` is a neighbour distance,
not a maximum cluster diameter. `min_samples` counts the point itself. A core point
has enough neighbours; connected core points and nearby border points form a
cluster. Other points receive label **-1**, meaning noise under these settings,
not an error or an unimportant incident.

Advantages: no preset number of clusters; irregular groups are possible.
Limitations: one density threshold may fit some neighbourhoods poorly; block-level
geocoding can manufacture repeated locations; large neighbourhoods can consume
substantial memory. Use the complete filtered training set for this lab. Sampling
changes density and is not a free speed-up for the same model.

At 50 m expect two three-point clusters and one noise point. The integer labels
are arbitrary names, not ranks. Predict what happens at 10 m and 900 m, then
try both and restore 50 m. At 10 m all points are noise; at 900 m they form one cluster. See [DBSCAN's worked example](https://scikit-learn.org/stable/auto_examples/cluster/plot_dbscan.html).

A set of point labels has no area for PAI. Here we use a **convex hull**, the
smallest convex polygon enclosing a cluster, like an elastic band around pins.
It can bridge empty space and overstate an irregular cluster's footprint. Clusters
on one location or a straight line have zero hull area; we exclude and report them.
This footprint choice is part of our method, not an output automatically supplied
by DBSCAN.

<a name="cluster-schema"></a>

#### Cluster attributes and empty results

The A6 worked cell collects one dictionary per usable hull. `cluster_id` is the
DBSCAN label, `n_points` counts the cluster's original incident points, and
`geometry` contains its convex hull. The explicit column list keeps the same
result schema even when the list of dictionaries is empty.

An empty result still needs an active geometry column and the input CRS:

```python
empty_hotspots = gpd.GeoDataFrame(
    columns=["cluster_id", "n_points", "geometry"],
    geometry="geometry", crs=demo_points.crs,
)
```

Inspect `.empty`, `.columns`, and `.crs`. Set the A6 distance slider to 10 m to
produce an empty result through clustering, then restore 50 m. Returning `None`
would prevent later cells from using `.geometry` or `.to_crs()`. An empty
GeoDataFrame can continue through those operations; its zero hotspot area makes
PAI undefined. Report noise and zero-area clusters separately, without inventing
a buffer to make their area positive.

<a name="a7"></a>

### A7. PAI: distinguish hits from area covered

Use this section for [Task 5: calculating PAI](#task-5-calculate-and-interpret-pai)
and [Task 6: comparing the conclusions](#task-6-inspect-maps-and-challenge-your-conclusion).

For a fixed test period and study boundary:

**PAI = (hits / test incidents) / (hotspot area / study area).**

Catching 20 of 100 future incidents in 10% of the study area gives PAI = 2.
That is twice the concentration implied by uniform distribution over area.
It is not “200% accuracy,” a significance test, or evidence that an intervention
would prevent incidents. PAI = 1 matches the uniform-area benchmark; it does not
establish that an observed pattern is random.

Always show **hits, total test records, hit rate, hotspot area, area fraction, and
PAI** together. A tiny footprint with very few hits can have a high PAI. Different
area budgets can change the ranking. Empty hotspots or an empty test set make
PAI undefined, not zero.

For geometry, first **union** overlapping hotspot polygons and **clip** the result
to the study boundary. Sum its area once. Test each unique incident against that
union with `intersects`; we explicitly include boundary points. A spatial join
against separate overlapping polygons could count an incident more than once.

Expect 2 hits among 3 points at the default settings. Boundary inclusion matters
here: the points on the hull vertices count. These points teach the geometry
operation; the Chicago evaluation will use genuinely later records.

**Practice:** a second map catches 40 of 100 records in 25% of the area. Calculate
its PAI (1.6). Which map catches more? Which has greater concentration? Explain why
neither number alone answers which map is preferable.

<a name="none-guard"></a>

#### Python guards and `None`

A guard handles an exceptional input before the calculation. In A7's small
`_safe_share` example, a zero denominator returns `None` before division.
`return` exits the function immediately. With a positive denominator, zero in
the numerator gives a valid zero instead.

`None` is Python's missing-result value; it is different from the string
`"None"` and the number `0`. Use `result is None` when testing it. Task 5 needs
to guard all three undefined inputs specified in its checklist before applying
the PAI formula. See [Python's return statement](https://docs.python.org/3/reference/simple_stmts.html#the-return-statement).

<a name="a8"></a>

### A8. Explore with Leafmap's Kepler backend

Use this section for [Task 6: the Chicago hotspot map](#task-6-inspect-maps-and-challenge-your-conclusion).

The map opens at the example's location. Keep calculations in the metric CRS and
send longitude/latitude to the web map. Use hover, layer toggles, and filters to
inspect the data; colours alone do not establish a statistically significant hotspot.

The display copy omits `h3_id` so Kepler uses our clipped polygons rather than
automatically drawing complete H3 cells from their IDs. The original grid keeps
its IDs for analysis. In Kepler, style the grid by `count`, reduce its opacity,
and keep points on top.
Inspect an empty cell and a convex hull. Plotly is convenient for interactive EDA
charts; Matplotlib gives quick static checks; Leafmap provides layered maps with
several possible backends. Large point layers can overwhelm a browser, so display
aggregates when possible. See the [Leafmap walkthrough](https://leafmap.org/notebooks/26_kepler_gl/).

**Display note:** the current Kepler widget can render a short map or unstyled
controls in marimo’s browser editor. Leafmap still uses that renderer. If this
happens, use the Matplotlib maps to inspect geometry and tell the instructor
which editor and package versions you used.

**Before moving on:** explain one missing-data decision, the order of H3's
coordinates, the difference between `eps` and hull area, and why we need future
records. You can return to any example while completing Part B.

## Part B. Reproduce the evaluation idea with Chicago data

Can a hotspot map built from earlier records locate incidents recorded later?
This part connects data quality, spatial methods, and an honest evaluation.
Use it as a reference while working through the [exercise](exercise.py).
The [README](README.md#part-b-data-and-workflow) lists the two local files and setup steps.

<a name="b1"></a>

### B1. Audit the extract with DuckDB

#### Understand what a row represents

The [Chicago source](https://data.cityofchicago.org/d/ijzp-q8t2) contains
police-recorded reports. Reporting, recording, and enforcement affect which
incidents enter the table. A location with more records may have more activity,
more reporting, or both. Without an exposure denominator such as residents,
visitors, or businesses, a count is not an individual risk estimate.

Read the source's category definitions. Its murder records are per victim,
whereas other categories describe reported incidents. The core exercise selects
BURGLARY, which is not necessarily the paper's residential-burglary category.
Locations are approximate, and records can be revised. Keep your saved files
fixed, record their download date, and respect the source's restriction on
recovering exact addresses.

#### Read the file before building geometry

DuckDB can scan the CSV and return a short summary. This avoids creating a
citywide GeoDataFrame before knowing which records you need. CSV queries still
scan data; a small result does not imply a small amount of reading. Parquet can
offer more opportunities to skip columns or data blocks.

The notebook uses `read_csv(..., normalize_names=true)`. DuckDB detects column
types and converts headers such as `Primary Type` to `primary_type` for queries.
The original CSV stays unchanged. Start with the `DESCRIBE` result to see the
names and types DuckDB found. `TRY_CAST(value AS type)` attempts a conversion
and returns SQL `NULL` when conversion is impossible.

Read the two audits as different questions:

| Output | Period | What to learn |
| --- | --- | --- |
| `source_audit` | All of 2025 | Does the file cover the year? Are IDs unique? Are dates usable? How many annual burglaries are present? |
| `category_audit` | January–November | Which recorded categories dominate training data? Where are coordinates missing? |

`COUNT(*)` counts rows; `COUNT(column)` skips nulls; `COUNT(DISTINCT id)` counts
different IDs. Equal row and distinct-ID counts suggest one row per ID. They
do not establish completeness or accurate geocoding. The year-start and
year-end checks likewise test date coverage, not whether every report is present.
If a check fails, inspect the export and its filters before deleting rows to make it pass.

Compare missing-coordinate counts with percentages. A large category can have
the most missing locations but a smaller missing percentage. Excluding those
rows changes the mapped sample. The source audit counts missing or unreadable
coordinates; Task 2 also checks coordinate ranges and the city boundary.

#### Explore time without seeing the test pattern

The training calendar has 334 days. A daily query should retain days with zero
recorded burglaries, using the calendar join from [A2](#a2). Otherwise gaps
disappear from the plot and averages can be misleading. Keep the output columns
`day` and `incidents`. Their total should match the BURGLARY row of
`category_audit`, because both describe the same period before spatial exclusions.

Describe what the plot shows before proposing why it occurs. For example,
a reporting delay and a change in incident frequency need different evidence.
See [A1](#a1) for missing-value queries and [A2](#a2) for denominators.

[Open B1 in the exercise](exercise.py#L748).

<a name="task-1"></a>

### Task 1. Select the analysis records in SQL

The SQL task produces a small, typed table for spatial analysis. Its output,
`selected_records`, contains an incident ID, occurrence timestamp, category,
latitude, and longitude. Use aliases to name the timestamp `occurred_at`.

The selection covers all 2025 burglaries. Keeping December here is deliberate:
we still need its records for evaluation. The split comes after spatial cleaning.
A half-open interval includes its start and excludes its end, so
`2025-01-01 <= occurred_at < 2026-01-01` includes 31 December without
depending on a particular time of day.

Keep missing coordinates at this stage. Dropping them in SQL would hide part of
the exclusion audit. Do not use `LIMIT`, because the first rows are not a
representative spatial or temporal sample. The check compares your result with
the annual BURGLARY count in `source_audit`, not the January–November count.

| SQL tool | Role in this task |
| --- | --- |
| `SELECT ... AS ...` | Choose columns and name the outputs. |
| `TRY_CAST(... AS TIMESTAMP)` | Convert dates to timestamps; failed conversions become nulls. |
| `WHERE` with `AND` | Apply the category and date conditions together. |
| `ORDER BY id` | Make row order predictable. It does not remove duplicates. |

Every SQL cell needs a unique output name. Edit the existing `selected_records`
cell instead of creating another cell with that name.
Review [A1](#a1) and [A3](#a3), or the [SQL tutorial](../tutorials/07_duckdb.md).

[Open Task 1 in the exercise](exercise.py#L858).

<a name="task-2"></a>

### Task 2. Prepare points and account for exclusions

A GeoDataFrame combines ordinary attributes with geometry and a coordinate
reference system. Here the input is the SQL table and the output is a point
GeoDataFrame in the city boundary's projected CRS. The function returns that
GeoDataFrame only. Build the exclusion audit in the separate workspace.

Longitude is x and latitude is y for `points_from_xy`. Declare the input as
EPSG:4326, then use `.to_crs(boundary.crs)` to transform it. Declaring a CRS
describes existing coordinates; transforming a CRS changes their coordinates.
Distances and areas in longitude/latitude degrees are unsuitable for our metre
and square-metre calculations.

Missing values and impossible ranges should be excluded before geometry
creation. A coordinate inside the global ranges can still be wrong for Chicago,
so the city-boundary test is a separate step. `intersects` includes points on
the boundary, while `within` excludes points exactly on its edge. We use
`intersects` consistently in this exercise.

Deduplicate by incident ID, not by coordinates. Several distinct reports can
share a location, particularly when locations are approximate. Work on copies
so the original rows remain available for comparison.

Keep the city footprint fixed for every method. It has no population or
land-use mask. Changing that footprint would change the study-area denominator
in PAI, even if the hotspot polygons stayed the same.

#### Make exclusions add up

Assign the period from each original row's `occurred_at` before filtering.
Record one outcome per row, in a stated order: missing/invalid coordinates,
duplicate ID among remaining rows, outside the boundary, or retained. Once a
row receives an exclusion reason, do not count it again under another reason.

Present one row per period:

| Period | Input | Missing/invalid coordinates | Duplicate IDs | Outside boundary | Retained |
| --- | --- | --- | --- | --- | --- |
| January–November | Your count | Your count | Your count | Your count | Your count |
| December | Your count | Your count | Your count | Your count | Your count |

For each period, input must equal retained plus all exclusions. Also compare
the retained fraction, not just the number dropped. An unequal fraction means
the model and evaluation may describe differently selected samples. The small
probe in Task 2 checks your function; it does not replace this audit of the
actual records. Use the [worked exclusion audit](#exclusion-audit) for the table pattern.

Review [A3](#a3) for cleaning and [A4](#a4) for geometry and projection.

[Open Task 2 in the exercise](exercise.py#L931).

<a name="training-geography"></a>

### Inspect training geography before choosing hotspots

The notebook splits the retained points at 1 December:

| Role | Included dates | Permitted use |
| --- | --- | --- |
| `train` | 1 January through 30 November 2025 | Explore spatial patterns and build the hotspot maps. |
| `test` | 1 through 31 December 2025 | Evaluate the maps after their settings are fixed. |

Map `train` with the city outline before clustering. Look for points outside
the expected extent and repeated locations. Later, inspect the full H3 count
histogram, including zero cells. A few high counts can pull the mean far above
the median. A zero means no retained training reports of this category in that
cell, not proof of safety.

Use the course settings first: H3 resolution 8 with a 10% city-area budget;
DBSCAN `eps=500` metres and `min_samples=10`. These settings make a reproducible
comparison, not a claim that they are optimal. Choosing settings after viewing
December PAI would use the test data twice and favour a lucky result.
For an extension, fit on January–October and compare settings on November,
then fix the choice, refit on January–November, and evaluate December once.
See [A3](#a3) and [A5](#a5).

<a name="task-3"></a>

### Task 3. Build H3 hotspots from training points

H3 gives every location a cell ID at a chosen resolution. The same resolution
and coordinate order must be used for assigning incidents and building the
grid. `h3.latlng_to_cell` takes latitude first. Shapely point coordinates use
x then y, so a geographic point supplies `point.y` then `point.x`.

`chicago_grid` contains city-intersecting resolution-8 cells, clipped to the
city. Map training counts onto a copy of this full grid and fill absent counts
with zero. Starting only from occupied cells would hide the zero-count areas.
Counts per cell can differ from density because clipping produces unequal
cell areas at the city edge. Density here is count divided by the cell's
clipped metric area. Small fragments can have high densities from few incidents;
inspect them on the map.

The budget passed to `h3_hotspots` is in square metres. The calling cell
calculates 10% of the city area. Sort by density descending, then H3 ID
ascending to settle ties reproducibly. The task keeps a prefix of that ranking:

| Ranked cell | Area in km² | Cumulative area in km² | Keep with a 6 km² budget? |
| --- | --- | --- | --- |
| First | 2 | 2 | Yes |
| Second | 3 | 5 | Yes |
| Third | 4 | 9 | No |

Do not skip an oversized ranked cell to fit lower-ranked cells later. Whole
cells can leave part of the budget unused. This is why selecting a percentage
of cells or a count quantile would answer a different question. A zero budget
returns an empty GeoDataFrame with the same required columns and CRS.

Inspect the selected counts and one boundary fragment before trusting the
result. Review [A5](#a5) for loops, count mapping, ranking, and cumulative area.

[Open Task 3 in the exercise](exercise.py#L1057).

<a name="task-4"></a>

### Task 4. Turn DBSCAN clusters into hotspot polygons

DBSCAN groups nearby points through density connectivity. `eps_m` is the
maximum neighbour distance in metres. `min_samples` is the number of nearby
points required for a core point, including the point itself. Chains of core
points can connect a cluster across a much larger distance than `eps_m`.

Use projected x/y values from `train`. Geographic degrees would make a 500-unit
neighbour distance meaningless for this task. Attach the fitted labels to a
copy of the points. Label `-1` means noise under these settings, not a location
without crime or a point that can be removed from evaluation.

A cluster is initially a group of points, not an area. The task converts each
non-noise cluster to a convex hull, the smallest convex polygon enclosing its
points. A hull can span unoccupied space, rivers, or gaps. Clipping it to the
city later does not remove all those limitations. This is also a methodological
change from the paper's spatial ellipses.

The result has one row per positive-area hull, with `cluster_id`, `n_points`,
and `geometry`. Count source points before building the hull; counting hull
vertices would lose interior and repeated-location incidents. Print the noise
count and the number of discarded zero-area hulls. Collinear or coincident
points can produce a line or point rather than a polygon. Do not buffer those
results just to create a denominator for PAI.

If no usable hull remains, return an empty spatial table with those columns
and `points.crs`. An empty result is meaningful; losing its schema would cause
the later comparison to fail. The [A6 schema example](#cluster-schema) shows the
pattern. The Task 4 check uses A6's seven points before applying your function
to Chicago. Cluster numbers may differ; membership and sizes matter.
Review [A6](#a6) and the [DBSCAN worked example](https://scikit-learn.org/stable/auto_examples/cluster/plot_dbscan.html).

[Open Task 4 in the exercise](exercise.py#L1121).

<a name="task-5"></a>

### Task 5. Calculate and interpret PAI

The prediction accuracy index compares the fraction of test incidents captured
with the fraction of study area covered:

$$
\mathrm{PAI} = \frac{\mathrm{hits}/\mathrm{total}}{\mathrm{hotspot\ area}/\mathrm{study\ area}}.
$$

Capturing 25% of December records in 10% of the city gives PAI 2.5. It means
recorded test incidents are concentrated within the selected area relative to
the citywide average. It does not mean the model is 250% accurate or estimates
an individual's risk. A whole-city map has PAI 1 and captures every retained
test incident, while providing no spatial focus.

`compute_pai` receives counts and areas. Areas must use the same units. Return
`None` before dividing when the test count, hotspot area, or study area is zero.
With positive denominators, zero hits gives a valid PAI of zero. Python `None`
means no defined result; it is different from `0` or the string `"None"`.
See the [A7 guard example](#none-guard) for early returns.

#### Read the supplied evaluation cell

Both methods use the same December points, fixed city boundary, and spatial
predicate. The code unions hotspot polygons before intersecting them with the
city. That measures overlapping areas once. A point intersecting the union is
one hit even if it touches several original polygons. Boundary points are
included, consistently with Task 2.

Read the resulting columns together:

| Column | Meaning |
| --- | --- |
| `hits` / `test_records` | Captured and total retained December burglaries. |
| `hit_rate` | Fraction of those December records captured. |
| `hotspot_km2` / `area_fraction` | How much of the fixed city footprint is selected. |
| `PAI` | Hit fraction divided by area fraction, or undefined for a zero denominator. |

H3 has an area budget; DBSCAN's area emerges from its clusters and settings.
A higher PAI alone cannot settle which map is preferable. A small map might
capture few incidents at high concentration. Compare its hit rate and area
with the other map, and state the trade-off. Empty hotspots produce zero hits
and undefined PAI, not an infinite score. Review [A7](#a7) for the hand calculation.

[Open Task 5 in the exercise](exercise.py#L1183).

<a name="task-6"></a>

### Task 6. Inspect maps and challenge your conclusion

Use Leafmap's Kepler backend to inspect the city outline and non-empty hotspot
layers. Transform display copies to EPSG:4326; keep projected analysis layers
for measuring areas. Remove `h3_id` from the H3 display copy so Kepler uses the
clipped polygon geometry rather than reconstructing a whole H3 cell from its ID.

Add December points only after fixing the hotspot maps. Look for missed
incidents and hulls spanning empty space. Compare one place captured by only
one method with a place captured by both. Use distinct layer names, readable
colours and transparency, and show the category, dates, and City of Chicago
source. An empty hotspot layer should be reported and omitted from the map.

Task 6 has a visual check rather than a single correct map. Do the layers line
up with Chicago? Are H3 boundary cells clipped? Can you tell the two methods
apart and inspect their records? Does the map support the comparison in your
results table? A Matplotlib comparison is also useful; see [A8](#a8) and the
[visualization tutorial](../tutorials/09_visualization.md).

[Open Task 6 in the exercise](exercise.py#L1272).

<a name="reflection"></a>

Reflect beside your outputs:

- Did exclusion fractions differ between training and test? What might that change?
- Which map captured more December incidents, and which covered less area?
  Would ranking by PAI alone hide a trade-off?
- What denominator would you need to discuss risk rather than recorded counts?
- What do zero H3 cells and DBSCAN noise mean under this design?
- Which choices follow the paper, and which adapt it? What did EDA change in your initial proposal?
- Which additional evidence would help distinguish a data-quality issue from a spatial pattern?

These results test associations in recorded incidents. They do not explain
causes or measure fairness, prevention, or the effects of acting on a map.

### Further investigation

Choose one extension after the core tasks:

1. Compare two prespecified settings using January–October for fitting and
   November for validation. Refit the chosen method on January–November,
   then evaluate December once. Record area coverage as well as PAI.
2. Compare hotspot maps with similar measured area coverage. Explain why this
   gives a different comparison from selecting the same percentage of cells.
3. Repeat the fixed design for another recorded category. Read its definition
   and keep settings fixed before viewing its test results.
4. Add an administrative-area baseline or KDE to move closer to the paper.
   A continuous density surface needs an explicit hotspot-area threshold for PAI.

Moran's I and Gi* address spatial association under a chosen weights structure
and null model. They do not replace future-period evaluation. For further study,
start with [PySAL's ESDA tutorials](https://pysal.org/esda/tutorial.html).

### Documentation and walkthroughs

- [Source paper and open preprint](https://discovery.ucl.ac.uk/id/eprint/112873/)
- [Chicago crime metadata](https://data.cityofchicago.org/d/ijzp-q8t2) and [city boundary](https://data.cityofchicago.org/d/qqq8-j68g)
- [DuckDB CSV reader](https://duckdb.org/docs/stable/data/csv/overview.html) and [safe casting](https://duckdb.org/docs/stable/sql/expressions/cast.html)
- [GeoPandas introduction](https://geopandas.org/en/stable/getting_started/introduction.html)
- [H3 polygon tutorial](https://uber.github.io/h3-py/polygon_tutorial.html)
- [DBSCAN worked example](https://scikit-learn.org/stable/auto_examples/cluster/plot_dbscan.html)
- [Plotly bar charts](https://plotly.com/python/bar-charts/) and [Leafmap Kepler walkthrough](https://leafmap.org/notebooks/26_kepler_gl/)
- [Geographic Data Science: exploratory spatial data analysis](https://geographicdata.science/book/notebooks/06_spatial_autocorrelation.html)
