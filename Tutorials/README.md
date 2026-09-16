# Tutorials and cheatsheets

[Back to the course](../README.md)

These guides support the GST200B classes. Use them to learn an unfamiliar tool or refresh the commands you need for an exercise. Each guide starts with a short cheatsheet and ends with a practice task and reflection.

## First time here?

Start with the [course README](../README.md#clone-the-course-repository) to install Git and clone the repository. 

Once you have a clone, follow this order if all the tools are new to you:

| Tutorial | What you practise | Approximate time |
| --- | --- | --- |
| [1. VS Code](vscode.md) | Open the project, write Markdown, install the marimo extension | 20 to 30 min |
| [2. Terminal and paths](cli.md) | Navigate in a separate terminal and locate files | 25 to 35 min |
| [3. Git and GitHub](git.md) | Save changes, pull class updates, and resolve conflicts | 40 to 60 min |
| [4. uv](uv.md) | Sync packages, add or remove a package, and choose Python | 25 to 35 min |
| [5. marimo in VS Code](marimo.md) | Create cells, run a notebook, and use a slider | 30 to 45 min |
| [6. Python in marimo](python.md) | Work with values, lists, conditions, and functions | 45 to 60 min |
| [7. DuckDB in marimo](duckdb.md) | Query local tables and remote Overture Parquet data | 60 to 90 min |

The VS Code guide points you to uv when you need the Python environment. You can read the cheatsheet first and return to the full explanation when a step is unfamiliar.

## Where to type

| Tool | Use it for |
| --- | --- |
| Separate PowerShell or Terminal window | `cd`, `git`, and `uv` commands |
| VS Code file editor | Markdown, CSV data, and ordinary Python files |
| marimo notebook inside VS Code | Python cells, SQL queries, explanations, and interactive outputs |
| GitHub in your browser | Course materials, issues, and discussions |

> [!TIP]
> Run terminal commands one line at a time. Copy the command, not an example prompt or its output. If a command fails, read the message before moving to the next line.

The **course root** is the `GST.200UB` folder containing `pyproject.toml`. Terminal commands in these guides start there unless a step explicitly changes folder. Notebook data paths start at the saved notebook's own folder.

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
> The small park datasets in these guides are fictional. The Overture section uses live geographic data, so its results depend on the selected release and area.

If you get stuck, include the tutorial step, your operating system, the code or command, and its complete error message when asking for help. [Useful discussions count as course participation](../README.md#help-improve-the-class).

## Further reading

These courses and books informed the examples and teaching approach. They use different environments and may assume prior experience. Use the GST200B setup instructions for this class.

- [Introduction to GIS Programming](https://gispro.gishub.org/): software setup, Python basics, and geospatial applications.
- [Geographic Data Science with Python](https://geographicdata.science/book/): analysis and interpretation of geographic data.
- [UW Geospatial Data Analysis with Python](https://uwgda-jupyterbook.readthedocs.io/en/latest/intro.html): shell and Git skills, demonstrations, and exercises.
- [PyGIS](https://pygis.io/docs/a_intro.html): programming applied to geographic questions.
- [Advanced Geospatial Analytics with Python](https://hamedalemo.github.io/advanced-geo-python/intro.html): further study after the foundations.
- [Hands-on GeoAI](https://handson-geoai.readthedocs.io/en/latest/index.html): learning objectives followed by practical work.


