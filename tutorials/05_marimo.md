# 5. Use marimo notebooks in VS Code

[Tutorial index](README.md) · Previous: [Git](04_git.md) · Next: [Python](06_python.md)

## Cheatsheet

| Action | In VS Code |
| --- | --- |
| Open the Command Palette | **Cmd+Shift+P** on macOS; **Ctrl+Shift+P** on Windows/Linux |
| Create a notebook | **Create: New marimo notebook** |
| Open an existing notebook | **marimo: Open as marimo notebook** |
| Run a cell | Click its run button |
| Run pending dependent cells | **marimo: Run stale cells** |
| Restart execution | **marimo: Restart notebook kernel** |
| Inspect a value | Put it on the last line of a cell |

Allow about 30 to 45 minutes. Complete [uv section 2](01_uv.md#2-install-the-course-packages) and the [VS Code extension setup, section 5](02_vscode.md#5-install-python-and-marimo-support) first. You will edit and run the notebook inside VS Code. The Python examples are small; the next tutorial explains the language in more detail.

## 1. What is a notebook?

A **notebook** combines code, its output, and explanatory text. A **cell** is one editable block within the notebook.

marimo saves notebooks as `.py` files. It also tracks which cells use values defined by other cells. When an input changes, dependent cells run again in automatic mode. This behavior is called **reactivity**. The [key concepts guide](https://docs.marimo.io/getting_started/key_concepts/) explains how marimo determines that order.

## 2. Open or create a notebook

For a lab notebook, select its `.py` file in Explorer, open the Command Palette, and choose **marimo: Open as marimo notebook**. The marimo icon in the file's editor toolbar opens the same view.

For this tutorial:

1. Open the course root in VS Code.
2. Open the Command Palette and choose **Create: New marimo notebook**. Search for `marimo` if the wording differs in your extension version.
3. Save it as `practice/first_notebook.py`.
4. When asked for an environment or kernel, choose the course's `.venv` interpreter. A kernel is the Python process running your code.

You should now see notebook cells inside VS Code. The extension starts and manages the kernel. Use the existing project environment, so the notebook has the packages installed by `uv sync`.

> [!IMPORTANT]
> Create a notebook with the marimo command rather than pasting ordinary Python into an empty `.py` file and renaming it. marimo writes the structure that connects cells. [The extension guide](https://marketplace.visualstudio.com/items?itemName=marimo-team.vscode-marimo) lists its commands.

## 3. Run two Python cells

Paste this into the first Python cell and click its run button:

```python
area_ha = 0.5
```

Use the add-code-cell control to add another Python cell. Enter and run:

```python
area_m2 = area_ha * 10000
area_m2
```

`area_ha = 0.5` assigns a value to a name. The next cell multiplies it by 10,000 to convert hectares to square metres. The final expression in a cell is displayed as its output. You should see `5000.0`. An ordinary script uses `print` to display a value.

Now edit the **first** cell so that `area_ha = 1.2`, then run that cell. The dependent calculation should show `12000.0`. If marimo is set to lazy execution, it marks dependent cells as needing to run; run them or switch the runtime to automatic execution. See [running cells](https://docs.marimo.io/guides/reactivity/).

Do not add a second definition of `area_ha` in another cell. Edit the original definition. marimo requires a shared variable to be defined in only one cell, so it can identify where that value comes from.

> [!NOTE]
> Cell position alone does not determine execution order. The second cell depends on `area_ha`, so marimo runs the cell defining that name before the calculation that uses it.

## 4. Add an explanation

Add a new Python cell:

```python
import marimo as mo
```

`as mo` gives the imported module a shorter name. An import loads a module. Use this single import throughout the notebook. If marimo already inserted it, keep the existing import and do not add a duplicate.

In another Python cell:

```python
mo.md(f"The example park covers **{area_m2} square metres**.")
```

`mo.md` displays Markdown. The `f` before the string inserts the value inside `{}` into the text. Change `area_ha` in its original cell again and confirm that both the number and this sentence update. An explanation that uses the calculated value is less likely to become stale when the input changes.

## 5. Add a slider

Create a Python cell:

```python
area_slider = mo.ui.slider(
    start=0.0,
    stop=5.0,
    step=0.5,
    value=1.0,
    label="Park area in hectares",
)
area_slider
```

The words before `=` inside this function call are **keyword arguments**. They tell the slider its minimum, maximum, step size, initial value, and visible label. The final line displays it.

In a **separate** Python cell:

```python
slider_area_m2 = area_slider.value * 10000
mo.md(f"Selected area: **{slider_area_m2} square metres**.")
```

`area_slider.value` reads the current input. Move the slider to `2.0`. Expect `20000.0` square metres.

> [!TIP]
> Create an input in one cell and read its `.value` in another. That separation lets marimo rerun the calculation when the input changes. The [interactive elements guide](https://docs.marimo.io/guides/interactivity/) explains this pattern.

The original `area_ha` calculation and the slider calculation are independent examples. Moving the slider changes only cells that use `area_slider` or `slider_area_m2`.

## 6. Save and restart

Save with **Cmd+S** on macOS or **Ctrl+S** on Windows/Linux. Then use the Command Palette command **marimo: Restart notebook kernel** and rerun the notebook. Check that it can recreate its outputs from the saved code.

The slider starts at the `value` specified in its code after a restart. Do not rely on the last position you dragged it to as a saved parameter.

Before `git pull`, save and use **marimo: Shut Down Kernel**, available in the notebook or marimo menu. Reopen the notebook after pulling and running `uv sync`, so it loads the updated code and environment.

> [!WARNING]
> In automatic mode, dependent cells can rerun when an input changes. Keep file writes and downloads out of cells driven by sliders unless you intend to repeat those actions.

## 7. Use relative paths and SQL cells

Use a relative path such as `data/parks.csv` for a file inside the notebook's working folder. Check that folder with `Path.cwd()` if a file cannot be found. The [CLI tutorial](03_cli.md#relative-paths-in-a-notebook) explains why the terminal and notebook can start in different places.

marimo also has SQL cells. Choose **SQL** in the cell-language selector or add-cell menu, then enter a query directly. The [DuckDB tutorial](07_duckdb.md) shows how to name results and reuse them in later cells. SQL cells are saved as Python in the `.py` file; the editor handles that translation.

## If the notebook behaves unexpectedly

| Symptom | What to check |
| --- | --- |
| The marimo command is missing | Install or enable the official extension and reload VS Code |
| A package cannot be imported | Run `uv sync` in the course folder, choose `.venv` as the notebook kernel, and restart it |
| `MultipleDefinitionError` | Find both cells defining the same name; edit or rename one definition |
| Slider value cannot be read in its defining cell | Move the calculation into a new cell |
| A result stays stale | Check for a cell error or lazy execution mode, then run the affected cells |
| A cell cannot find a name | Run the defining cell and check spelling |

The [multiple-definitions guide](https://docs.marimo.io/guides/understanding_errors/multiple_definitions/) explains the error in more detail.

## Documentation and a video

- [marimo extension documentation](https://marketplace.visualstudio.com/items?itemName=marimo-team.vscode-marimo) and [key concepts](https://docs.marimo.io/getting_started/key_concepts/): editor commands and dependencies.
- [marimo's VS Code introduction](https://marimo.io/blog/vscode): a blog walkthrough with an embedded video of the extension.
- [marimo's concepts series on YouTube](https://www.youtube.com/watch?v=3N6lInzq5MI&list=PLNJXGo8e1XT9jP7gPbRdm1XwloZVFvLEq): begin with the introductory demonstration, then try its examples in your own notebook. This series is also linked from the official quickstart.

## Exercise: estimate how many plots fit

Continue in `practice/first_notebook.py`:

1. Create a slider called `plot_size` for plot sizes from `100` to `1000` square metres, in steps of `100`, starting at `500` (see [section 5](#5-add-a-slider)).
2. In another cell, calculate `plot_count = int(slider_area_m2 // plot_size.value)` (see [section 3](#3-run-two-python-cells) and [section 5](#5-add-a-slider)).
3. Display a sentence containing the selected area, plot size, and whole number of plots (see [section 4](#4-add-an-explanation)).
4. Test an area of `1.0` hectare with a plot size of `500`, then `600` square metres (see [section 5](#5-add-a-slider)).
5. Add a Markdown explanation of what this estimate ignores about real parks (see [section 4](#4-add-an-explanation)).
6. Save and reopen the notebook to check that it runs from its code (see [section 6](#6-save-and-restart)).

`//` divides and rounds down to a whole quotient. `int` converts the result to an integer. Keeping the minimum plot size above zero avoids division by zero.

You are done when both controls update the result and the notebook includes a limitation of the estimate.

<details>
<summary>Check your results</summary>

One hectare is 10,000 square metres. At 500 square metres per plot, the result is 20. At 600, it is 16 whole plots. This calculation uses only total area. It ignores park shape, paths, obstacles, and space between plots, so it cannot establish how many plots would actually fit on a map.

</details>
