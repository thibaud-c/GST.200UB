# 6. Learn Python in a marimo notebook

[Tutorial index](README.md) · Previous: [marimo](marimo.md) · Next: [DuckDB](duckdb.md)

## Cheatsheet

Write these in Python cells inside your VS Code marimo notebook.

| Python | Meaning |
| --- | --- |
| `area_ha = 0.5` | Assign a value to a name |
| `print(area_ha)` | Display a value |
| `areas = [0.5, 1.2, 2.0]` | Make a list |
| `areas[0]` | Read the first item |
| `len(areas)` / `sum(areas)` | Count / add the items |
| `area_ha >= 1.0` | Test a condition |
| `def hectares_to_m2(area):` | Start a function definition |
| `assert 0.5 * 10000 == 5000` | Check an expected result |

Allow about 45 to 60 minutes. Complete the [marimo setup](marimo.md) first. No previous Python knowledge is assumed.

You will calculate an area, work through a list, select values with a condition, and write a reusable function.

## 1. Create a notebook and run a cell

In VS Code, open the Command Palette with **Cmd+Shift+P** on macOS or **Ctrl+Shift+P** on Windows/Linux. Choose **Create: New marimo notebook**, save it as `practice/python_basics.py`, and select the course `.venv` as its kernel.

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

A hectare is 10,000 square metres. Here, `=` assigns a value to a name, and `*` multiplies two numbers. `print(...)` calls a function that displays its argument. These are invented park measurements.

> [!IMPORTANT]
> Run the examples as notebook cells in VS Code. Each block below goes in a new Python cell unless the instructions tell you to edit an existing one. Define a shared variable in only one cell; edit that definition when you want a different value.

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

## 6. Find a file from the notebook

Python can load reusable code with `import`. Add this Python cell if marimo has not already supplied the import:

```python
import marimo as mo
```

In a separate cell:

```python
learning_log = mo.notebook_dir() / "learning_log.md"
print(learning_log)
print(learning_log.exists())
```

`as mo` gives the module a shorter name. A dot accesses something supplied by that module or object. `mo.notebook_dir()` gives the saved notebook's folder, and `/` joins it to a filename. For `practice/python_basics.py`, the result points to `practice/learning_log.md`.

`.exists()` checks whether the file exists. Expect `True` if you created the learning log in the VS Code tutorial. See [marimo's path helper](https://docs.marimo.io/api/miscellaneous/#marimo.notebook_dir) and the [Python pathlib reference](https://docs.python.org/3/library/pathlib.html).

> [!NOTE]
> Save the notebook before resolving paths. Using its directory keeps this path useful even when your separate terminal is open somewhere else.

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

Use **Create: New marimo notebook** and save `practice/area_exercise.py`, so you keep the worked example intact. Choose the course `.venv` kernel.

1. Define `areas = [0.25, 1.0, 1.75, 3.0]` and `threshold = 1.0` in one cell.
2. In another cell, use a loop and a condition to collect areas at least as large as `threshold`.
3. Print how many areas you selected and their total in hectares.
4. Convert that total to square metres with a function.
5. Add an assertion for the expected selected total. Predict what changes when the threshold becomes `2.0`, then try it and update the check.
6. Write two sentences in your learning log: why does `>=` matter at the boundary, and what would go wrong if one input were already in square metres?

You are done when you have run the notebook, checked both thresholds, and recorded your explanation. Save it, restart its kernel, and check that the results can be reproduced.

<details>
<summary>Show a hint</summary>

Start with an empty list. Use `.append(area)` inside the `if` block. Use `len` and `sum` after the loop. Define your area-conversion function in one cell before calling it from another.

</details>

<details>
<summary>Check your results</summary>

At a threshold of `1.0`, select `[1.0, 1.75, 3.0]`: three areas, `5.75` hectares, or `57500` square metres. At `2.0`, select only `[3.0]`: one area and `30000` square metres. `>=` includes an area equal to the threshold. Units must match before you add values.

</details>
