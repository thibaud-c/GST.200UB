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
- [B0. Know the source before downloading](#b0).
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

<a name="b0"></a>

### B0. Know the source before downloading

Use the City of Chicago's [Crimes — 2001 to Present](https://data.cityofchicago.org/d/ijzp-q8t2).
These are police-recorded reports, not all crimes that occurred. Reporting,
recording, and enforcement practices affect the pattern. The source treats murders
as records per victim; other records describe reported incidents. Read the metadata
before treating categories as directly comparable.

The portal omits the latest seven days, revises records, and provides approximate
locations. Its notice prohibits deriving exact addresses and cautions against
comparisons over time. Our temporal split is a teaching experiment on recorded
patterns, not a claim about changes in true crime or safety. Do not identify people,
reconstruct addresses, label neighbourhoods “dangerous,” or propose patrol targets
from these results.

The download covers **all of 2025**, from **2025-01-01 inclusive to 2026-01-01
exclusive**, including 31 December. It saves `data/chicago_2025.csv`. Task 1 selects
BURGLARY throughout that same year. Training is **2025-01-01 inclusive to
2025-12-01 exclusive**; December evaluation is **2025-12-01 inclusive to
2026-01-01 exclusive**. The extract retains all
categories for training EDA; the core model uses **BURGLARY**. Chicago's label
does not necessarily match the paper's residential-burglary category.

The cell below downloads a bounded CSV and city boundary once to `data/` and
records the URLs and UTC retrieval time. It uses the portal's API, a web interface
for requesting data. The `$where` filter runs on the portal; later SQL runs locally
in DuckDB. The limit is a safety cap, not a random sample; the audit checks it was
not reached. Do not enlarge the date window without adding pagination or using
a complete portal export.

Run this cell once. Paths assume this notebook's working folder is `lab_02`; see the
[relative-path guide](https://github.com/thibaud-c/GST.200UB/blob/main/tutorials/03_cli.md#relative-paths-in-a-notebook).

You can also [filter and export the data on the website](README.md#download-from-the-website).
Save that original as `data/chicago_2025_export.csv`. When no analysis CSV is cached,
B0 imports it into `data/chicago_2025.csv`. This conversion standardises headers
such as `Primary Type` to `primary_type` and converts the website's dates to a
consistent timestamp format. The raw export stays unchanged. The import checks
the year and size before writing, and records its source and import time.

<a name="b1"></a>

### B1. Audit the extract with DuckDB

(See [A1](#a1-eda-begins-with-questions-about-the-records): counts, missing values,
and `TRY_CAST`; [A2](#a2-time-denominators-and-misleading-summaries): calendar counts and denominators.)

DuckDB scans the file and returns a small summary rather than loading the whole
city's table into a GeoDataFrame. This becomes useful with larger archives. CSV
still needs scanning; Parquet can additionally skip columns and data blocks.
“Fast” does not mean every query reads only its returned rows.

We read as text (`all_varchar=true`) and explicitly convert fields so that bad
values can be counted. Inspect schema, count, date coverage, missing coordinates,
and duplicate IDs **before** dropping anything. Read the cached `.source.txt`
files when noting the data version used.

| Audit table | Period and purpose |
| --- | --- |
| `source_audit` | All 2025, for coverage, unique IDs, missing values, and Task 1's annual burglary count. |
| `category_audit` | January–November, for training EDA and daily-count checks. |

Match each check to its period. Task 1 keeps all annual burglaries, while EDA
uses training records only. These counts come from
the same cached file and may change when the portal revises its records. SQL
results in this notebook are pandas DataFrames.

Explore this table before coding a model:

1. Which categories dominate? Which have the highest missing-coordinate percentage?
2. Compare percentage and absolute missing counts. Would you prioritise the same rows?
3. Read the category descriptions in the source. Why would combining THEFT and
   BURGLARY change the question? Do not silently drop categories with unfamiliar labels.
4. Could a change in reporting or geocoding explain a pattern you were about to
   attribute to human behaviour?

Add one SQL cell for the daily **training-period** counts of BURGLARY. Use the
calendar pattern in [A2](#a2-time-denominators-and-misleading-summaries)
for all 334 days of January–November. Make a Plotly chart;
check gaps and coverage before interpreting peaks. Keep December hidden from this
pattern exploration. Your table should have 334 calendar days, and its total
should equal the BURGLARY count in `category_audit`. Add a Markdown cell separating **observation**, **possible
explanation**, and **evidence you would need**.

<a name="task-1"></a>

### Task 1. Select the analysis records in SQL

(See [A1](#a1-eda-begins-with-questions-about-the-records): SQL audit and conversion;
[A3](#a3-clean-deliberately-and-keep-future-records-separate): filters and date windows.)

Replace the next SQL cell. Its output must stay named `selected_records`.
Read `csv_path` with `read_csv` as above. Return only:

- `id` as an integer;
- `date` converted to a timestamp and renamed `occurred_at`;
- `primary_type`, `latitude`, and `longitude` (coordinates as doubles).

Keep BURGLARY records from **2025-01-01 inclusive to 2026-01-01 exclusive**.
Use `TRY_CAST` and keep missing coordinates for now so Task 2 can account for
exclusions. Order by `id`. Do not use `LIMIT`: it would bias the model's input.
The placeholder query below is deliberately harmless; write your own full query.
The following check uses the annual burglary count in `source_audit`. Keep
December in this selection; the later split keeps it out of training.

<a name="task-2"></a>

### Task 2. Prepare points and account for exclusions

(See [A3](#a3-clean-deliberately-and-keep-future-records-separate): coordinate checks and duplicate IDs;
[A4](#a4-geometry-distances-and-a-fixed-study-area): points, CRS, and boundary predicates.)

Write `prepare_points(records, boundary)`. Return a GeoDataFrame in the boundary's
metric CRS, keeping the original attributes. Exclude missing or out-of-range
coordinates, keep one row per ID, make points in EPSG:4326, project them, and keep
only points intersecting the city boundary. The SQL step already validated dates.
Inspect the boundary: our footprint includes everything in that polygon, without
an exposure or land-use mask. Keep it identical for every method.

The following cell reports how many records were removed. Add your own breakdown
of missing coordinates versus outside-boundary records, separately for training
and test. A single retained-row count can hide unequal exclusions.
Use the [A4 exclusion audit](#exclusion-audit) to organise the counts and keep
one reason per excluded row.

<a name="training-geography"></a>

### Inspect training geography before choosing hotspots

(See [A3](#a3-clean-deliberately-and-keep-future-records-separate): avoiding test leakage;
[A5](#a5-h3-and-discrete-global-grids): H3 count distributions and densities.)

Use a Matplotlib scatter map of `train` against the city outline. Look for distant
points and repeated coordinates. Add an H3 count histogram after building the grid
below. Compare its mean and median, and count zero cells. Skewed counts explain
why a mean-based threshold may behave unexpectedly.

Freeze the following course settings **before** viewing test patterns: H3 resolution
8 with a 10% area budget; DBSCAN `eps=500` m and `min_samples=10`. These are teaching
settings, not estimated optimal values. For parameter selection, use the
January–October fitting and November validation plan from
[A3](#a3-clean-deliberately-and-keep-future-records-separate), record your choice, then refit on the
full training period. Do not optimise settings against December PAI.

<a name="task-3"></a>

### Task 3. Build H3 hotspots from training points

(See [A5](#a5-h3-and-discrete-global-grids): H3 IDs, zero cells, density, and area budgets.)

Write `h3_hotspots(points, grid, area_budget)`. Transform points to
EPSG:4326, assign resolution-8 H3 IDs, count them, and map counts to a **copy** of
the full grid. Fill empty cells with zero. Compute density from each clipped
cell's actual area. Sort by density descending, then H3 ID ascending. Return the
positive-count prefix whose cumulative area is at most `area_budget`, keeping
`h3_id`, `count`, and the metric geometry. Do not replace the area budget with a
quantile of cell counts.

Inspect zero counts and very small edge cells before selection. Explain why a
10% cell selection need not cover 10% of the city, even with a global grid.

<a name="task-4"></a>

### Task 4. Turn DBSCAN clusters into hotspot polygons

(See [A6](#a6-dbscan-density-connected-points): `eps`, `min_samples`, noise, and convex hulls.)

Write `dbscan_hotspots(points, eps_m, min_samples)`. Use projected x/y coordinates
from the supplied **training** points. Fit DBSCAN, exclude noise label -1, and take
one convex hull per cluster. Return a GeoDataFrame of positive-area hulls in the
input CRS, with `cluster_id` and `n_points`. Print the number of noise points and
zero-area hulls excluded. Return an empty GeoDataFrame with these columns when
there are no usable clusters. Do not sample test points or buffer zero-area hulls
to manufacture a PAI denominator.

Start with the seven-point example before applying it to Chicago. Label numbers
can vary; cluster membership and sizes are what matter.
The [A6 schema example](#cluster-schema) shows how to retain columns, geometry,
and CRS for an empty result. Task 4's check verifies those properties too.

<a name="task-5"></a>

### Task 5. Calculate and interpret PAI

(See [A7](#a7-pai-distinguish-hits-from-area-covered): the PAI formula and hit counting;
[A4](#a4-geometry-distances-and-a-fixed-study-area): metric areas and a fixed boundary.)

Write `compute_pai(hits, total, hotspot_area, study_area)`. Return the PAI formula.
Return `None` if there are no test records or either area is zero. Zero hits with
positive denominators gives 0. All inputs here are non-negative and areas share
the same units. Try the hand-calculated examples first.
Use the [A7 guard example](#none-guard) if `None` and early `return` are new to you.

The shared evaluation below applies the same union, clipping, and boundary-point
rules to both methods. Read it before running. H3 uses a 10% area budget; DBSCAN's
area emerges from its clusters. **Different area coverage limits a direct ranking.**
The whole-city baseline has PAI 1 and 100% hit rate but gives no spatial focus.

<a name="task-6"></a>

### Task 6. Inspect maps and challenge your conclusion

(See [A8](#a8-explore-with-leafmaps-kepler-backend): Kepler layers;
[A2](#a2-time-denominators-and-misleading-summaries): denominators;
[A7](#a7-pai-distinguish-hits-from-area-covered): interpreting hits and area coverage.)

Create a Leafmap Kepler map centred at `[41.88, -87.63]`, zoom 10. Add the city
outline, H3 hotspots, and DBSCAN hulls in EPSG:4326. After freezing the methods,
you may add December points to inspect misses. Omit `h3_id` from the H3 display
copy so the map uses clipped geometries. Use distinct layer names, transparency,
and a legend stating the period and crime category. Keep source attribution.
Inspect hulls spanning empty space, clipped grid edges, and incidents missed by
both methods. Use a Matplotlib map for a side-by-side static comparison if helpful.

<a name="reflection"></a>

Reflect beside your outputs; there is no separate report:

- How many records were excluded, and did the exclusion fraction differ by period?
- Which method captured more incidents? Which concentrated hits in less area?
  Would your conclusion change if you compared only PAI?
- What denominator would be needed to discuss risk, rather than recorded incident density?
- What do zero cells and DBSCAN noise actually mean? Do either establish safety?
- Which choices came from the paper, and which are our adaptations?
- How might reporting practices, approximate geocoding, or the city boundary
  explain a pattern? What evidence would distinguish those explanations?
- Revisit your initial proposal. What did EDA change about it?

A stable pattern is an association in recorded data, not an explanation of why
crime happens. PAI cannot measure fairness, prevention, or the consequences of
acting on a map. No result here justifies decisions about individuals or neighbourhoods.

### Further investigation

Choose one extension after completing the core:

1. **Validation:** fit on January–October and score on November for two prespecified H3
   resolutions or DBSCAN radii. Choose without December, refit on January–November,
   and evaluate December once. Log area fraction as well as PAI.
2. **Matched area:** compare maps with similar measured hotspot coverage, reporting
   the remaining difference. Explain why this is more informative than comparing
   the top 10% of differently sized units.
3. **Transfer:** repeat the fixed design for another recorded category without
   changing thresholds after inspecting its test results. Explain category definitions.
4. **Closer to the paper:** add an administrative-area baseline or KDE and document
   its footprint threshold. A smooth density surface needs a declared area threshold
   before PAI can be calculated.

Moran's I and Gi* ask about spatial association or local concentrations under a
specified weights structure and null model. They are not replacements for a
future-period test. Study weights, zero cells, permutations, and multiple testing
before adding them; see [PySAL's ESDA tutorials](https://pysal.org/esda/tutorial.html).

### Documentation and walkthroughs

- [Source paper and open preprint](https://discovery.ucl.ac.uk/id/eprint/112873/)
- [Chicago crime metadata](https://data.cityofchicago.org/d/ijzp-q8t2) and [city boundary](https://data.cityofchicago.org/d/qqq8-j68g)
- [Socrata query filters](https://dev.socrata.com/docs/queries/where.html)
- [DuckDB CSV reader](https://duckdb.org/docs/stable/data/csv/overview.html)
- [H3 polygon tutorial](https://uber.github.io/h3-py/polygon_tutorial.html)
- [DBSCAN worked example](https://scikit-learn.org/stable/auto_examples/cluster/plot_dbscan.html)
- [Plotly bar charts](https://plotly.com/python/bar-charts/) and [Leafmap Kepler walkthrough](https://leafmap.org/notebooks/26_kepler_gl/)
- [Geographic Data Science: exploratory spatial data analysis](https://geographicdata.science/book/notebooks/06_spatial_autocorrelation.html)

AI has been used to review and improve the course materials.
