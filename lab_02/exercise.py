import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium", sql_output="pandas")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import geopandas as gpd
    import h3
    import plotly.express as px
    import matplotlib.pyplot as plt
    import leafmap.kepler as leafmap
    from sklearn.cluster import DBSCAN
    from shapely.geometry import Polygon, box
    from pathlib import Path
    from urllib.parse import urlencode
    from urllib.request import urlopen
    from datetime import datetime, timezone

    return (
        DBSCAN,
        Path,
        Polygon,
        box,
        datetime,
        gpd,
        h3,
        leafmap,
        mo,
        pd,
        plt,
        px,
        timezone,
        urlencode,
        urlopen,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Lab 02: what can a crime hotspot map tell us?

    Can earlier police records help locate later incidents? Run Part A's small examples,
    then complete Part B for Chicago. Replace each task's `return None`, run its check,
    and keep short reflections beside your results.

    Before coding, inspect Figure 1 in the [paper](https://link.springer.com/article/10.1057/palgrave.sj.8350066).
    What would make a hotspot comparison fair?

    [Setup and scope](https://github.com/thibaud-c/GST.200UB/blob/main/lab_02/README.md) · [Study notes](https://github.com/thibaud-c/GST.200UB/blob/main/lab_02/notes.md#overview)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## What we reproduce, change, and leave out

    We adapt the paper's temporal evaluation and PAI to Chicago. H3 and DBSCAN are our
    method choices; we do not reproduce the paper's numerical results.

    ## Quick reference

    [Functions and documentation](https://github.com/thibaud-c/GST.200UB/blob/main/lab_02/notes.md#quick-reference). Open a section's **Notes** link
    when you need the longer explanation. Keep this notebook open while reading.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Part A. Learn the operations on small examples

    ## A1. EDA begins with questions about the records

    EDA means asking questions, inspecting data, and checking possible explanations.
    What does one row represent? Predict the row, duplicate, bad-date, and missing-coordinate
    counts before running the audit.

    [Notes: EDA](https://github.com/thibaud-c/GST.200UB/blob/main/lab_02/notes.md#a1) · Apply in [B1](#b1-audit-the-extract-with-duckdb)
    and [Task 1](#task-1-select-the-analysis-records-in-sql).
    """)
    return


@app.cell
def _(pd):
    # Inspect the original records before choosing what to exclude.
    demo_records = pd.DataFrame({
        "id": [1, 2, 2, 3, 4, 5, 6, 7],
        "date": ["2025-01-01", "2025-01-01", "2025-01-01", "2025-01-03",
                 "bad date", "2025-01-03", "2025-02-01", "2025-12-01"],
        "primary_type": ["BURGLARY", "THEFT", "THEFT", "BURGLARY",
                         "THEFT", "BURGLARY", "BURGLARY", "BURGLARY"],
        "latitude": [41.88, 41.89, 41.89, None, 41.87, 999, 41.88, 41.88],
        "longitude": [-87.63, -87.64, -87.64, -87.65, -87.62, -87.63, -87.64, -87.64],
    })
    demo_records
    return (demo_records,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Edit the next cells as SQL cells. Give every output a unique name. DuckDB runs
    inside marimo. `COUNT(column)` skips missing values; `TRY_CAST` returns `NULL`
    when conversion fails. [SQL editor help](https://github.com/thibaud-c/GST.200UB/blob/main/tutorials/07_duckdb.md).
    """)
    return


@app.cell
def _(mo):
    demo_audit = mo.sql(
        f"""
        -- Count problems before deleting records; COUNT(column) skips NULLs.
        SELECT COUNT(*) AS rows,
               COUNT(DISTINCT id) AS distinct_ids,
               COUNT(*) - COUNT(TRY_CAST(date AS TIMESTAMP)) AS unusable_dates,
               COUNT(*) - COUNT(latitude) AS missing_latitudes
        FROM demo_records
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Expect 8 rows, 7 distinct IDs, 1 unusable date, and 1 missing latitude.
    Why does latitude 999 pass the missing-value check? Record counts before and after exclusions.
    """)
    return


@app.cell
def _(mo):
    demo_missingness = mo.sql(
        f"""
        -- Group first to see whether missingness differs between crime categories.
        SELECT primary_type, COUNT(*) AS rows,
               COUNT(*) - COUNT(latitude) AS missing_latitudes
        FROM demo_records
        GROUP BY primary_type
        ORDER BY primary_type
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Try calculating the missing-latitude percentage for each category before removing rows.

    ## A2. Time, denominators, and misleading summaries

    A calendar join keeps zero-record days visible. First check that the extract covers those days.

    [Notes: counts, densities, rates](https://github.com/thibaud-c/GST.200UB/blob/main/lab_02/notes.md#a2) · Apply in [B1](#b1-audit-the-extract-with-duckdb)
    and [Task 6](#task-6-inspect-maps-and-challenge-your-conclusion).
    """)
    return


@app.cell
def _(mo):
    demo_daily = mo.sql(
        f"""
        -- Join onto a calendar so days with no recorded incidents stay visible.
        WITH daily AS (
            SELECT CAST(TRY_CAST(date AS TIMESTAMP) AS DATE) AS day,
                   COUNT(DISTINCT id) AS incidents
            FROM demo_records
            WHERE TRY_CAST(date AS TIMESTAMP) < TIMESTAMP '2025-01-03'
            GROUP BY day
        )
        SELECT CAST(calendar.day AS DATE) AS day,
               COALESCE(daily.incidents, 0) AS incidents
        FROM generate_series(DATE '2025-01-01', DATE '2025-01-02', INTERVAL 1 DAY) AS calendar(day)
        LEFT JOIN daily ON calendar.day = daily.day
        ORDER BY day
        """
    )
    return (demo_daily,)


@app.cell
def _(demo_daily, px):
    px.bar(demo_daily, x="day", y="incidents",
           labels={"day": "Date", "incidents": "Recorded incidents"},
           title="Daily counts, including a day with zero records").update_xaxes(
               dtick=86400000, tickformat="%d %b"
           )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Expect 2 incidents on 1 January and 0 on 2 January. Why would counting rows change the first bar?
    A count measures volume, density divides by area, and a rate needs an exposure denominator.

    Try comparing 40 records over 20 days with 45 over 30 days. Which has the higher daily average?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A3. Clean deliberately and keep future records separate

    Read each condition. We remove the duplicate ID only because it repeats the same record.
    Conflicting duplicates need investigation.

    [Notes: cleaning and leakage](https://github.com/thibaud-c/GST.200UB/blob/main/lab_02/notes.md#a3) · Apply in
    [Task 1](#task-1-select-the-analysis-records-in-sql),
    [Task 2](#task-2-prepare-points-and-account-for-exclusions), and
    [training exploration](#inspect-training-geography-before-choosing-hotspots).
    """)
    return


@app.cell
def _(demo_records, pd):
    # Work on a copy so the original values remain available for the audit.
    demo_clean = demo_records.copy()
    demo_clean["occurred_at"] = pd.to_datetime(demo_clean["date"], errors="coerce")
    _valid = (
        demo_clean["occurred_at"].notna()
        & demo_clean["latitude"].between(-90, 90)
        & demo_clean["longitude"].between(-180, 180)
    )
    demo_clean = demo_clean.loc[_valid].drop_duplicates("id").copy()
    print("Rows before:", len(demo_records), "after:", len(demo_clean))
    demo_clean
    return (demo_clean,)


@app.cell
def _(demo_clean):
    # Hold December aside before exploring or choosing any hotspot settings.
    demo_train = demo_clean.loc[demo_clean["occurred_at"] < "2025-12-01"].copy()
    demo_test = demo_clean.loc[demo_clean["occurred_at"] >= "2025-12-01"].copy()
    assert set(demo_train["id"]).isdisjoint(demo_test["id"])
    print("Training IDs:", demo_train["id"].tolist())
    print("Test IDs:", demo_test["id"].tolist())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Expect 4 clean records: training IDs 1, 2, 6; test ID 7. The cutoff belongs to the test period.
    **Leakage** means using future information to build or choose a model. Explore training
    patterns and freeze settings before viewing test patterns.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A4. Geometry, distances, and a fixed study area

    A GeoDataFrame is a table with geometry and a coordinate reference system, or CRS.
    In the first cell, `points_from_xy` turns longitude and latitude into points.
    EPSG:4326 describes these coordinates in degrees; it does not give metre distances.

    In the second cell, `estimate_utm_crs()` suggests a local metre-based CRS from the
    points' location. For Chicago it returns EPSG:32616. Estimating the CRS does not
    change coordinates: `to_crs()` transforms both layers before we measure or map them.
    It changes the geometry; the original longitude/latitude columns stay unchanged.
    Keep the same study boundary for every method.

    [Notes: CRS and boundary checks](https://github.com/thibaud-c/GST.200UB/blob/main/lab_02/notes.md#a4) · Apply in
    [Task 2](#task-2-prepare-points-and-account-for-exclusions) and
    [Task 5](#task-5-calculate-and-interpret-pai).

    If projection or plotting fails because package data are missing, see the
    [Windows repair steps](https://github.com/thibaud-c/GST.200UB/blob/main/lab_02/README.md#windows-known-issue-package-repair).
    """)
    return


@app.cell
def _(box, gpd, pd):
    # Start with a coordinate table. Longitude is x; latitude is y.
    _locations = pd.DataFrame({
        "id": [0, 1, 2, 3, 4, 5, 6],
        "longitude": [
            -87.637595399343, -87.637354356880, -87.637476668665,
            -87.630417242846, -87.630176179584, -87.630298481945,
            -87.627351080305,
        ],
        "latitude": [
            41.884058355479, 41.884059693513, 41.884239150389,
            41.889502056260, 41.889503379367, 41.889682843786,
            41.884114775824,
        ],
    })
    demo_points_wgs84 = gpd.GeoDataFrame(
        _locations,
        geometry=gpd.points_from_xy(_locations["longitude"], _locations["latitude"]),
        crs=4326,
    )
    demo_boundary_wgs84 = gpd.GeoDataFrame(
        geometry=[box(-87.6389, 41.8831, -87.6267, 41.8923)], crs=4326,
    )
    print("Starting CRS:", demo_points_wgs84.crs)
    demo_points_wgs84
    return demo_boundary_wgs84, demo_points_wgs84


@app.cell
def _(demo_boundary_wgs84, demo_points_wgs84, plt):
    # Estimate a local UTM CRS, then transform both layers into it.
    _metric_crs = demo_points_wgs84.estimate_utm_crs()
    demo_points = demo_points_wgs84.to_crs(_metric_crs)
    demo_boundary = demo_boundary_wgs84.to_crs(_metric_crs)
    print("Estimated metric CRS:", _metric_crs)

    # Passing the same axes to both layers draws them on one map.
    _fig, _ax = plt.subplots(figsize=(5, 5))
    demo_boundary.boundary.plot(ax=_ax, color="black")
    demo_points.plot(ax=_ax, color="navy")
    _ax.set(xlabel="Easting (m)", ylabel="Northing (m)", title="Inspect the input points")
    _fig
    return demo_boundary, demo_points


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Count exclusions by period

    This small table supplies the outcomes of filtering eight records. Count each
    excluded row under one reason. Predict which period loses a larger proportion.
    In Task 2, assign outcomes as you filter your records, then make the same audit.

    [Notes: exclusion audit](https://github.com/thibaud-c/GST.200UB/blob/main/lab_02/notes.md#exclusion-audit) ·
    Apply in [Task 2](#task-2-prepare-points-and-account-for-exclusions).
    """)
    return


@app.cell
def _(pd):
    _outcomes = pd.DataFrame({
        "period": ["training"] * 4 + ["test"] * 4,
        "outcome": [
            "retained", "retained", "missing/invalid coordinates", "duplicate ID",
            "retained", "missing/invalid coordinates", "outside boundary", "outside boundary",
        ],
    })
    # One outcome per input row prevents double-counting exclusions.
    demo_exclusion_audit = pd.crosstab(_outcomes["period"], _outcomes["outcome"])
    demo_exclusion_audit["input_rows"] = demo_exclusion_audit.sum(axis=1)
    demo_exclusion_audit["excluded_rows"] = (
        demo_exclusion_audit["input_rows"] - demo_exclusion_audit["retained"]
    )
    demo_exclusion_audit["excluded_pct"] = (
        100 * demo_exclusion_audit["excluded_rows"] / demo_exclusion_audit["input_rows"]
    )
    assert demo_exclusion_audit.loc["training", "excluded_pct"] == 50
    assert demo_exclusion_audit.loc["test", "excluded_pct"] == 75
    demo_exclusion_audit
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Check coordinate ranges and outside-boundary points. Duplicate coordinates can represent
    separate incidents; duplicate IDs require investigation.

    ## A5. H3 and discrete global grids

    H3 assigns global cell IDs, mostly hexagons. Higher resolution means smaller cells.
    Resolution changes patterns; a cell count is not a risk measure.

    [Notes: H3, grid choices, and MAUP](https://github.com/thibaud-c/GST.200UB/blob/main/lab_02/notes.md#a5) · Apply in
    [training exploration](#inspect-training-geography-before-choosing-hotspots) and
    [Task 3](#task-3-build-h3-hotspots-from-training-points).
    """)
    return


@app.cell
def _(mo):
    demo_resolution = mo.ui.slider(7, 10, value=8, label="H3 resolution", show_value=True)
    demo_resolution
    return (demo_resolution,)


@app.cell
def _(demo_points, demo_resolution, h3):
    # H3 needs geographic coordinates, while distance calculations use metres.
    _demo_wgs = demo_points.to_crs(4326)
    demo_cell_ids = []
    for _point in _demo_wgs.geometry:
        _cell_id = h3.latlng_to_cell(_point.y, _point.x, demo_resolution.value)
        demo_cell_ids.append(_cell_id)
    _first_id = demo_cell_ids[0]
    print("First cell:", _first_id)
    print("Its area (km²):", round(h3.cell_area(_first_id, unit="km^2"), 3))
    print("Occupied cells:", len(set(demo_cell_ids)))
    return (demo_cell_ids,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    H3 takes **latitude, longitude**; Shapely polygons use longitude, latitude.
    Build the grid over the whole study area, including zero cells. The helper includes
    boundary-crossing cells and clips them to the boundary.
    """)
    return


@app.cell
def _(Polygon, gpd, h3):
    def make_grid(boundary, resolution):
        """Cover and clip a metric study boundary with H3 cells, including empty ones."""
        shape = h3.geo_to_h3shape(boundary.to_crs(4326).geometry.union_all().__geo_interface__)
        cell_ids = sorted(h3.h3shape_to_cells_experimental(shape, resolution, contain="overlap"))
        polygons = []
        for cell_id in cell_ids:
            coordinates = []
            # H3 gives latitude first; Shapely needs longitude first.
            for latitude, longitude in h3.cell_to_boundary(cell_id):
                coordinates.append((longitude, latitude))
            polygons.append(Polygon(coordinates))
        grid = gpd.GeoDataFrame({"h3_id": cell_ids}, geometry=polygons, crs=4326)
        # Clip in the study area's metric CRS, including cells with no incidents.
        grid = gpd.clip(grid.to_crs(boundary.crs), boundary)
        return grid.loc[grid.geometry.area > 0].copy()

    return (make_grid,)


@app.cell
def _(
    demo_boundary,
    demo_cell_ids,
    demo_points,
    demo_resolution,
    make_grid,
    pd,
):
    demo_grid = make_grid(demo_boundary, demo_resolution.value)
    _counts = pd.Series(demo_cell_ids).value_counts()
    # Match counts by cell ID. Cells missing from the count table get zero.
    demo_grid["count"] = demo_grid["h3_id"].map(_counts).fillna(0).astype(int)
    demo_grid["area_km2"] = demo_grid.geometry.area / 1_000_000
    demo_grid["density"] = demo_grid["count"] / demo_grid["area_km2"]
    assert demo_grid["count"].sum() == len(demo_points)
    demo_grid[["h3_id", "count", "area_km2", "density"]]
    return (demo_grid,)


@app.cell
def _(demo_grid, demo_points, plt):
    _fig, _ax = plt.subplots(figsize=(6, 5))
    demo_grid.plot(ax=_ax, column="count", edgecolor="white", legend=True)
    demo_points.plot(ax=_ax, color="black", markersize=12)
    _ax.set_title("H3 counts: empty cells belong on the map too")
    _ax.set_axis_off()
    _fig
    return


@app.cell
def _(demo_grid, px):
    print(demo_grid["count"].describe())
    print("Zero cells:", int(demo_grid["count"].eq(0).sum()))
    px.histogram(demo_grid, x="count",
                 labels={"count": "Incidents per cell"},
                 title="Distribution across all cells, including zeros").update_traces(
                     xbins=dict(start=-0.5, end=demo_grid["count"].max() + 0.5, size=1)
                 ).update_yaxes(title="Number of cells", dtick=1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Compare the mean, median, maximum, and zero count. Change resolution once and inspect
    the map and histogram. Do tiny clipped cells have high density?

    For hotspots, rank by training density and keep whole cells within a study-area budget.
    A percentage of cells is not a percentage of area. [Selection details](https://github.com/thibaud-c/GST.200UB/blob/main/lab_02/notes.md#a5).
    """)
    return


@app.cell
def _(demo_boundary, demo_grid):
    # Keep whole cells in rank order until the area budget would be exceeded.
    _demo_ranked = demo_grid.sort_values(["density", "h3_id"], ascending=[False, True])
    _demo_budget = 0.2 * demo_boundary.geometry.area.sum()
    demo_h3_hotspots = _demo_ranked.loc[
        (_demo_ranked.geometry.area.cumsum() <= _demo_budget)
        & (_demo_ranked["count"] > 0)
    ].copy()
    print("Selected cells:", len(demo_h3_hotspots))
    print("Actual area fraction:", demo_h3_hotspots.geometry.area.sum() / demo_boundary.geometry.area.sum())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    An empty selection is valid if no cell fits the budget. Do not enlarge it after viewing test results.

    ## A6. DBSCAN: density-connected points

    `eps` is a neighbour distance, not cluster diameter. `min_samples` includes the point
    itself. Label -1 means noise under these settings.

    [Notes: DBSCAN and hulls](https://github.com/thibaud-c/GST.200UB/blob/main/lab_02/notes.md#a6) · Apply in
    [Task 4](#task-4-turn-dbscan-clusters-into-hotspot-polygons).
    """)
    return


@app.cell
def _(mo):
    demo_eps = mo.ui.slider(10, 900, step=10, value=50,
                            label="DBSCAN neighbour distance (metres)", show_value=True)
    demo_eps
    return (demo_eps,)


@app.cell
def _(DBSCAN, demo_eps, demo_points, pd, plt):
    demo_clusters = demo_points.copy()
    # Projected x/y coordinates make the neighbour distance a number of metres.
    _xy = pd.DataFrame({"x": demo_clusters.geometry.x, "y": demo_clusters.geometry.y})
    demo_clusters["cluster_id"] = DBSCAN(eps=demo_eps.value, min_samples=3).fit_predict(_xy)
    print(demo_clusters["cluster_id"].value_counts().sort_index())
    _fig, _ax = plt.subplots(figsize=(5, 5))
    demo_clusters.plot(ax=_ax, column="cluster_id", categorical=True, legend=True)
    _ax.set_title("Cluster labels are categories; -1 is noise")
    _fig
    return (demo_clusters,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    At 50 m expect two three-point clusters and one noise point. Predict and try 10 m and
    900 m, then restore 50 m. Labels are names, not ranks.

    A convex hull gives each cluster an area for PAI. It may span empty space.
    Exclude and report zero-area hulls rather than inventing an area.
    """)
    return


@app.cell
def _(demo_clusters, demo_points, gpd):
    _demo_rows = []
    _demo_skipped = 0
    # Each group is one cluster; noise and zero-area hulls do not supply hotspot area.
    for _label, _group in demo_clusters.groupby("cluster_id"):
        if _label == -1:
            continue
        _hull = _group.geometry.union_all().convex_hull
        if _hull.area == 0:
            _demo_skipped += 1
            continue
        _demo_rows.append({
            "cluster_id": int(_label), "n_points": len(_group), "geometry": _hull,
        })
    demo_db_hotspots = gpd.GeoDataFrame(
        _demo_rows, columns=["cluster_id", "n_points", "geometry"],
        geometry="geometry", crs=demo_points.crs,
    )
    print("Noise points:", int(demo_clusters["cluster_id"].eq(-1).sum()))
    print("Zero-area clusters excluded:", _demo_skipped)
    demo_db_hotspots
    return (demo_db_hotspots,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    At 50 m, inspect the two rows and their `n_points`. Then set the slider to 10 m.
    The empty GeoDataFrame still has `cluster_id`, `n_points`, an active `geometry`
    column, and a CRS because we declared them in the constructor. It is not `None`.
    Restore 50 m before continuing. [Result schema](https://github.com/thibaud-c/GST.200UB/blob/main/lab_02/notes.md#cluster-schema).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A7. PAI: distinguish hits from area covered

    **PAI = (hits / test incidents) / (hotspot area / study area).**

    Twenty hits out of 100 in 10% of the area gives PAI 2. Show hits and area alongside PAI;
    a tiny area can inflate it. Empty hotspots or test sets make PAI undefined.

    [Notes: interpretation](https://github.com/thibaud-c/GST.200UB/blob/main/lab_02/notes.md#a7) · Apply in
    [Task 5](#task-5-calculate-and-interpret-pai) and
    [Task 6](#task-6-inspect-maps-and-challenge-your-conclusion).
    """)
    return


@app.cell
def _():
    _demo_hits = 20
    _demo_total = 100
    _demo_hotspot_area = 10
    _demo_study_area = 100
    demo_pai = (_demo_hits / _demo_total) / (_demo_hotspot_area / _demo_study_area)
    assert demo_pai == 2
    print("Hit rate:", _demo_hits / _demo_total, "PAI:", demo_pai)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A Python **guard** checks an undefined case before division. `return None`
    exits the function without a numerical result; zero remains a valid share.
    Adapt this pattern to Task 5's denominators. [Notes: guards](https://github.com/thibaud-c/GST.200UB/blob/main/lab_02/notes.md#none-guard).
    """)
    return


@app.cell
def _():
    def _safe_share(part, total):
        # Stop before attempting division by zero.
        if total == 0:
            return None
        return part / total

    assert _safe_share(0, 4) == 0
    assert _safe_share(2, 0) is None
    print("Ordinary share:", _safe_share(2, 4))
    print("Zero share:", _safe_share(0, 4))
    print("Undefined share:", _safe_share(2, 0))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Union overlapping hotspots, clip to the fixed boundary, and measure area once.
    Count each unique test incident against that union with `intersects`, which includes boundary points.
    """)
    return


@app.cell
def _(demo_boundary, demo_db_hotspots, demo_points):
    # Union first so overlapping polygons do not count an incident twice.
    _demo_union = demo_db_hotspots.geometry.union_all().intersection(demo_boundary.geometry.union_all())
    _demo_future = demo_points.iloc[[0, 3, 6]].copy()
    print("Hits:", int(_demo_future.intersects(_demo_union).sum()), "of", len(_demo_future))
    print("Hotspot area (m²):", round(_demo_union.area, 2))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Expect 2 hits among 3 points. These geometry examples are not a future-period test.
    Try 40 hits out of 100 in 25% of the area: PAI is 1.6. More hits, but less concentration. Why?

    ## A8. Explore with Leafmap's Kepler backend

    Calculate in the metric CRS; send EPSG:4326 geometry to the web map.
    Inspect layers and individual records.

    [Notes: map controls and display help](https://github.com/thibaud-c/GST.200UB/blob/main/lab_02/notes.md#a8) · Apply in
    [Task 6](#task-6-inspect-maps-and-challenge-your-conclusion).
    """)
    return


@app.cell
def _(demo_db_hotspots, demo_grid, demo_points, leafmap):
    demo_map = leafmap.Map(center=[41.89, -87.63], zoom=13, height=500)
    demo_map.add_gdf(demo_grid.drop(columns="h3_id").to_crs(4326), layer_name="H3 grid")
    demo_map.add_gdf(demo_db_hotspots.to_crs(4326), layer_name="DBSCAN hulls")
    # Extra longitude/latitude columns can create a second automatic point layer.
    demo_map.add_gdf(demo_points[["id", "geometry"]].to_crs(4326), layer_name="Training points")
    demo_map
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Style the grid by `count` and inspect a zero cell and a hull. The display copy omits
    `h3_id` so Kepler draws our clipped polygons. If the widget displays poorly, use the
    Matplotlib maps.

    Before Part B, explain H3's coordinate order, `eps`, and why evaluation needs later records.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Part B. Reproduce the evaluation idea with Chicago data

    ## B0. Know the source before downloading

    These are approximate police-recorded reports, not all crime or a measure of safety.
    Read the [source metadata](https://data.cityofchicago.org/d/ijzp-q8t2); do not reconstruct addresses.

    Download all of **2025**, from 2025-01-01 inclusive to 2026-01-01 exclusive, into
    `data/chicago_2025.csv`. Use January–November for training and predict December hotspots.
    Evaluate the frozen hotspot maps against December's held-out records.

    To download through the website, follow the [export steps](https://github.com/thibaud-c/GST.200UB/blob/main/lab_02/README.md#download-from-the-website).
    You can also run the cell below to download the data.

    [Notes: source limits, download window, and paths](https://github.com/thibaud-c/GST.200UB/blob/main/lab_02/notes.md#b0).
    """)
    return


@app.cell
def _(Path, datetime, pd, timezone, urlencode, urlopen):
    Path("data").mkdir(exist_ok=True)
    _export_path = Path("data/chicago_2025_export.csv")
    _crime_path = Path("data/chicago_2025.csv")
    # Preserve a website export and create the analysis copy only when needed.
    if _export_path.exists() and not _crime_path.exists():
        _export = pd.read_csv(_export_path, dtype="string", encoding="utf-8-sig", nrows=250000)
        assert len(_export) < 250000, "Filter the website export to Year = 2025; the download cap was reached."
        # Website and API downloads can use different column labels and date formats.
        _export.columns = _export.columns.str.strip().str.lower().str.replace(" ", "_", regex=False)
        _columns = ["id", "date", "primary_type", "description", "district", "latitude", "longitude"]
        assert set(_columns).issubset(_export.columns), "Export the original columns, including Date and Primary Type."
        _export = _export.loc[:, _columns].copy()
        _export["date"] = pd.to_datetime(_export["date"], format="mixed")
        assert _export["date"].dt.year.eq(2025).all(), "Filter the website to Year = 2025 before exporting."
        _export.to_csv(_crime_path, index=False)
        _crime_path.with_suffix(".csv.source.txt").write_text(
            "Source: https://data.cityofchicago.org/d/ijzp-q8t2\n"
            f"Website export: {_export_path.name}; Year = 2025\n"
            f"Imported UTC: {datetime.now(timezone.utc).isoformat()}\n"
        )
    _query = urlencode({
        "$select": "id,date,primary_type,description,district,latitude,longitude",
        "$where": "date >= '2025-01-01T00:00:00' AND date < '2026-01-01T00:00:00'",
        "$order": "id",
        "$limit": 250000,
    })
    _sources = {
        "chicago_2025.csv": "https://data.cityofchicago.org/resource/ijzp-q8t2.csv?" + _query,
        "chicago_boundary.geojson": "https://data.cityofchicago.org/api/geospatial/qqq8-j68g?method=export&format=GeoJSON",
    }
    # Reuse cached files so each comparison uses the same data snapshot.
    for _name, _url in _sources.items():
        _path = Path("data") / _name
        if not _path.exists():
            with urlopen(_url, timeout=120) as _response:
                _contents = _response.read()
            _path.write_bytes(_contents)
            _path.with_suffix(_path.suffix + ".source.txt").write_text(
                f"Source: {_url}\nRetrieved UTC: {datetime.now(timezone.utc).isoformat()}\n"
            )
    csv_path = "data/chicago_2025.csv"
    boundary_path = "data/chicago_boundary.geojson"
    print("Using cached files:", csv_path, boundary_path)
    return boundary_path, csv_path


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## B1. Audit the extract with DuckDB

    Inspect schema, date coverage, missing coordinates, and duplicate IDs before exclusions.
    We read text and convert explicitly so bad values remain countable.
    `source_audit` covers all 2025 and supplies Task 1's annual burglary count.
    `category_audit` covers January–November training records only.

    Review [A1](#a1-eda-begins-with-questions-about-the-records) and
    [A2](#a2-time-denominators-and-misleading-summaries) · [Notes: file audit](https://github.com/thibaud-c/GST.200UB/blob/main/lab_02/notes.md#b1).
    """)
    return


@app.cell
def _(csv_path, mo):
    source_audit = mo.sql(
        f"""
        -- This annual audit includes December; the EDA query below excludes it.
        SELECT COUNT(*) AS rows, COUNT(DISTINCT id) AS distinct_ids,
               COUNT(*) FILTER (WHERE primary_type = 'BURGLARY') AS burglary_records,
               MIN(TRY_CAST(date AS TIMESTAMP)) AS first_date,
               MAX(TRY_CAST(date AS TIMESTAMP)) AS last_date,
               COUNT(*) - COUNT(TRY_CAST(date AS TIMESTAMP)) AS bad_dates,
               COUNT(*) FILTER (WHERE TRY_CAST(latitude AS DOUBLE) IS NULL
                                   OR TRY_CAST(longitude AS DOUBLE) IS NULL) AS missing_coordinates
        FROM read_csv('{csv_path}', all_varchar=true)
        """
    )
    return (source_audit,)


@app.cell
def _(pd, source_audit):
    _summary = source_audit.iloc[0]
    assert 0 < _summary["rows"] < 250000, "Empty extract or API cap reached: obtain a complete snapshot."
    assert _summary["rows"] == _summary["distinct_ids"], "Investigate repeated IDs before proceeding."
    assert _summary["bad_dates"] == 0, "Investigate unusable dates before splitting by time."
    assert pd.Timestamp(_summary["first_date"]).normalize() == pd.Timestamp("2025-01-01"), "The annual snapshot must start on 1 January 2025."
    assert pd.Timestamp(_summary["last_date"]).normalize() == pd.Timestamp("2025-12-31"), "The annual snapshot must include 31 December 2025; check the filename and source notes."
    print("Annual extract, unique-ID, and date-coverage checks passed.")
    return


@app.cell
def _(csv_path, mo):
    category_audit = mo.sql(
        f"""
        -- Explore January-November only, before looking at December patterns.
        SELECT primary_type, COUNT(*) AS records,
               COUNT(*) FILTER (WHERE TRY_CAST(latitude AS DOUBLE) IS NULL
                                   OR TRY_CAST(longitude AS DOUBLE) IS NULL) AS missing_coordinates,
               ROUND(100.0 * missing_coordinates / COUNT(*), 2) AS missing_pct
        FROM read_csv('{csv_path}', all_varchar=true)
        WHERE TRY_CAST(date AS TIMESTAMP) >= TIMESTAMP '2025-01-01'
          AND TRY_CAST(date AS TIMESTAMP) < TIMESTAMP '2025-12-01'
        GROUP BY primary_type
        ORDER BY records DESC
        """
    )
    return (category_audit,)


@app.cell
def _(category_audit, px):
    px.bar(category_audit, x="records", y="primary_type", height=850,
           labels={"primary_type": "Recorded category", "records": "Training-period records"},
           hover_data=["missing_coordinates", "missing_pct"],
           title="January–November 2025: categories before coordinate exclusions").update_yaxes(
               categoryorder="total ascending"
           )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Which categories dominate, and which have the largest missing-coordinate percentage?

    Add a SQL calendar query for daily BURGLARY counts across all 334 January–November days,
    then a Plotly chart. Its total should match `category_audit`'s BURGLARY count.
    Keep December patterns hidden. Add one observation, possible explanation, and check you would need.
    Use [A2's calendar example](#a2-time-denominators-and-misleading-summaries).
    """)
    return


@app.cell
def _():
    # Add your daily training-count SQL cell and Plotly chart here.
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Task 1. Select the analysis records in SQL

    Replace the next SQL cell.

    - Read the annual file at `csv_path`; keep output name `selected_records`.
    - Keep only BURGLARY in **all of 2025**, from 2025-01-01 inclusive to 2026-01-01 exclusive.
    - Return integer `id`, timestamp `occurred_at` from `date`, `primary_type`,
      and double `latitude`/`longitude`. Use `TRY_CAST`.
    - Keep missing coordinates for Task 2; do not use `LIMIT`. Order by `id`.
    - Compare the output count with `source_audit`'s annual `burglary_records` count.

    Review [A1](#a1-eda-begins-with-questions-about-the-records) and
    [A3](#a3-clean-deliberately-and-keep-future-records-separate) · [Notes](https://github.com/thibaud-c/GST.200UB/blob/main/lab_02/notes.md#task-1).
    """)
    return


@app.cell
def _(mo):
    selected_records = mo.sql(
        f"""
        -- Read the annual file, filter 2025 BURGLARY, and return five typed columns.
        -- Keep missing coordinates and all matching rows; order by id.
        SELECT 'Replace this with your filtered query' AS instruction
        """
    )
    return (selected_records,)


@app.cell(hide_code=True)
def _(mo, pd, selected_records, source_audit):
    selection_ok = False
    try:
        _required = {"id", "occurred_at", "primary_type", "latitude", "longitude"}
        assert _required.issubset(selected_records.columns), "Return the five requested columns."
        selected_df = selected_records.copy()
        assert not selected_df.empty, "Your query returned no records."
        _expected = int(source_audit["burglary_records"].iloc[0])
        assert len(selected_df) == _expected, f"Expected {_expected} 2025 burglaries, including missing coordinates. Check the year and remove LIMIT."
        assert selected_df["id"].is_unique, "Keep each source ID once."
        assert selected_df["primary_type"].eq("BURGLARY").all(), "Select only BURGLARY."
        assert pd.api.types.is_integer_dtype(selected_df["id"]), "Cast id to an integer."
        for _column in ["latitude", "longitude"]:
            assert pd.api.types.is_numeric_dtype(selected_df[_column]), "Cast coordinates to DOUBLE."
        assert pd.api.types.is_datetime64_any_dtype(selected_df["occurred_at"]), "Cast date to TIMESTAMP."
        assert selected_df["occurred_at"].between("2025-01-01", "2026-01-01", inclusive="left").all(), "Use the specified date window."
        selection_ok = True
        _message = f"**Tests passed.** {len(selected_df)} selected records. Check the query has no LIMIT and retains missing coordinates."
    except AssertionError as _error:
        selected_df = None
        _message = f"**Test failed:** {_error}"
    mo.md(_message)
    return selected_df, selection_ok


@app.cell
def _(boundary_path, gpd):
    # Estimate a local metric CRS from the city, then combine its boundary polygons.
    city_boundary = gpd.read_file(boundary_path)
    _city_metric_crs = city_boundary.estimate_utm_crs()
    city_boundary = city_boundary.to_crs(_city_metric_crs).dissolve()
    assert city_boundary.geometry.is_valid.all(), "Inspect the boundary before proceeding."
    print("Study area (km²):", city_boundary.geometry.area.sum() / 1_000_000)
    city_boundary
    return (city_boundary,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Task 2. Prepare points and account for exclusions

    Write `prepare_points(records, boundary)`.

    - Exclude missing/out-of-range coordinates and keep one row per ID.
    - Create EPSG:4326 points, project to the boundary's metric CRS, and keep
      points intersecting the boundary.
    - Return a GeoDataFrame retaining input attributes. Keep the boundary fixed.
    - Show an audit for training and test: input, retained, missing/invalid coordinates,
      duplicate IDs, and outside-boundary rows. Assign one reason per excluded row.

    Use [A4's exclusion audit](#count-exclusions-by-period) for the last step.
    Review [A3](#a3-clean-deliberately-and-keep-future-records-separate) and
    [A4](#a4-geometry-distances-and-a-fixed-study-area) · [Notes](https://github.com/thibaud-c/GST.200UB/blob/main/lab_02/notes.md#task-2).
    """)
    return


@app.function
def prepare_points(records, boundary):
    # - Check coordinates and duplicate IDs.
    # - Create points, project, and filter against the boundary.
    # - Return the GeoDataFrame with its original attributes.
    # - Show exclusions by training/test period in an audit table.
    return None


@app.cell(hide_code=True)
def _(box, city_boundary, gpd, mo, pd, selected_df, selection_ok):
    mo.stop(not selection_ok, mo.md("Complete Task 1 before preparing Chicago points."))
    crime_points = prepare_points(selected_df, city_boundary)
    points_ok = False
    try:
        assert isinstance(crime_points, gpd.GeoDataFrame), "Return a GeoDataFrame."
        assert not crime_points.empty and crime_points.crs == city_boundary.crs, "Return non-empty points in the boundary's metric CRS."
        assert crime_points.geom_type.eq("Point").all(), "Create point geometries."
        assert crime_points["id"].is_unique, "Keep one row per incident ID."
        assert set(selected_df.columns).issubset(crime_points.columns), "Retain the input attributes."
        assert crime_points.intersects(city_boundary.geometry.union_all()).all(), "Exclude points outside the study area."
        assert set(crime_points["id"]).issubset(selected_df["id"]), "Preserve the input IDs."
        _probe = pd.DataFrame({
            "id": [1, 1, 2, 3, 4],
            "occurred_at": pd.to_datetime(["2025-01-01"] * 3 + ["2025-12-01"] * 2),
            "longitude": [-87.63, -87.63, None, 0, -87.64],
            "latitude": [41.88, 41.88, 41.88, 0, 999],
        })
        _probe_boundary = gpd.GeoDataFrame(geometry=[box(-87.7, 41.8, -87.5, 42.0)], crs=4326).to_crs(city_boundary.crs)
        _probe_result = prepare_points(_probe, _probe_boundary)
        assert _probe_result["id"].tolist() == [1], "Small check: retain ID 1 once; remove missing, outside, and invalid coordinates."
        points_ok = True
        _message = f"**Tests passed.** Retained {len(crime_points)} of {len(selected_df)} records; explain the exclusions."
    except AssertionError as _error:
        _message = f"**Test failed:** {_error}"
    mo.md(_message)
    return crime_points, points_ok


@app.cell
def _(crime_points, mo, points_ok):
    mo.stop(not points_ok, mo.md("Complete Task 2 before splitting the records."))
    # Task 1 kept all of 2025; this split keeps December out of training.
    train = crime_points.loc[
        crime_points["occurred_at"].between("2025-01-01", "2025-12-01", inclusive="left")
    ].copy()
    test = crime_points.loc[
        crime_points["occurred_at"].between("2025-12-01", "2026-01-01", inclusive="left")
    ].copy()
    assert not train.empty and not test.empty, "Check the extract and exclusions."
    assert len(train) + len(test) == len(crime_points), "Keep only 2025 records."
    assert set(train["id"]).isdisjoint(test["id"])
    assert train["occurred_at"].max() < test["occurred_at"].min()
    print("January–November training:", len(train), "December test:", len(test))
    return test, train


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Inspect training geography before choosing hotspots

    Map `train` against the city outline. After building the grid, inspect its count histogram,
    mean, median, zero cells, and repeated coordinates.

    Freeze H3 resolution 8 with a 10% area budget and DBSCAN `eps=500` m, `min_samples=10`
    before viewing December patterns. These are course settings, not optimal estimates.

    Review [A3](#a3-clean-deliberately-and-keep-future-records-separate) and
    [A5](#a5-h3-and-discrete-global-grids) · [Notes: validation options](https://github.com/thibaud-c/GST.200UB/blob/main/lab_02/notes.md#training-geography).
    """)
    return


@app.cell
def _(city_boundary, make_grid):
    # Include every city cell, including places with no training records.
    chicago_grid = make_grid(city_boundary, 8)
    print("Grid cells, including zeros:", len(chicago_grid))
    chicago_grid.head()
    return (chicago_grid,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Task 3. Build H3 hotspots from training points

    Write `h3_hotspots(points, grid, area_budget)`.

    - Transform points to EPSG:4326 and assign resolution-8 H3 IDs.
    - Map counts onto a copy of the full grid, including zero cells.
    - Calculate density using clipped metric areas; inspect small edge cells.
    - Sort density descending, then H3 ID ascending. Keep the positive-count prefix
      with cumulative area at most `area_budget`.
    - Return selected rows with `h3_id`, `count`, and metric geometry, including an empty selection.

    Review [A5](#a5-h3-and-discrete-global-grids) · [Notes](https://github.com/thibaud-c/GST.200UB/blob/main/lab_02/notes.md#task-3).
    """)
    return


@app.function
def h3_hotspots(points, grid, area_budget):
    # - Assign H3 IDs and count training points on the full grid.
    # - Calculate density and rank cells within the area budget.
    # - Return h3_id, count, and geometry in the grid CRS.
    return None


@app.cell(hide_code=True)
def _(chicago_grid, city_boundary, gpd, h3, mo, pd, train):
    h3_zones = h3_hotspots(train, chicago_grid, 0.1 * city_boundary.geometry.area.sum())
    h3_ok = False
    try:
        assert isinstance(h3_zones, gpd.GeoDataFrame), "Return a GeoDataFrame, including for an empty selection."
        assert {"h3_id", "count"}.issubset(h3_zones.columns), "Keep h3_id and count."
        assert h3_zones.crs == chicago_grid.crs, "Keep the metric CRS."
        assert h3_zones["h3_id"].is_unique, "Return each cell once."
        assert set(h3_zones["h3_id"]).issubset(chicago_grid["h3_id"]), "Select from the supplied grid."
        assert h3_zones["count"].gt(0).all(), "Select positive-count cells only."
        assert h3_zones.geometry.area.sum() <= 0.1 * city_boundary.geometry.area.sum() + 0.01, "Do not exceed the area budget."
        _wgs = train.to_crs(4326)
        _cell_ids = []
        for _point in _wgs.geometry:
            _cell_ids.append(h3.latlng_to_cell(_point.y, _point.x, 8))
        _counts = pd.Series(_cell_ids).value_counts()
        assert set(_counts.index).issubset(chicago_grid["h3_id"]), "The grid must cover every training point."
        assert h3_zones["count"].tolist() == h3_zones["h3_id"].map(_counts).tolist(), "Check counts against training records."
        _reference = chicago_grid.set_index("h3_id").loc[h3_zones["h3_id"]]
        assert h3_zones.geometry.reset_index(drop=True).geom_equals(_reference.geometry.reset_index(drop=True)).all(), "Keep the supplied clipped grid geometries."
        h3_ok = True
        _message = f"**Tests passed.** Selected {len(h3_zones)} cells. Review the density ranking and tie rule."
    except AssertionError as _error:
        _message = f"**Test failed:** {_error}"
    mo.md(_message)
    return h3_ok, h3_zones


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Task 4. Turn DBSCAN clusters into hotspot polygons

    Write `dbscan_hotspots(points, eps_m, min_samples)`.

    - Fit DBSCAN to projected training x/y using the supplied settings.
    - Exclude noise label -1; make one convex hull per cluster and discard zero-area hulls.
    - Return `cluster_id`, `n_points`, and `geometry` in a GeoDataFrame with the input CRS.
      If no hull remains, keep these columns, the active geometry, and the CRS in an empty table.
    - Print noise and discarded zero-area hull counts.
    - Test on the seven-point example first. Do not use test points or buffer zero-area hulls.

    Review [A6](#a6-dbscan-density-connected-points) · [Notes](https://github.com/thibaud-c/GST.200UB/blob/main/lab_02/notes.md#task-4).
    """)
    return


@app.function
def dbscan_hotspots(points, eps_m, min_samples):
    # - Cluster projected training points; exclude noise.
    # - Build positive-area hulls and record cluster_id and n_points.
    # - Keep the output columns and CRS even when no hull remains.
    # - Print noise and zero-area hull counts; return a GeoDataFrame.
    return None


@app.cell(hide_code=True)
def _(demo_points, gpd, mo):
    db_ok = False
    try:
        _small = dbscan_hotspots(demo_points, 50, 3)
        assert isinstance(_small, gpd.GeoDataFrame), "Return a GeoDataFrame."
        assert {"cluster_id", "n_points"}.issubset(_small.columns), "Keep cluster_id and n_points."
        assert len(_small) == 2 and sorted(_small["n_points"]) == [3, 3], "Expect two three-point clusters."
        assert _small.crs == demo_points.crs and _small.geometry.area.gt(0).all(), "Keep positive-area metric polygons."
        assert _small["cluster_id"].ne(-1).all(), "Exclude noise."
        _empty = dbscan_hotspots(demo_points, 1, 3)
        assert isinstance(_empty, gpd.GeoDataFrame) and _empty.empty, "Return an empty GeoDataFrame when every point is noise."
        assert {"cluster_id", "n_points", "geometry"}.issubset(_empty.columns), "Keep the result columns even when the table is empty."
        assert _empty.crs == demo_points.crs and _empty.geometry.name == "geometry", "Keep the CRS and active geometry on empty results."
        db_ok = True
        _message = "**Tests passed:** two clusters at 50 m, empty output at 1 m."
    except AssertionError as _error:
        _message = f"**Test failed:** {_error}"
    mo.md(_message)
    return (db_ok,)


@app.cell
def _(db_ok, mo, train):
    mo.stop(not db_ok, mo.md("Complete Task 4's small checks before fitting Chicago."))
    db_zones = dbscan_hotspots(train, 500, 10)
    print("Chicago cluster hulls:", len(db_zones))
    db_zones
    return (db_zones,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Task 5. Calculate and interpret PAI

    Write `compute_pai(hits, total, hotspot_area, study_area)`.

    - Check for a zero test count, hotspot area, or study area before dividing; return `None`.
    - Otherwise return the PAI formula from A7. Zero hits with valid denominators gives 0.
    - Use the same units for both areas; inputs here are non-negative.
    - Run the ordinary, zero-hit, and undefined-case checks below.

    Review [A7](#a7-pai-distinguish-hits-from-area-covered) and
    [A4](#a4-geometry-distances-and-a-fixed-study-area) · [Notes](https://github.com/thibaud-c/GST.200UB/blob/main/lab_02/notes.md#task-5).
    """)
    return


@app.function
def compute_pai(hits, total, hotspot_area, study_area):
    # - Guard the undefined cases before dividing.
    # - Return PAI for valid inputs, including zero hits.
    return None


@app.cell(hide_code=True)
def _(mo):
    pai_ok = False
    try:
        assert compute_pai(20, 100, 10, 100) == 2, "20% hits in 10% area gives PAI 2."
        assert compute_pai(40, 100, 25, 100) == 1.6, "40% hits in 25% area gives PAI 1.6."
        assert compute_pai(100, 100, 100, 100) == 1, "The whole-study-area baseline is 1."
        assert compute_pai(0, 100, 10, 100) == 0, "Zero hits can give a defined PAI of zero."
        assert compute_pai(0, 0, 10, 100) is None, "No test records means undefined PAI."
        assert compute_pai(0, 100, 0, 100) is None, "No hotspot area means undefined PAI."
        assert compute_pai(0, 100, 10, 0) is None, "No study area means undefined PAI."
        pai_ok = True
        _message = "**Tests passed:** ordinary cases, whole-area baseline, zero hits, and undefined denominators."
    except AssertionError as _error:
        _message = f"**Test failed:** {_error}"
    mo.md(_message)
    return (pai_ok,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The shared evaluation unions and clips both methods identically. Their covered areas differ,
    so compare hits and area alongside PAI. The whole-city baseline has PAI 1 and 100% hit rate.
    """)
    return


@app.cell
def _(city_boundary, db_ok, db_zones, h3_ok, h3_zones, mo, pai_ok, pd, test):
    mo.stop(not (h3_ok and db_ok and pai_ok), mo.md("Complete Tasks 3–5 before evaluating December."))
    # Evaluate both methods on the same December records and fixed city boundary.
    _study = city_boundary.geometry.union_all()
    _results = []
    for _name, _zones in [("H3", h3_zones), ("DBSCAN hulls", db_zones), ("Whole city", city_boundary)]:
        _hotspot = _zones.geometry.union_all().intersection(_study)
        _hits = int(test.intersects(_hotspot).sum())
        _results.append({
            "method": _name, "hits": _hits, "test_records": len(test),
            "hit_rate": _hits / len(test), "hotspot_km2": _hotspot.area / 1_000_000,
            "area_fraction": _hotspot.area / _study.area,
            "PAI": compute_pai(_hits, len(test), _hotspot.area, _study.area),
        })
    results = pd.DataFrame(_results)
    assert abs(results.loc[results["method"] == "Whole city", "PAI"].iloc[0] - 1) < 1e-9
    results
    return (results,)


@app.cell
def _(px, results):
    px.scatter(results, x="area_fraction", y="hit_rate", text="method",
               hover_data=["hits", "test_records", "hotspot_km2", "PAI"],
               labels={"area_fraction": "Fraction of city covered", "hit_rate": "Fraction of December records captured"},
               title="Read coverage and captured incidents together")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Task 6. Inspect maps and challenge your conclusion

    Build your Chicago map.

    - Centre Leafmap Kepler at `[41.88, -87.63]`, zoom 10.
    - Add the city outline, H3 hotspots, and DBSCAN hulls in EPSG:4326.
      Omit `h3_id` from the display copy.
    - Freeze method settings before adding December points; inspect missed incidents.
    - Label periods, category, and sources; use clear layer names and transparency.
    - Display the map in marimo and answer the reflection questions below.

    Review [A8](#a8-explore-with-leafmaps-kepler-backend),
    [A2](#a2-time-denominators-and-misleading-summaries), and
    [A7](#a7-pai-distinguish-hits-from-area-covered) · [Notes](https://github.com/thibaud-c/GST.200UB/blob/main/lab_02/notes.md#task-6).
    """)
    return


@app.cell
def _():
    # - Build a Kepler map with the three EPSG:4326 layers.
    # - Add December points only after freezing the methods.
    # - Label the map and display it here, following A8.
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Reflect

    Beside your outputs, explain:

    - Did exclusions differ between periods?
    - Which method caught more incidents, and which used less area?
    - Why do zero cells and DBSCAN noise tell us nothing certain about safety?
    - What did EDA change in your initial proposal?

    These maps describe recorded patterns, not causes or evidence for targeting people.
    [Further questions, extensions, and documentation](https://github.com/thibaud-c/GST.200UB/blob/main/lab_02/notes.md#reflection).
    """)
    return


if __name__ == "__main__":
    app.run()
