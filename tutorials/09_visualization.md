# 9. Explore charts and maps

[Tutorial index](README.md) · Previous: [Code practices](08_code_practices.md)

## Cheatsheet

| Code | Use |
| --- | --- |
| `import plotly.express as px` | Load Plotly's concise chart interface |
| `px.bar(data, x="name", y="area_ha")` | Make an interactive bar chart |
| `figure` | Display a figure as the last expression |
| `import leafmap.kepler as leafmap` | Load the interactive map |
| `map_view.add_gdf(points, layer_name="Stores")` | Add a named geographic layer |
| `map_view` | Display the Kepler widget inside marimo (print the map object) |
| `points.to_crs(4326)` | Prepare longitude/latitude for a web map |

Allow 30 to 45 minutes. Prepare the environment using [uv section 2](01_uv.md#2-install-the-course-packages), then create `practice/visualization.py` as a marimo notebook with the course kernel using [marimo section 2](05_marimo.md#2-open-or-create-a-notebook). Keep imports in one Python cell and each example in its own cell.

## 1. Choose a view for the question

A bar chart compares quantities. A scatter plot relates two numeric variables. A map shows where something is. Choose the view before choosing colours.

We use Plotly and Kepler.gl in this class. Other libraries include Matplotlib for detailed static figures, Seaborn for statistical plots, and Bokeh for interactive charts. You do not need to install all of them.

## 2. Start with Plotly

In a Python cell:

```python
import plotly.express as px
import geopandas as gpd
import marimo as mo
import leafmap.kepler as leafmap
```

In another cell:

```python
park_data = {
    "name": ["River Park", "Hill Garden", "South Meadow"],
    "area_ha": [2.0, 1.2, 3.0],
}
park_chart = px.bar(
    park_data,
    x="name",
    y="area_ha",
    labels={"name": "Park", "area_ha": "Area in hectares"},
    title="Areas of three parks",
)
park_chart
```

`px.bar` returns a figure. The final expression displays it without `print`. Hover over bars to read values; use the toolbar to zoom or reset. Labels state the unit. In the original cell, change one area and rerun to see the effect.

> [!TIP]
> Keep a bar chart's numeric axis starting at zero when bar length represents magnitude. A shortened axis can exaggerate differences. Avoid colour differences that suggest categories your data does not contain.

For a numeric relationship, add another cell:

```python
survey_chart = px.scatter(
    x=[0.5, 1.0, 2.0, 3.0],
    y=[2, 4, 3, 7],
    labels={"x": "Park area in hectares", "y": "Observed benches"},
    title="Park survey",
)
survey_chart
```

Each dot is one survey record. The apparent association does not establish that a larger park causes more benches.

## 3. Prepare a geographic table

Run:

```python
map_points = gpd.GeoDataFrame(
    {"name": ["Example A", "Example B"]},
    geometry=gpd.points_from_xy([15.43, 15.45], [47.07, 47.08]),
    crs="EPSG:4326",
)
map_points
```

The order is x then y, meaning longitude then latitude. Check the table and CRS before mapping. For data already in a projected CRS, `.to_crs(4326)` transforms the coordinates for the web map. Changing a label alone would misplace the points.

## 4. Display Kepler.gl inside marimo

In a new Python cell:

```python
map_view = leafmap.Map(center=[47.075, 15.44], zoom=12, height=500)
map_view.add_gdf(map_points, layer_name="Example locations")
map_view
```

`leafmap.Map` creates the map. `center` takes latitude then longitude; `zoom` controls how close the view starts. These values open the map around our points near Graz. `add_gdf` adds a GeoDataFrame, and the final line displays the interactive map inside marimo.

Leafmap is useful because it offers several **backends**, the libraries that draw a map and provide its controls. `import leafmap.kepler as leafmap` selects Kepler. Other choices include ipyleaflet, Folium, and Plotly. You can choose the renderer that suits your task while using familiar operations such as adding a GeoDataFrame. Backends do not support identical methods or features; changing the import may require changing the map code. See [Leafmap's backend guide](https://leafmap.org/get-started/).

| Tool | Useful for | Tradeoff |
| --- | --- | --- |
| Plotly Express | Quickly building charts with hover and zoom | Detailed custom layouts can require more code; large figures can become slow |
| Leafmap with Kepler | Exploring several geographic layers and styling them interactively | More dependencies and browser resources; some styling is done through map controls |
| Matplotlib | Precise static figures for a report | Interactive exploration usually needs extra setup |

Open the layer controls, inspect the two points, and change their colour or radius. These choices affect appearance, not the underlying coordinates. With several layers, use different names and keep point layers above filled polygons. Turn off a boundary polygon's fill when you only need its outline.

> [!NOTE]
> The basemap needs internet access. Keep its attribution visible. A layer can be present even if the basemap fails to load. Leafmap still uses Kepler underneath; if controls render incorrectly, report your editor and package versions to the instructor.

Changing a style through the map controls may not preserve it when the notebook restarts. For this exercise, focus on inspecting the data and being able to explain your styling choices.

## 5. Read the map critically

Compare the map with its table. Check that every expected point is visible and that coordinates are in the correct order. A large symbol can hide nearby points. A filled buffer can hide the basemap. For distance bands, use a consistent light-to-dark sequence and label the distances in metres.

A basemap and a polished legend do not validate a method. Ask what is absent from the input and what the colours actually measure.

## Documentation and walkthroughs

- [Plotly Express](https://plotly.com/python/plotly-express/) and [bar charts](https://plotly.com/python/bar-charts/): worked examples.
- [Introducing Plotly Express](https://medium.com/plotly/introducing-plotly-express-808df010143d): Plotly's illustrated blog walkthrough. Use the current `import plotly.express as px` syntax from this tutorial.
- [Leafmap Kepler walkthrough](https://leafmap.org/notebooks/26_kepler_gl/) and [layer controls](https://docs.kepler.gl/docs/user-guides/c-types-of-layers): loading data and adjusting maps.
- [marimo Plotly integration](https://docs.marimo.io/api/plotting/plotly/).

## Exercise: make the view answer a question

1. Add a fourth park to `park_data`. Keep the names and values the same length. Predict which bar will be tallest (see [section 2](#2-start-with-plotly)).
2. Make a chart that clearly states its measure and unit. Explain why a bar chart fits this comparison (see [section 1](#1-choose-a-view-for-the-question) and [section 2](#2-start-with-plotly)).
3. Add a third point to `map_points`. Predict where it will appear before running (see [section 3](#3-prepare-a-geographic-table)).
4. In Kepler, inspect all three names and toggle the layer off and on. Explain why changing point size does not change the distance between points (see [section 4](#4-display-keplergl-inside-marimo)).
5. Identify one misleading styling choice you could make in either view, and fix it (see [section 2](#2-start-with-plotly) and [section 5](#5-read-the-map-critically)).

<details>
<summary>Check your work</summary>

The chart should contain four bars and the map three records. The tallest bar must match the largest area in the table. Coordinates remain unchanged when you alter symbol size or colour. A classmate should be able to name the plotted quantity and its unit without reading your code.

</details>
