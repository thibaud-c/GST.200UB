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
    import leafmap.kepler as leafmap
    import matplotlib.pyplot as plt
    from sklearn.cluster import DBSCAN
    from shapely.geometry import box

    return DBSCAN, box, gpd, h3, leafmap, mo, pd, plt, px


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Lab 02 live demo: inspect, cluster, evaluate
    """)
    return


@app.cell
def _(pd):
    records = pd.DataFrame([
        (1, "2025-01-01", "BURGLARY", -87.6300, 41.8800),
        (2, "2025-01-02", "BURGLARY", -87.6296, 41.8800),
        (3, "2025-01-03", "BURGLARY", -87.6298, 41.8804),
        (4, "2025-02-01", "BURGLARY", -87.6200, 41.8900),
        (5, "2025-02-02", "BURGLARY", -87.6196, 41.8900),
        (6, "2025-02-03", "BURGLARY", -87.6198, 41.8904),
        (7, "2025-02-04", "BURGLARY", -87.6260, 41.8730),
        (8, "2025-12-01", "BURGLARY", -87.6298, 41.8801),
        (9, "2025-12-02", "BURGLARY", -87.6198, 41.8901),
        (10, "2025-12-03", "BURGLARY", -87.6250, 41.8800),
        (11, "2025-12-04", "BURGLARY", -87.6320, 41.8950),
        (2, "2025-01-02", "BURGLARY", -87.6296, 41.8800),
        (12, "2025-01-04", "BURGLARY", -87.6300, None),
        (13, "bad date", "BURGLARY", -87.6300, 41.8800),
        (14, "2025-01-05", "THEFT", -87.6300, 41.8800),
    ], columns=["id", "date", "primary_type", "longitude", "latitude"])
    records
    return (records,)


@app.cell
def _(records):
    records.plot.scatter(x="longitude", y="latitude", figsize=(10, 10))
    return


@app.cell
def _(mo):
    test_fun = mo.sql(
        f"""
        SELECT COUNT(*) AS rows,
               COUNT(DISTINCT id) AS distinct_ids,
               COUNT(*) - COUNT(latitude) AS missing_latitudes,
               COUNT(*) - COUNT(TRY_CAST(date AS DATE)) AS unusable_dates
        FROM records
        """
    )
    return


@app.cell
def _(mo):
    selected = mo.sql(
        f"""
        SELECT DISTINCT id, TRY_CAST(date AS DATE) AS date, longitude, latitude
        FROM records
        WHERE primary_type = 'BURGLARY'
          AND TRY_CAST(date AS DATE) >= DATE '2025-01-01'
          AND TRY_CAST(date AS DATE) < DATE '2026-01-01'
          AND longitude BETWEEN -87.64 AND -87.60
          AND latitude BETWEEN 41.87 AND 41.90
        ORDER BY date, id
        """
    )
    return (selected,)


@app.cell
def _(box, gpd, selected):
    # First describe longitude/latitude coordinates, then transform them into metres.
    points_wgs84 = gpd.GeoDataFrame(
        selected,
        geometry=gpd.points_from_xy(selected["longitude"], selected["latitude"]),
        crs=4326,
    )
    _metric_crs = points_wgs84.estimate_utm_crs()
    points = points_wgs84.to_crs(_metric_crs)
    study_area = gpd.GeoDataFrame(
        geometry=[box(-87.64, 41.87, -87.60, 41.90)], crs=4326,
    ).to_crs(_metric_crs)
    # December is held out; only earlier points can build our hotspots.
    train = points.loc[points["date"] < "2025-12-01"].copy()
    test = points.loc[points["date"] >= "2025-12-01"].copy()
    assert len(train) == 7 and len(test) == 4
    print("Training records:", len(train), "December records held out:", len(test))
    train
    return (train,)


@app.cell
def _(h3, px, train):
    def assign_h3_cell(row):
        # These original coordinate columns are still in degrees after projection.
        latitude = row["latitude"]
        longitude = row["longitude"]
        return h3.latlng_to_cell(latitude, longitude, 9)

    h3_training = train.copy()
    # axis=1 passes one row at a time to our function; H3 takes latitude first.
    h3_training["h3_cell"] = h3_training.apply(assign_h3_cell, axis=1)

    # Count rows in each cell, then turn the result into a table for plotting.
    h3_counts = h3_training.groupby("h3_cell").size()
    h3_counts = h3_counts.reset_index(name="incidents")
    assert h3_counts["incidents"].sum() == len(train)
    px.bar(h3_counts, x="h3_cell", y="incidents", title="Training incidents per occupied H3 cell")
    return (h3_counts,)


@app.cell
def _(h3_counts, leafmap):
    map = leafmap.Map()
    map.add_df(h3_counts)
    map#.to_html("demo.html")
    return


@app.cell
def _(DBSCAN, gpd, pd, plt, train):
    clusters = train.copy()
    # DBSCAN needs projected x/y coordinates so its distance setting is in metres.
    _coordinates = pd.DataFrame({"x": clusters.geometry.x, "y": clusters.geometry.y})
    clusters["cluster"] = DBSCAN(eps=100, min_samples=3).fit_predict(_coordinates)

    _hulls = []
    for _label, _group in clusters.groupby("cluster"):
        if _label == -1:
            continue  # -1 means noise, so it does not get a hotspot polygon.
        _hull = _group.geometry.union_all().convex_hull
        if _hull.area > 0:
            _hulls.append(_hull)
    hotspots = gpd.GeoDataFrame(
        geometry=_hulls, crs=train.crs,
    )
    print(clusters["cluster"].value_counts().sort_index())
    _fig, _ax = plt.subplots(figsize=(10, 10))
    if not hotspots.empty:
        hotspots.plot(ax=_ax, color="orange", alpha=0.5)
    clusters.plot(ax=_ax, s=10, column="cluster", categorical=True, legend=True)
    _ax.set_title("Training clusters; -1 is noise")
    _ax.set_axis_off()
    _fig
    return


if __name__ == "__main__":
    app.run()
