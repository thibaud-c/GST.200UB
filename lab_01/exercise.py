import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import geopandas as gpd
    import pandas as pd
    import osmnx as ox
    import matplotlib.pyplot as plt
    import leafmap.kepler as leafmap
    from shapely.geometry import Point, box

    return Point, box, gpd, leafmap, mo, ox, pd, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Lab 01: average distance to a BILLA in Graz

    How far is a location in Graz from its nearest BILLA? Your task is to
    estimate an average distance and explain what that number represents.
    At home, repeat the analysis for the SPAR family.

    ## First, propose a method

    Look at the picture in [Arthur A.'s LinkedIn post about distances to Migros
    in Switzerland](https://www.linkedin.com/posts/carbonateturi_you-are-on-average-only-78-km-away-from-activity-7234914074541633536-m11_/).
    Spend five minutes on these questions before scrolling to Part A:

    - Which data would you need to reproduce a similar picture for Graz?
    - What might its colours and shapes represent? Check your reading against the legend.
    - How could you turn a map like this into one average distance?
    - Average over what: stores, locations, or something else? Would those give the same answer?
    - Which assumptions would you need to ask the author about?

    Add a Markdown cell with a short proposal or sketch it on paper. Compare
    ideas with a neighbour. Keep your first proposal to revisit after the exercise.

    ## Before starting

    If there are course updates, save your work and run `git pull`, then `uv sync`,
    in a separate terminal in the course folder. See the
    [Git tutorial](https://github.com/thibaud-c/GST.200UB/blob/main/tutorials/04_git.md)
    if you need help preserving edits or resolving conflicts.
    Open this file as a marimo notebook in VS Code and select the course `.venv`.

    Part A is a worked tutorial. Run it and explore the results. Part B is your
    exercise. Complete the function bodies and run the following test cells.
    `return None` marks an unfinished function; replace it with your own code.
    Tests show **passed**, **failed**, or which earlier task needs completing.

    ## Quick reference

    | Operation | Use | Documentation |
    | --- | --- | --- |
    | `ox.geocode_to_gdf(place)` | Find a place boundary | [OSMnx geocoder](https://osmnx.readthedocs.io/en/stable/user-reference.html#osmnx.geocoder.geocode_to_gdf) |
    | `ox.features_from_polygon(polygon, tags)` | Query OSM features | [OSMnx features](https://osmnx.readthedocs.io/en/stable/user-reference.html#osmnx.features.features_from_polygon) |
    | `data.head()`, `data.columns` | Explore a table | [GeoPandas introduction](https://geopandas.org/en/stable/getting_started/introduction.html) |
    | `data.crs`, `data.to_crs(32633)` | Inspect or transform the CRS | [Projection](https://geopandas.org/en/stable/docs/user_guide/projections.html) |
    | `data.geometry.representative_point()` | One interior point per feature | [Geometry operations](https://geopandas.org/en/stable/docs/user_guide/geometric_manipulations.html) |
    | `data.loc[mask].copy()` | Select matching rows | [Indexing](https://pandas.pydata.org/docs/user_guide/indexing.html) |
    | `data.buffer(radius_m)` | Create distance buffers | [Buffer](https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoSeries.buffer.html) |
    | `data.dissolve()` | Merge overlapping areas | [Dissolve](https://geopandas.org/en/stable/docs/user_guide/aggregation_with_dissolve.html) |
    | `gpd.clip(data, city)` | Keep areas inside the city | [Clip](https://geopandas.org/en/stable/docs/user_guide/clip.html) |
    | `data.geometry.area` | Measure area in squared CRS units | [Area](https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoSeries.area.html) |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Part A. Try the chosen approach

    **After writing your proposal:** for this exercise, we average across Graz's
    area. We will create several distance buffers around BILLA locations, merge
    overlaps, clip to the city, and use the resulting bands to approximate distance.
    Larger bands contribute more because they cover more land. Part A explains
    each operation before you apply it yourself in Part B.

    This is our adaptation of last year's exercise, rather than a reconstruction
    of every decision behind the post. Keep asking how projection, store location,
    city boundaries, and approximation affect the result.

    ## A1. Query OpenStreetMap with OSMnx

    You have used tags in Overpass Turbo. OSMnx lets Python send similar feature
    requests and returns a GeoDataFrame: a table with geometry and a CRS.
    A tag is a key and value, such as `amenity=cafe`. A Python dictionary writes
    that pair as `{"amenity": "cafe"}`. You can read more about osm tags: [here](https://wiki.openstreetmap.org/wiki/Tags).

    Run these cells. The first gets Salzburg's boundary as a worked example. The second asks for cafés
    in a small box in Graz. In Task 1 you will query Graz’s city boundary yourself.
    These are live service requests;
    allow them to finish before running again. OSMnx caches responses locally.
    """)
    return


@app.cell
def _(ox):
    ox.settings.use_cache = True
    ox.settings.cache_folder = "data/osmnx_cache"
    example_boundary = ox.geocode_to_gdf("Salzburg, Austria")
    example_boundary[["display_name", "geometry"]]
    return


@app.cell
def _(ox):
    cafes = ox.features_from_point(
        (47.070, 15.440), tags={"amenity": "cafe"}, dist=300
    )
    cafes.head()
    return (cafes,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The centre uses **latitude, longitude**, as specified by OSMnx.
    `dist=300` sets the search box size in metres. It is not a 300-metre walking route.
    For a city-wide question, `features_from_polygon` takes a boundary geometry
    in EPSG:4326 instead of a centre point.

    Run the exploration cell below. Try `cafes.columns.tolist()` and inspect
    `cafes[["name", "geometry"]].head()` too. Which details are missing? What
    would you check in Overpass Turbo or on the OSM map?

    OSMnx's feature index contains an element type and OSM ID. A node may be a
    point; a way or relation may be a footprint. Multiple tag keys select the
    **union** of matching features, not only features satisfying every key.
    For example, adding `shop=supermarket` to the café query would retrieve
    cafés **or** supermarkets. Query one feature type, then filter its attributes.
    """)
    return


@app.cell
def _(cafes):
    print(cafes.crs)
    print(cafes.geom_type.value_counts())
    print(cafes.index.names)
    cafes.isna().sum().sort_values(ascending=False).head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A2. Explore and prepare a small GeoDataFrame

    This small table contains points, a footprint polygon, and one missing brand. The coordinates
    are already in metres in EPSG:32633, a suitable UTM CRS for Graz.

    For real OSM data, use `.to_crs(32633)` before measuring distance. Do not
    use `.set_crs()` to convert coordinates: that changes the label only.
    """)
    return


@app.cell
def _(Point, box, gpd):
    toy_shops = gpd.GeoDataFrame(
        {"brand": ["Example", "EXAMPLE", "Other", None]},
        geometry=[
            Point(500100, 5210100),
            box(500250, 5210200, 500300, 5210250),
            Point(500700, 5210600),
            Point(500800, 5210800),
        ],
        crs=32633,
    )
    toy_city = gpd.GeoDataFrame(
        geometry=[box(500000, 5210000, 501000, 5211000)], crs=32633
    )
    toy_shops
    return toy_city, toy_shops


@app.cell
def _(toy_city, toy_shops):
    print(toy_shops.geom_type.value_counts())
    print(toy_shops["brand"].value_counts(dropna=False))
    print(toy_city.geometry.area.sum())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Expect three points, one polygon, and a city area of 1,000,000 m².
    `.value_counts(dropna=False)` includes missing values. Never assume every
    OSM store has a `brand` tag.

    An interior representative point gives each feature a comparable location.
    It is not necessarily a shop entrance, and converting geometry does not
    remove duplicate records. `.copy()` keeps the original table available.
    """)
    return


@app.cell
def _(toy_shops):
    toy_points = toy_shops.copy()
    toy_points["geometry"] = toy_shops.geometry.representative_point()
    toy_mask = toy_points["brand"].str.contains(
        "example", case=False, na=False, regex=False
    )
    toy_selected = toy_points.loc[toy_mask].copy()
    toy_selected
    return (toy_selected,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Expect two selected points. `case=False` ignores capitalisation; `na=False`
    excludes missing brands; `regex=False` searches literal text. Change the
    search to `other`, predict the result, then restore `example`.

    ## A3. Buffer, merge, and clip

    A buffer contains locations within a given straight-line distance of a point.
    Merge overlaps before measuring area, then clip to the study boundary.
    Otherwise you can count an overlap twice or include area outside the city.
    """)
    return


@app.cell
def _(gpd, toy_city, toy_selected):
    toy_buffers = gpd.GeoDataFrame(
        geometry=toy_selected.buffer(200), crs=toy_selected.crs
    )
    toy_union = toy_buffers.dissolve()
    toy_clipped = gpd.clip(toy_union, toy_city)
    print(f"Separate buffer areas: {toy_buffers.geometry.area.sum():.0f} m²")
    print(f"Merged and clipped area: {toy_clipped.geometry.area.sum():.0f} m²")
    toy_clipped
    return (toy_clipped,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Inspect the result with Matplotlib

    `plt.subplots` creates a figure and axes. Use the same axes for each layer.
    Draw points last so they remain visible. The last expression displays the figure.
    """)
    return


@app.cell
def _(plt, toy_city, toy_clipped, toy_selected):
    _fig, _ax = plt.subplots(figsize=(6, 6))
    toy_city.boundary.plot(ax=_ax, color="black")
    toy_clipped.plot(ax=_ax, color="steelblue", alpha=0.4)
    toy_selected.plot(ax=_ax, color="darkred", markersize=35)
    _ax.set_title("Fictional stores: 200 m straight-line buffers")
    _ax.set_xlabel("Easting in metres")
    _ax.set_ylabel("Northing in metres")
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Find an overlap and a buffer cut by the city edge. What would happen to the
    area if the two store points were identical?

    ## A4. Repeat for several distances

    Each larger buffer includes the smaller ones. These are **cumulative** areas.
    They must be converted to non-overlapping bands before weighting distances.
    This example uses 100, 200, and 400 metres.
    """)
    return


@app.cell
def _(gpd, toy_city, toy_selected):
    toy_distances = [100, 200, 400]
    toy_geometries = []
    for _radius in toy_distances:
        _buffers = gpd.GeoDataFrame(
            geometry=toy_selected.buffer(_radius), crs=toy_selected.crs
        )
        _clipped = gpd.clip(_buffers.dissolve(), toy_city)
        toy_geometries.append(_clipped.geometry.iloc[0])

    toy_zones = gpd.GeoDataFrame(
        {"distance_m": toy_distances}, geometry=toy_geometries, crs=32633
    )
    toy_zones.assign(area_m2=toy_zones.geometry.area)
    return toy_distances, toy_zones


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Follow one iteration of the loop. `_radius` receives one distance, a buffer
    is made around every selected point, overlaps are merged, and the clipped
    geometry is added to the list. The final table has one row per distance.

    The area within 200 m includes the area within 100 m. Subtract the cumulative
    areas to obtain the area in the 100–200 m band. The last outside area is the
    city area minus the final cumulative area.
    """)
    return


@app.cell
def _(pd, toy_city, toy_distances, toy_zones):
    toy_cumulative = toy_zones.geometry.area.tolist()
    toy_ring_areas = []
    _previous = 0
    for _area in toy_cumulative:
        toy_ring_areas.append(_area - _previous)
        _previous = _area

    toy_outside = toy_city.geometry.area.sum() - toy_cumulative[-1]
    pd.DataFrame({"upper_distance_m": toy_distances, "ring_area_m2": toy_ring_areas})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A5. Calculate an area-weighted average

    Suppose 20% of an area's land lies within 100 m, another 30% lies between
    100 and 200 m, another 30% between 200 and 400 m, and 20% beyond 400 m.
    Use each closed band's midpoint, then choose a representative distance for
    the open-ended outside band:

    | Band | Area weight | Representative distance |
    | --- | --- | --- |
    | 0 to 100 m | 20 | 50 m |
    | 100 to 200 m | 30 | 150 m |
    | 200 to 400 m | 30 | 300 m |
    | Beyond 400 m | 20 | Assumed 600 m |

    Run the calculation. The weights can be areas or percentages as long as the
    denominator uses the same units.
    """)
    return


@app.cell
def _():
    example_weights = [20, 30, 30, 20]
    example_distances = [50, 150, 300, 600]
    example_weighted_sum = 0
    for _weight, _distance in zip(example_weights, example_distances):
        example_weighted_sum += _weight * _distance
    example_mean_m = example_weighted_sum / sum(example_weights)
    example_mean_m
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Expect **265 metres**. `zip` pairs the weights with distances. Try an outside
    distance of 1000 m, then restore 600 m. Why does the estimate change by 80 m?

    For our Graz exercise the closed bands end at 250, 500, 1000, and 2500 m.
    Their midpoints are 125, 375, 750, and 1750 m. We begin with an outside
    assumption of 3000 m, then test alternatives.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(
        mo.md("This is a **band-based estimate**, not an exact mean. Midpoints approximate distances within each band. The distance assigned beyond the final buffer is an assumption. State it beside your result and test how much it matters. We measure straight-line distance to the selected stores inside Graz; stores just outside the boundary are excluded."),
        kind="warn",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A6. Explore multiple layers in Kepler.gl

    The map displays directly in marimo. Use longitude/latitude for this web
    map, while keeping the metric tables for calculations. We use Leafmap’s Kepler
    backend: `add_gdf` adds a GeoDataFrame and printing the map object displays it.
    Leafmap also offers other backends; see the visualization tutorial for tradeoffs.
    """)
    return


@app.cell
def _(leafmap, toy_city, toy_selected, toy_zones):
    toy_map = leafmap.Map(center=[47.045, 15.005], zoom=14, height=500)
    toy_map.add_gdf(toy_selected.to_crs(4326), layer_name="Store points")
    toy_map.add_gdf(toy_zones.to_crs(4326), layer_name="Distance zones")
    toy_map.add_gdf(toy_city.to_crs(4326), layer_name="City boundary")
    toy_map
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In the layer controls, turn off the city fill so it becomes an outline.
    Style `Distance zones` by `distance_m`, with smaller distances lighter.
    Use transparency and inspect the field on hover: the zones overlap because
    they are cumulative. A filter on `distance_m` lets you inspect one threshold.
    Keep the store layer on top and the source attribution visible.

    Documentation: [Leafmap Kepler](https://leafmap.org/notebooks/26_kepler_gl/),
    [GeoPandas mapping](https://geopandas.org/en/stable/docs/user_guide/mapping.html),
    and the course [visualization tutorial](https://github.com/thibaud-c/GST.200UB/blob/main/tutorials/09_visualization.md).

    # Part B. Your Graz analysis

    ## Task 1. Query Graz and its supermarkets with OSMnx

    First write `get_city(place)`. Use OSMnx to query the administrative boundary
    for the supplied place name. Return its GeoDataFrame in EPSG:4326, keeping
    its attributes. The check calls your function with `"Graz, Austria"`.
    Inspect the returned place name and geometry: did you get the city you intended?
    Part A1 shows the same operation for a different city.

    Then write `get_supermarkets(boundary)`. The input is a Shapely polygon in
    EPSG:4326. Return all mapped supermarkets inside it as an OSMnx GeoDataFrame.
    Choose the tag key and value yourself, using your Overpass Turbo experience
    and [OSM's supermarket tag](https://wiki.openstreetmap.org/wiki/Tag:shop%3Dsupermarket).
    Keep the original attributes and OSM index. Do not filter by brand yet.

    The check cells call each function once. Explore the supermarket table:
    inspect its shape, columns, geometry types, brand counts, and missing brands.
    Are both nodes and ways present? Does one mapped feature always mean one store?
    """)
    return


@app.function
def get_city(place):
    # Query OSMnx and return the place boundary as a GeoDataFrame in EPSG:4326.
    return None


@app.cell(hide_code=True)
def _(gpd, mo):
    city = get_city("Graz, Austria")
    city_ok = False
    try:
        assert isinstance(city, gpd.GeoDataFrame), "Complete get_city: return a GeoDataFrame."
        assert len(city) == 1, "Return one city boundary. Inspect the place query."
        assert city.crs is not None and city.crs.to_epsg() == 4326, "Keep the boundary in EPSG:4326."
        assert city.geom_type.isin(["Polygon", "MultiPolygon"]).all(), "Return an area boundary, not a point."
        assert city.geometry.is_valid.all() and not city.geometry.is_empty.any(), "Return a valid, non-empty boundary."
        assert "display_name" in city and "Graz" in city["display_name"].iloc[0], "Keep OSMnx attributes and check the place name."
        city_ok = True
        _message = "**Tests passed.** Inspect the place name and boundary before querying stores."
    except AssertionError as _error:
        _message = f"**Test failed:** {_error}"
    mo.md(_message)
    return city, city_ok


@app.cell
def _(city, city_ok, mo):
    mo.stop(not city_ok, mo.md("Complete the city query in Task 1 to inspect its result."))
    city[["display_name", "geometry"]]
    return


@app.function
def get_supermarkets(boundary):
    # Return a GeoDataFrame of OSM supermarkets in this EPSG:4326 polygon.
    return None


@app.cell(hide_code=True)
def _(city, city_ok, gpd, mo):
    mo.stop(not city_ok, mo.md("Complete the Graz boundary query before testing the supermarket query."))
    supermarkets = get_supermarkets(city.geometry.iloc[0])
    download_ok = False
    try:
        assert isinstance(supermarkets, gpd.GeoDataFrame), "Complete get_supermarkets: return a GeoDataFrame."
        assert not supermarkets.empty, "The query returned no features. Check the tags."
        assert supermarkets.crs is not None and supermarkets.crs.to_epsg() == 4326, "Keep the download in EPSG:4326 for now."
        assert "shop" in supermarkets and supermarkets["shop"].eq("supermarket").all(), "Query shop=supermarket only."
        download_ok = True
        _message = f"**Tests passed.** Downloaded {len(supermarkets)} supermarket features. Now inspect the table."
    except AssertionError as _error:
        _message = f"**Test failed:** {_error}"
    mo.md(_message)
    return download_ok, supermarkets


@app.cell
def _(download_ok, mo, supermarkets):
    mo.stop(not download_ok, mo.md("Complete Task 1 to explore the downloaded supermarkets."))
    supermarkets.head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Add exploration cells here. Try `supermarkets.columns.tolist()`,
    `supermarkets.geom_type.value_counts()`, and
    `supermarkets["brand"].value_counts(dropna=False)`. Keep a note of unusual
    labels or possible duplicate store records. A passing tag check does not
    establish completeness.

    ## Task 2. Prepare BILLA points

    Write `prepare_billa(data)`. Project the downloaded GeoDataFrame to EPSG:32633,
    convert geometry to representative points, and keep brands containing `billa`,
    ignoring case and excluding missing values. Include BILLA PLUS. Keep the
    original index so you can trace records back to OSM.

    Inspect the selected labels and locations. If the number surprises you,
    return to the full brand counts before changing your filter.
    """)
    return


@app.function
def prepare_billa(data):
    # Return projected BILLA-family points with their attributes and OSM index.
    return None


@app.cell(hide_code=True)
def _(download_ok, gpd, mo, supermarkets):
    mo.stop(not download_ok, mo.md("Complete Task 1 before testing Task 2."))
    billa = prepare_billa(supermarkets)
    billa_ok = False
    try:
        assert isinstance(billa, gpd.GeoDataFrame), "Complete prepare_billa: return a GeoDataFrame."
        assert not billa.empty and billa.crs is not None and billa.crs.to_epsg() == 32633, "Return BILLA stores in EPSG:32633."
        _mask = supermarkets["brand"].astype("string").str.contains("billa", case=False, na=False, regex=False)
        _expected = supermarkets.loc[_mask].to_crs(32633)
        assert billa.index.equals(_expected.index), "Keep all and only matching records with the original index."
        assert billa.geom_type.eq("Point").all(), "Convert footprints to points."
        assert billa.geometry.geom_equals(_expected.geometry.representative_point()).all(), "Check projection and representative points."
        billa_ok = True
        _message = f"**Tests passed.** {len(billa)} BILLA-family features. Inspect the selected brands and map."
    except AssertionError as _error:
        _message = f"**Test failed:** {_error}"
    mo.md(_message)
    return billa, billa_ok


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Task 3. Build cumulative distance zones

    Write `make_zones(points, boundary, distances)`. Both inputs use a metric CRS.
    Return one GeoDataFrame row per requested distance, in the supplied order,
    with columns `distance_m` and `geometry`. Merge overlaps and clip each zone
    to the boundary. Part A4 shows the operations on the small example.

    Use `[250, 500, 1000, 2500]` metres for Graz. Inspect the areas at each distance.
    They should grow or stay the same and never exceed the city's area. Explain
    why adding the four cumulative areas would count some land several times.
    """)
    return


@app.function
def make_zones(points, boundary, distances):
    # Return merged, clipped zones with one row per distance, in order.
    return None


@app.cell
def _(city, city_ok, mo):
    mo.stop(not city_ok, mo.md("Complete the Graz boundary query before projecting it."))
    city_m = city.to_crs(32633)
    distances_m = [250, 500, 1000, 2500]
    return city_m, distances_m


@app.cell(hide_code=True)
def _(billa, billa_ok, city_m, distances_m, gpd, mo):
    mo.stop(not billa_ok, mo.md("Complete Task 2 before testing the Graz zones."))
    billa_zones = make_zones(billa, city_m, distances_m)
    zones_ok = False
    try:
        assert isinstance(billa_zones, gpd.GeoDataFrame), "Complete make_zones: return a GeoDataFrame."
        assert billa_zones.crs == city_m.crs, "Keep the metric CRS."
        assert "distance_m" in billa_zones and billa_zones["distance_m"].tolist() == distances_m, "Keep one ordered row per distance."
        for _geometry, _radius in zip(billa_zones.geometry, distances_m):
            _expected = billa.buffer(_radius).union_all().intersection(city_m.geometry.union_all())
            assert _geometry.is_valid, "Inspect invalid geometry."
            assert _geometry.symmetric_difference(_expected).area < 0.1, "Check buffer radius, overlap merging, and clipping."
        zones_ok = True
        _message = "**Tests passed.** Explore the areas and view the four zones."
    except AssertionError as _error:
        _message = f"**Test failed:** {_error}"
    mo.md(_message)
    return billa_zones, zones_ok


@app.cell
def _(billa_zones, mo, zones_ok):
    mo.stop(not zones_ok, mo.md("Complete Task 3 to inspect cumulative areas."))
    billa_zones.assign(area_km2=billa_zones.geometry.area / 1_000_000)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Task 4. Estimate the average distance

    Write `estimate_mean_distance(cumulative_areas, city_area, midpoints, outside_distance)`.
    Return one number in metres. All areas use the same units. Inputs are ordered,
    non-decreasing cumulative areas bounded by the city area; each has a midpoint.

    1. Subtract successive cumulative areas to get ring areas, starting at zero.
    2. Calculate the outside area as the city area minus the final cumulative area.
    3. Multiply each ring area by its midpoint and add those products.
    4. Add outside area multiplied by its assumed distance.
    5. Divide by the city area.

    The test uses small numbers you can verify by hand. It does not require the
    OSM download, so you can work on this function independently.
    """)
    return


@app.function
def estimate_mean_distance(cumulative_areas, city_area, midpoints, outside_distance):
    # Return the area-weighted band estimate in metres, including outside area.
    return None


@app.cell(hide_code=True)
def _(mo):
    mean_ok = False
    try:
        _answer = estimate_mean_distance([20, 50, 80], 100, [50, 150, 300], 600)
        assert _answer is not None, "Complete estimate_mean_distance and return a number."
        assert abs(_answer - 265) < 0.000001, "The worked example should give 265 m. Use ring areas, not cumulative areas."
        _full = estimate_mean_distance([20, 50, 100], 100, [50, 150, 300], 600)
        assert abs(_full - 205) < 0.000001, "If the city is fully covered, outside area must be zero."
        _changed = estimate_mean_distance([20, 50, 80], 100, [50, 150, 300], 1000)
        assert abs(_changed - 345) < 0.000001, "Include the outside distance in the weighted total."
        mean_ok = True
        _message = "**Tests passed:** 265 m, 205 m with no outside area, and 345 m with the changed outside assumption."
    except AssertionError as _error:
        _message = f"**Test failed:** {_error}"
    mo.md(_message)
    return (mean_ok,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Apply the estimate to Graz and test the assumption

    The slider changes only the outside-distance assumption. It does not trigger
    a download. Start at 3000 m. Predict what happens at 5000 m before moving it.
    """)
    return


@app.cell
def _(mo):
    outside_distance = mo.ui.slider(
        2500, 7500, step=250, value=3000,
        label="Assumed distance beyond the 2500 m zone, in metres",
        show_value=True,
    )
    outside_distance
    return (outside_distance,)


@app.cell
def _(billa_zones, city_m, mean_ok, mo, outside_distance, zones_ok):
    mo.stop(not zones_ok or not mean_ok, mo.md("Complete Tasks 3 and 4 to calculate the Graz estimate."))
    billa_areas = billa_zones.geometry.area.tolist()
    city_area_m2 = city_m.geometry.area.sum()
    midpoints_m = [125, 375, 750, 1750]
    billa_mean_m = estimate_mean_distance(
        billa_areas, city_area_m2, midpoints_m, outside_distance.value
    )
    outside_fraction = (city_area_m2 - billa_areas[-1]) / city_area_m2
    mo.md(
        f"**Estimated average straight-line distance to a BILLA-family store: {billa_mean_m:.0f} m.** "
        f"The area beyond 2500 m is {outside_fraction:.1%} of Graz. "
        f"This estimate assigns it {outside_distance.value} m."
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Pause and reflect in your own notebook:

    - Compare the method with your initial proposal. What did you change, and why?

    - How much did the estimate change when you moved the slider? Can you explain
      that change using the fraction of land outside the largest zone?
    - What information is lost when every location in a band gets its midpoint?
    - Would narrower bands remove the outside-distance assumption?
    - Which source records would you inspect before quoting your number?
    - What might change if you included stores just outside Graz?

    You do not need a separate report. Keep brief answers or comments beside the
    result so you understand it when you reopen the notebook.

    ## Task 5. Explore BILLA and the distance zones in Kepler

    Follow Part A6. Use `leafmap.Map` and `add_gdf` to add the city, BILLA points, and the cumulative
    zones in EPSG:4326, then print the map object to display it directly.
    Start with `leafmap.Map(center=[47.07, 15.44], zoom=11, height=500)`.
    Label distances in metres and retain **© OpenStreetMap contributors**.

    Use the blank cell below. Inspect at least two stores and the city edge.
    Filter the zone layer by `distance_m` to compare thresholds. What areas
    contribute to the outside band? Can you see the effect of merging overlaps?
    """)
    return


@app.cell
def _():
    # Create and display your Graz Kepler map here.
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Homework. Repeat for the SPAR family

    Use the same downloaded supermarkets, boundary, distances, and outside
    assumption. Keep your BILLA work. Select brands containing `spar` without
    case sensitivity, including the matching EUROSPAR and INTERSPAR labels.
    Inspect those labels rather than assuming the rule is perfect.

    Reuse `make_zones` and `estimate_mean_distance`. Compare the two estimates
    and their outside-area fractions. Which is more sensitive to the outside
    assumption? Does your visual comparison support the numerical one?

    If you have time, try narrower bands or a larger final distance, updating
    midpoints accordingly. Explain which source of approximation each change
    addresses. Keep the source data fixed while comparing methods.

    ## Further help

    - [OSMnx worked examples](https://github.com/gboeing/osmnx-examples)
    - [GeoPandas introduction](https://geopandas.org/en/stable/getting_started/introduction.html)
    - [Code practices](https://github.com/thibaud-c/GST.200UB/blob/main/tutorials/08_code_practices.md)
    - [OpenStreetMap attribution](https://www.openstreetmap.org/copyright)
    """)
    return


if __name__ == "__main__":
    app.run()
