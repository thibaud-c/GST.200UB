# 8. Write Python you can explain

[Tutorial index](README.md) · Previous: [DuckDB](07_duckdb.md) · Next: [Visualization](09_visualization.md)

## Cheatsheet

| Habit | Example |
| --- | --- |
| Name the quantity and unit | `distance_m`, `area_km2` |
| Use lowercase words with underscores | `average_distance`, `select_stores` |
| Name functions for their action | `convert_to_metres` |
| Keep a function focused | Calculate a result and return it |
| Break a long expression inside parentheses | One argument per line |
| Explain a decision in a comment | `# Merge overlaps before measuring area.` |
| Check an example you can calculate by hand | `assert hectares_to_m2(0.5) == 5000` |

Allow 30 to 45 minutes. Create `practice/readable_code.py` as a marimo notebook using [marimo section 2](05_marimo.md#2-open-or-create-a-notebook), then use Python cells for the examples. The aim is code you can revisit next week, change, and trust for a stated purpose.

## 1. Names are part of the explanation

Compare `x = 500` with `radius_m = 500`. The second tells you what the number means. Use meaningful names, but avoid sentences as variable names. `gpd` is a conventional alias for GeoPandas; `a`, `b`, and `x2` usually do not explain an analysis.

Use `snake_case` for functions and variables. Python distinguishes upper and lowercase letters. Avoid replacing built-in names such as `list`, `sum`, or `map` with your own variables.

```python
def hectares_to_m2(area_ha):
    """Convert an area in hectares to square metres."""
    return area_ha * 10000

hectares_to_m2(0.5)
```

The first string in the function is a **docstring**. It describes the function for readers and help tools. `return` gives the caller a value; `print` only displays one.

## 2. Keep lines and functions readable

Aim for about 79 characters per line, following Python's PEP 8 convention. The point is to avoid horizontal scrolling, not to win a character-count contest. Split a long function call across lines inside parentheses. Avoid joining unrelated statements on one line with semicolons.

There is no universal maximum number of lines in a function. As a review cue, inspect a function that grows beyond about 20 to 30 lines. Does it do several separate jobs? Split at those jobs, not at an arbitrary line number. A clear 12-line loop can be easier to understand than one dense comprehension.

```python
def select_large_areas(areas_ha, minimum_ha):
    selected = []
    for area_ha in areas_ha:
        if area_ha >= minimum_ha:
            selected.append(area_ha)
    return selected
```

In another cell:

```python
selected_areas = select_large_areas([0.5, 1.0, 2.0], 1.0)
assert selected_areas == [1.0, 2.0]
selected_areas
```

Notice the boundary case at exactly one hectare. A check should catch a plausible mistake, such as using `>` where the question requires `>=`.

## 3. Four principles worth using

Put each example below in its own cell. Predict the result before running it.

### DRY: Don't Repeat Yourself

Keep a calculation in one place when several parts of your analysis need the same rule. If you copy an area-conversion formula into five cells, a correction can easily reach only four of them.

Reuse the `hectares_to_m2` function from section 1:

```python
north_area_m2 = hectares_to_m2(3.7)
south_area_m2 = hectares_to_m2(5.3)
assert north_area_m2 == 37000
assert south_area_m2 == 53000
```

**Remember: one rule, one place to change it.** In the lab, BILLA and SPAR can share a distance-zone function. Their inputs differ; the calculation stays the same. DRY does not require a helper for every repeated line: combine code when it represents the same rule, rather than merely looking similar.

### KISS: Keep It Simple

Choose the clearest approach that solves the current problem. Use existing Python or library functions when their meaning is easy to explain.

```python
areas_to_total = [0.5, 1.0, 2.0]
area_total_ha = sum(areas_to_total)
assert area_total_ha == 3.5
area_total_ha
```

`sum` already adds a list. A custom class with methods for adding, storing, and retrieving the total would make this task harder to follow. Likewise, GeoPandas supplies `.buffer()`; we do not need to construct circles ourselves.

**Remember: make the next reader's job easy.** Simple does not always mean shortest. A clear loop can be better than a compressed expression you cannot explain.

### YAGNI: You Aren't Going to Need It

Implement the requirement you actually have. Avoid building options for imagined future requirements.

Today's question is how many areas reach a threshold:

```python
def count_large_areas(areas_ha, minimum_ha):
    return len(select_large_areas(areas_ha, minimum_ha))

assert count_large_areas([0.5, 1.0, 2.0], 1.0) == 2
```

The threshold is a useful input because the exercise asks us to vary it. A database connection, ten export formats, and a plug-in system are not needed to answer this question. Add an export option when someone actually needs to save the result in that format.

**Remember: today's question first.** YAGNI does not justify omitting checks, units, or handling a known missing value. Those are current needs.

### SoC: Separation of Concerns

Give different jobs different places. Downloading a dataset, calculating a quantity, and displaying it have different reasons to change.

The function below only calculates:

```python
def mean_area(areas_ha):
    if not areas_ha:
        raise ValueError("Provide at least one area.")
    return sum(areas_ha) / len(areas_ha)

assert mean_area([1.0, 3.0]) == 2.0
```

A separate cell decides how to display the result:

```python
mean_area_ha = mean_area([1.0, 3.0])
f"Mean area: {mean_area_ha:.1f} hectares"
```

Changing that label does not require changing the function. In a spatial notebook, keep the OSM download separate from buffer calculations and map styling. Moving a radius slider should recalculate the buffer, rather than download the city again.

**Remember: one job per piece.** Separate cells or small functions are enough here; you do not need a separate file or class for every step.

> [!TIP]
> When reviewing your code, ask four questions: Where would I change this rule? Can I make it clearer? Do I need this option now? Does this function have more than one job?

## 4. Comments explain choices

`# Add one` above `count += 1` adds little. A useful comment records a choice that the code cannot explain on its own:

```python
# Include the threshold itself because the question says "at least".
minimum_area_ha = 1.0
```

Use Markdown cells for the analysis question, input units, assumptions, and interpretation. Use short code comments near the decision they explain. Update both when the code changes. A confident but outdated comment can mislead the next reader.

## 5. Check before you trust

Run a small example whose answer you know. Include an edge case, such as zero area or a value exactly at a threshold. Restart the notebook kernel and run from the saved code. This catches dependencies on forgotten state.

For spatial work, check the CRS, units, feature count, missing values, and geometry types before interpreting output. A beautiful map is not a correctness test. Read errors rather than hiding them with `except: pass`.

## Documentation and a walkthrough

- [PEP 8](https://peps.python.org/pep-0008/): names, indentation, comments, and line length.
- [Python functions](https://docs.python.org/3/tutorial/controlflow.html#defining-functions): parameters and return values.
- [Corey Schafer's functions tutorial](https://www.youtube.com/watch?v=9Os0o3wzS_I): a worked introduction. Try the examples in marimo cells.

## Exercise: remove the clutter

In a new cell, write `total_area_m2(areas_ha)`. It should take a list of areas in hectares and return their total in square metres (see [functions, Python section 5](06_python.md#5-name-a-calculation-with-a-function)).

1. Use clear names and a short docstring that states the units (see [section 1](#1-names-are-part-of-the-explanation)).
2. Check `[0.5, 1.0, 2.0]` and an empty list. Predict both answers before running (see [section 5](#5-check-before-you-trust)).
3. Explain why a separate function for every arithmetic operator would make this harder to read (see [KISS and YAGNI in section 3](#3-four-principles-worth-using)).
4. Ask a partner to describe your function without running it. Revise anything they misread (see [section 1](#1-names-are-part-of-the-explanation) and [section 2](#2-keep-lines-and-functions-readable)).

<details>
<summary>Check your results</summary>

Expect `35000` and `0`. A short implementation can use `sum(areas_ha) * 10000`. You do not need a class, a configuration file, or another dependency.

</details>

## Finish by recognising AI slop

Here, **AI slop** means plausible-looking generated code or explanation that has not been understood and checked. It can include unnecessary helper layers, repeated code, invented APIs, misleading comments, or tests that merely repeat the same mistake as the implementation.

AI assistants often do a poor job of KISS and YAGNI: they can produce a general system when you need three lines. They can also appear to follow DRY while hiding a simple calculation behind several functions. Ask for a small change, the assumptions it makes, and an explanation of each unfamiliar operation.

> [!IMPORTANT]
> You remain responsible for code you run and conclusions you draw. If you cannot explain the CRS, units, filter, or average, you cannot judge whether a generated answer fits the spatial question. A successful run is not evidence that the method is right.

Before keeping generated code, remove unused parts, verify unfamiliar functions in the official documentation, and test a case you can solve yourself. Do not let an assistant alter the expected answer merely to make a failed test pass. Reflect on one line in your exercise: what evidence would convince you that it is correct, beyond an AI saying so?
