import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import geopandas as gpd
    import osmnx as ox
    import leafmap.kepler as leafmap

    return gpd, leafmap, mo, ox, pd


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Lab 01 live demo: a table becomes a map
    """)
    return


@app.cell
def _(pd):
    places = pd.DataFrame({
        "name": ["Hauptplatz", "University of Graz", "Graz Hauptbahnhof"],
        "longitude": [15.4381, 15.4495, 15.4170],
        "latitude": [47.0711, 47.0788, 47.0715],
    })
    places
    return (places,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Add geometry and a coordinate reference system
    """)
    return


@app.cell
def _(gpd, places):
    graz_places = gpd.GeoDataFrame(
        places,
        geometry=gpd.points_from_xy(places["longitude"], places["latitude"]),
        crs=4326,
    )
    assert len(graz_places) == 3 and graz_places.crs.to_epsg() == 4326
    graz_places
    return (graz_places,)


@app.cell
def _(graz_places):
    graz_places.plot()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Get tagged OpenStreetMap features
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    [overpass status](https://overpass-api.de/api/status)
    """)
    return


@app.cell
def _(ox):
    tags = {"shop": "supermarket"}
    supermarkets = ox.features_from_place("Geidorf, Graz, Austria", tags=tags)
    print("Features:", len(supermarkets))
    print("CRS:", supermarkets.crs)
    print(supermarkets.geom_type.value_counts())
    supermarkets[["name", "shop", "geometry"]].head()
    return (supermarkets,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Save/read features as Geoparquet
    """)
    return


@app.cell
def _(supermarkets):
    # save supermarkets to parquet
    supermarkets.to_parquet("./data/graz_supermarkets.parquet")
    return


@app.cell
def _(gpd):
    # load the parquet file
    supermarkets_from_parquet = gpd.read_parquet("./data/graz_supermarkets.parquet")
    supermarkets_from_parquet
    return (supermarkets_from_parquet,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Display the GeoDataFrames with Kepler
    """)
    return


@app.cell
def _(graz_places, leafmap, supermarkets_from_parquet):
    supermarket_map = leafmap.Map(center=[47.071, 15.438], zoom=12)
    supermarket_map.add_gdf(graz_places[["name", "geometry"]], layer_name="Places we created")
    supermarket_map.add_gdf(
        supermarkets_from_parquet[["name", "shop", "geometry"]].to_crs(4326),
        layer_name="OSM supermarkets",
    )
    supermarket_map
    return


if __name__ == "__main__":
    app.run()
