# Lab 02: explore crime data before mapping hotspots

Can a map built from earlier records help locate incidents in a later period?
What would make that comparison convincing?

Start with Figure 1 in [Chainey, Tompson & Uhlig (2008), *The utility of hotspot
mapping for predicting spatial patterns of crime*](https://link.springer.com/article/10.1057/palgrave.sj.8350066)
([DOI](https://doi.org/10.1057/palgrave.sj.8350066)). Before opening the worked examples,
write a few lines about:

- What would you need to know about the records before mapping them?
- How would you decide which observations to use for building and evaluating a map?
- Would catching more incidents always make one map better?
- What exactly are representing the _crimes_ within the Chicago dataset?

Keep your first answer and revisit it after the exercise.

## Choose the file you need

The exercise file contains all the content you need for this lab. The other files are provided for reference and additional context.

| File | Use it for |
| --- | --- |
| [demo.py](demo.py) | The short classroom demonstration: one title and the working cells. |
| [exercise.py](exercise.py) | The main lab exercise with worked examples, tasks, checks, and short reflection prompts. |
| [notes.md](notes.md) | Longer explanations, paper comparisons, documentation, and extra practice. |

Start in the exercise. Predict an output, run the example, then try the matching task.
Read a notes chapter when you need more explanation; you do not need to read it all first.
The notebook's **Notes** links open the matching chapter on GitHub in a new tab.
For offline reading, open `notes.md` in VS Code and choose **Open Preview to the Side**.
Keep your notebook open and return to the same section after reading.

## Start here

Save your work and run `git pull` to get the latest changes, then `uv sync`, in a
separate terminal in the course folder. See the [Git tutorial](../tutorials/04_git.md)
if you need help. Open [exercise.py](exercise.py) in VS Code and choose
**marimo: Open as marimo notebook**. Select the course `.venv` kernel.
This notebook uses `lab_02` as its working folder, so `data/` means `lab_02/data/`.

- **Part A:** run small worked examples of EDA, SQL, spatial grids, clustering,
  and evaluation. Predict the results and try the interactive controls.
- **Part B:** investigate Chicago records, complete the SQL and function tasks,
  run their checks, and explain your conclusions beside the outputs.

The notebook is an adaptation of the paper's evaluation approach, using a different
city, period, and method selection.

## Part B: data and workflow

Use the files you downloaded manually. Part B reads them locally; it does not
download, overwrite, or convert them into another saved file.

| File in `lab_02/data/` | Contents |
| --- | --- |
| `chicago_2025.csv` | All categories from [Chicago's crime portal](https://data.cityofchicago.org/d/ijzp-q8t2), filtered to Year = 2025. |
| `chicago_boundary.geojson` | The [City of Chicago boundary](https://data.cityofchicago.org/d/qqq8-j68g), exported as GeoJSON. |

Keep the same files for the whole exercise and note their download date in your
notebook. DuckDB reads both website headers such as `Primary Type` and headers
such as `primary_type`. You do not need to edit the CSV by hand.

Work in this order:

1. Audit the full-year file, then explore **January–November** records.
2. Select 2025 burglaries in SQL and prepare spatial points, accounting for exclusions.
3. Build H3 and DBSCAN hotspot maps using January–November points only.
4. Keep those maps and settings fixed, then evaluate against **December** records.
5. Compare captured incidents, covered area, and PAI. Explain a map alongside its limitations.

The split is at **1 December 2025**. That date belongs to the test period.
`source_audit` checks the annual file; `category_audit` describes training-period
records. Task 1 is checked against the annual burglary count, not the training
count. Counts depend on your saved snapshot because the portal revises records.

Each coding task states its input and output, followed by a cell labelled
`Check ... Task ...`. A PASS checks those expectations. You still need to inspect
the outputs and complete the nearby map, audit, or reflection workspace.
The [Part B notes](notes.md#b1) explain the concepts behind these steps.

> [!IMPORTANT]
> These are approximate locations of police-recorded reports. They do not measure
> all crime or establish whether a neighbourhood is safe. Read the source's data
> limitations before interpreting a map. Do not try to recover exact addresses.

## Download from the website

If both files are already in `lab_02/data/`, start Part B. Otherwise:

1. Open [Crimes: 2001 to Present](https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-Present/ijzp-q8t2)
   and choose **Actions → Query data**.
2. In **Filters**, select **Year**, keep **is one of**, choose **2025**, then click
   **Apply**. Filter before exporting so you download only the required year.
3. Check that the table contains 2025 records. Keep all crime categories and the
   original columns; you will select BURGLARY in Task 1.
4. Choose **Export → Download file**, select **CSV**, then **Download**. The dialog
   should say that it exports the data returned by your current query.
5. Create `lab_02/data/` if needed. Save the CSV there as **`chicago_2025.csv`**.
6. Open [Boundaries: City](https://data.cityofchicago.org/d/qqq8-j68g).
   Use its export/download menu to select **GeoJSON**, then save it as
   **`chicago_boundary.geojson`** in the same folder.

Keep the original columns and values. Part B's first cells check the saved files
and their date coverage. See the [CLI tutorial](../tutorials/03_cli.md#relative-paths-in-a-notebook)
if a relative path does not point to the file you expect.

## Windows known issue: package repair

If A4 reports missing `pyproj`/PROJ data or Matplotlib font files:

1. Stop the marimo kernel in VS Code and other Python sessions using the course
   `.venv`. If marimo runs in a terminal, stop it with **Ctrl+C**.
2. In a separate PowerShell window, from the course folder, reinstall those packages:

   ```powershell
   uv sync --reinstall-package pyproj --reinstall-package matplotlib
   ```

3. Reopen the notebook with the course `.venv` and rerun A4. If Windows reports
   a locked file or "Access is denied", restart Windows and retry the command
   before opening marimo or another Python session.

See [uv's package reinstallation options](https://docs.astral.sh/uv/reference/cli/#uv-sync--reinstall-package).

> [!TIP]
> A passing check verifies specific expectations, not your whole analysis.
> Inspect tables and maps, keep track of exclusions, and explain assumptions.
> There is no separate report: keep reflections in your notebook.

Useful starting points: the [DuckDB tutorial](../tutorials/07_duckdb.md),
[H3 polygon walkthrough](https://uber.github.io/h3-py/polygon_tutorial.html),
[DBSCAN example](https://scikit-learn.org/stable/auto_examples/cluster/plot_dbscan.html),
and [visualization tutorial](../tutorials/09_visualization.md).
