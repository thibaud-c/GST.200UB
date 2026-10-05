# Tutorials and cheatsheets

[Back to the course](../README.md)

These guides support the GST200B classes. Use them to learn an unfamiliar tool or refresh the commands you need for an exercise. Each guide starts with a short cheatsheet and ends with a practice task and reflection.

## First time here?

Start with the [course README](../README.md#clone-the-course-repository) to install Git and clone the repository. 

Once you have a clone, follow this order if all the tools are new to you:

| Tutorial | What you practise | Approximate time |
| --- | --- | --- |
| [1. uv](01_uv.md) | Install uv and prepare Python and the course packages | 25 to 35 min |
| [2. VS Code](02_vscode.md) | Open the project, write Markdown, install the marimo extension | 20 to 30 min |
| [3. Terminal and paths](03_cli.md) | Navigate in a separate terminal and locate files | 25 to 35 min |
| [4. Git and GitHub](04_git.md) | Save changes, pull class updates, and resolve conflicts | 40 to 60 min |
| [5. marimo in VS Code](05_marimo.md) | Create cells, run a notebook, and use a slider | 30 to 45 min |
| [6. Python in marimo](06_python.md) | Work with values, lists, conditions, and functions | 45 to 60 min |
| [7. DuckDB in marimo](07_duckdb.md) | Query local tables and remote Parquet data in SQL cells | 60 to 90 min |
| [8. Readable Python and AI-generated code](08_code_practices.md) | Name, organise, explain, and check your code | 30 to 45 min |
| [9. Visualization](09_visualization.md) | Make charts with Plotly and maps with Kepler.gl | 30 to 45 min |

Start with uv so the course environment exists before selecting a notebook kernel. The cloning steps in the course README introduce the navigation commands needed for this setup. Filenames and headings use the same numbers, so you can follow the order in GitHub's file list. Exercise steps link back to the sections that explain them.

## Where to type

| Tool | Use it for |
| --- | --- |
| Separate PowerShell or Terminal window | `cd`, `git`, and `uv` commands |
| VS Code file editor | Markdown, CSV data, and ordinary Python files |
| marimo notebook inside VS Code | Python cells, SQL queries, explanations, and interactive outputs |
| GitHub in your browser | Course materials, issues, and discussions |

> [!TIP]
> Run terminal commands one line at a time. Copy the command, not an example prompt or its output. If a command fails, read the message before moving to the next line.

The **course root** is the `GST.200UB` folder containing `pyproject.toml`. Terminal commands in these guides start there unless a step explicitly changes folder. Notebook data paths start at Python's working directory. Check it once with `Path.cwd()`; see [relative paths](03_cli.md#relative-paths-in-a-notebook).

## The tools in one sentence each

- Git records versions on your computer; GitHub hosts the course repository online.
- VS Code edits files and, with the marimo extension, notebooks.
- The shell interprets the commands you type into your terminal application.
- Python runs your calculations and data-processing code.
- uv installs Python and the packages listed by the project.
- marimo keeps notebook outputs in step with their inputs.
- SQL expresses questions about tables; DuckDB executes those questions.

## A useful way to practise

Predict a result before running the example. Change one input, run again, and explain the difference. Keep short notes in `practice/learning_log.md`, which you create in the VS Code guide.

> [!NOTE]
> The small datasets we construct for teaching in the tutorials and lab demonstrations are fictional. OSMnx and Overture queries use live geographic data; their results depend on the retrieval date, release, and area.

If you get stuck, include the tutorial step, your operating system, the code or command, and its complete error message when asking for help. [Useful discussions count as course participation](../README.md#help-improve-the-class).

## Further reading

These courses and books informed the examples and teaching approach. They use different environments and may assume prior experience. Use the GST200B setup instructions for this class.

- [EfficientGeodataPython from Uni Graz (DE)](https://github.com/hkristen/EfficientGeodataPython2024): structured geospatial workflows with Python.
- [Introduction to GIS Programming](https://gispro.gishub.org/): software setup, Python basics, and geospatial applications.
- [UW Geospatial Data Analysis with Python](https://uwgda-jupyterbook.readthedocs.io/en/latest/intro.html): shell and Git skills, demonstrations, and exercises.
- [PyGIS](https://pygis.io/docs/a_intro.html): programming applied to geographic questions.

### Advanced resources

- [Advanced Geospatial Analytics with Python](https://hamedalemo.github.io/advanced-geo-python/intro.html): further study after the foundations.
- [Geographic Data Science with Python](https://geographicdata.science/book/): analysis and interpretation of geographic data.
- [Hands-on GeoAI](https://handson-geoai.readthedocs.io/en/latest/index.html): learning objectives followed by practical work.
