# 6. Learn Python in a marimo notebook

[Tutorial index](README.md) · Previous: [marimo](05_marimo.md) · Next: [DuckDB](07_duckdb.md)

## Cheatsheet

Write these in Python cells inside your VS Code marimo notebook.

| Python | Meaning |
| --- | --- |
| `area_ha = 0.5` | Assign a value to a name |
| `area_ha` | Display the last expression in a notebook cell |
| `print(area_ha)` | Print a value, including from inside a loop |
| `areas = [0.5, 1.2, 2.0]` | Make a list |
| `areas[0]` | Read the first item |
| `len(areas)` / `sum(areas)` | Count / add the items |
| `area_ha >= 1.0` | Test a condition |
| `def hectares_to_m2(area):` | Start a function definition |
| `assert 0.5 * 10000 == 5000` | Check an expected result |

Allow about 45 to 60 minutes. Complete the [marimo setup](05_marimo.md) first. No previous Python knowledge is assumed.

You will calculate an area, work through a list, select values with a condition, and write a reusable function.

## 1. Create a notebook and run a cell

In VS Code, open the Command Palette with **Cmd+Shift+P** on macOS or **Ctrl+Shift+P** on Windows/Linux. Choose **Create: New marimo notebook**, save it as `practice/python_basics.py`, and select the course `.venv` as its kernel. See [creating a notebook, marimo section 2](05_marimo.md#2-open-or-create-a-notebook), if you need the setup steps again.

Paste this into a **Python cell** and click its run button:

```python
park_name = "Mur Meadow"
area_ha = 0.5
area_m2 = area_ha * 10000
print(park_name)
print(area_m2)
```

Expected output:

```text
Mur Meadow
5000.0
```

A hectare is 10,000 square metres. Here, `=` assigns a value to a name, and `*` multiplies two numbers. `print(...)` calls a function that displays its argument.

> [!IMPORTANT]
> Run the examples as notebook cells in VS Code. Each block below goes in a new Python cell unless the instructions tell you to edit an existing one. Define a shared variable in only one cell; edit that definition when you want a different value.

> [!TIP]
> A notebook displays the **last expression** in a cell without `print`. Try a cell containing just `area_m2`. A table, plot, or map can also be the final expression. An assignment such as `area_m2 = 5000` does not display a value by itself. Use `print` when you want several text outputs or output from inside a loop.

## 2. Names and types

A **variable** is a name referring to a value. A value has a **type** that determines which operations make sense.

| Example | Type | Use |
| --- | --- | --- |
| `"Mur Meadow"` | `str`, a string | Text; keep the quotation marks |
| `3` | `int`, an integer | A whole-number count |
| `0.5` | `float` | A number with a fractional part |
| `True` or `False` | `bool`, a Boolean | A yes/no value |

Python is case-sensitive: `area_ha` and `Area_ha` are different names. Use a decimal point, such as `0.5`, even if your usual written convention uses a decimal comma. A comment begins with `#` and explains the code without being executed.

Add and run a new Python cell:

```python
# Report the result with a label and unit.
print(f"{park_name} covers {area_m2} square metres.")
print(type(area_ha))
```

The `f` before the string lets Python insert the values inside `{}`. The last line reports `<class 'float'>`. Change `area_ha` to `1.2`, predict the new area, and run that original cell. Then restore it to `0.5`.

The [Python introduction](https://docs.python.org/3/tutorial/introduction.html) has more examples of numbers and strings.

## 3. Store several values in a list

Add this block in a new Python cell:

```python
park_areas = [0.5, 1.2, 2.0]
print(park_areas[0])
print(len(park_areas))
print(sum(park_areas))
```

A **list** keeps values in order between square brackets. Commas separate its items. Python starts counting positions at zero, so `[0]` selects the first item. `len` counts the items and `sum` adds them.

The new lines should print `0.5`, `3`, and `3.7`. All areas in this list use hectares. Mixing hectares and square metres in the same list would give a meaningless total.

## 4. Repeat a calculation and make a choice

Add another Python cell:

```python
large_areas = []
for park_area in park_areas:
    if park_area >= 1.0:
        large_areas.append(park_area)

print(large_areas)
```

Read it as: start with an empty list; take each area in turn; if it is at least one hectare, append it to the new list. A **loop** repeats a block. A **condition** decides whether to execute a block.

- `for ... in ...` takes one item from the list each time.
- `>=` means greater than or equal to. `>` would exclude the boundary value.
- `:` starts the indented block after `for` or `if`.
- `.append(...)` adds one item to the list.

Use four spaces for each indentation level. `print(large_areas)` has no leading spaces, so it runs after the loop. The result should be `[1.2, 2.0]`.

> [!TIP]
> To understand a loop, follow one item by hand. For `0.5`, the condition is false and nothing is appended. For `1.2`, it is true.

The [control-flow guide](https://docs.python.org/3/tutorial/controlflow.html) explains `if`, `for`, and function definitions.

## 5. Name a calculation with a function

Add another Python cell:

```python
def hectares_to_m2(hectares):
    return hectares * 10000

print(hectares_to_m2(0.5))
assert hectares_to_m2(0.5) == 5000
assert hectares_to_m2(0) == 0
assert large_areas == [1.2, 2.0]
```

`def` defines a **function**, a named calculation you can call again. `hectares` is its input name, or **parameter**. `return` sends the computed value back to the caller. The call `hectares_to_m2(0.5)` provides the input `0.5`.

`==` compares two values; `=` assigns a value. An `assert` checks that a condition is true. Successful checks produce no output. If one fails, Python raises `AssertionError`. These checks are small examples of testing, not proof that every possible input works.

Run the cell. The new printed value is `5000.0`, followed by no assertion error. If you later change `park_areas`, reconsider the expected list in the last check too.

## 6. Import libraries and use their functions

Python's many libraries provide tools for specialised work, including spatial data analysis. A **library** is a collection of reusable code. `import` makes its modules available in your notebook. Installing a package with uv and importing it in Python are separate steps: the course's `uv sync` handles installation.

In a new cell:

```python
import geopandas as gpd
```

`as gpd` gives GeoPandas a short name. The dot in `gpd.points_from_xy(...)` accesses a function supplied by the library. A dot can also access an object's method, such as `sites.buffer(...)`, or an attribute, such as `sites.crs`. Functions and methods use parentheses; an attribute usually does not.

Run this in another cell:

```python
sites = gpd.GeoDataFrame(
    {"name": ["Site A", "Site B"]},
    geometry=gpd.points_from_xy([500000, 500600], [5210000, 5210300]),
    crs="EPSG:32633",
)
sites
```

This is a small spatial table. The coordinate system uses metres around Graz. You supplied two x coordinates, two y coordinates, and two names. A **GeoDataFrame** combines a table with a geometry column and its coordinate system.

In a new cell:

```python
site_buffers = sites.buffer(250)
site_buffers.plot(alpha=0.4)
```

GeoPandas supplies the buffer and plotting methods. Here a buffer covers locations within 250 metres of each point; `.plot()` draws those polygons. `alpha` controls transparency. Change 250 to 500 in the original cell and inspect the overlap. Do not buffer longitude/latitude coordinates in degrees when you need metres.

> [!NOTE]
> Use one import per library in the notebook. If you need another package, add it with `uv add package-name` in your separate terminal, then import its Python module. Package and import names sometimes differ.

[GeoPandas' introduction](https://geopandas.org/en/stable/getting_started/introduction.html) explains these objects with more worked examples. The [visualization tutorial](09_visualization.md) develops the plotting side. For files, use relative paths and check your working folder as explained in [terminal and notebook paths](03_cli.md#relative-paths-in-a-notebook).

## 7. Read an error before changing code

An error report may include a **traceback**, showing where execution failed. Read the last line for the error type and message, then find the referenced line in the cell.

| Error | Common cause here |
| --- | --- |
| `SyntaxError` | Missing quote, bracket, or colon |
| `NameError` | A misspelled name or a name used before assignment |
| `TypeError` | An operation on an unsuitable type, such as adding text to a number |
| `IndentationError` | Leading spaces do not match the block structure |
| `IndexError` | Asking for a list position that does not exist |
| `AssertionError` | A computed result differs from an expected value |

Try a small deliberate mistake: change one use of `area_ha` to `area_h`, run, and read the message. Restore the spelling and rerun. Keep working from the first error, because dependent cells may be waiting for it to succeed.

## Documentation and a video

- [Python's introduction](https://docs.python.org/3/tutorial/introduction.html) and [control flow](https://docs.python.org/3/tutorial/controlflow.html): reference pages to revisit after this lesson.
- [Corey Schafer: strings in Python](https://www.youtube.com/watch?v=k9TUPpGqYTo): a beginner video about text, variables, and printing. Try its Python examples in notebook cells; some formatting examples in the video use older syntax.

## Exercise: compare areas

Use **Create: New marimo notebook** and save `practice/area_exercise.py`, so you keep the worked example intact. Choose the course `.venv` kernel (see [section 1](#1-create-a-notebook-and-run-a-cell) and [marimo section 2](05_marimo.md#2-open-or-create-a-notebook)).

1. Define `areas = [0.25, 1.0, 1.75, 3.0]` and `threshold = 1.0` in one cell (see [section 2](#2-names-and-types) and [section 3](#3-store-several-values-in-a-list)).
2. In another cell, use a loop and a condition to collect areas at least as large as `threshold` (see [section 4](#4-repeat-a-calculation-and-make-a-choice)).
3. Print how many areas you selected and their total in hectares (see [section 3](#3-store-several-values-in-a-list)).
4. Convert that total to square metres with a function (see [section 5](#5-name-a-calculation-with-a-function)).
5. Add an assertion for the expected selected total. Predict what changes when the threshold becomes `2.0`, then try it and update the check (see [section 5](#5-name-a-calculation-with-a-function)).
6. Write two sentences in your learning log: why does `>=` matter at the boundary, and what would go wrong if one input were already in square metres (see [section 3](#3-store-several-values-in-a-list), [section 4](#4-repeat-a-calculation-and-make-a-choice), and [editing Markdown, VS Code section 4](02_vscode.md#4-create-a-file-and-preview-it))?

You are done when you have run the notebook, checked both thresholds, and recorded your explanation. Save it, restart its kernel, and check that the results can be reproduced.

<details>
<summary>Show a hint</summary>

Start with an empty list. Use `.append(area)` inside the `if` block. Use `len` and `sum` after the loop. Define your area-conversion function in one cell before calling it from another.

</details>

<details>
<summary>Check your results</summary>

At a threshold of `1.0`, select `[1.0, 1.75, 3.0]`: three areas, `5.75` hectares, or `57500` square metres. At `2.0`, select only `[3.0]`: one area and `30000` square metres. `>=` includes an area equal to the threshold. Units must match before you add values.

</details>
