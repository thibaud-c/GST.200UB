# 4. Manage the course environment with uv

[Tutorial index](README.md) · Previous: [Git](git.md) · Next: [marimo](marimo.md)

## Cheatsheet

Run these in your separate terminal, from the course root unless noted otherwise.

| Command | Use |
| --- | --- |
| `uv sync` | Install or update the project's environment |
| `uv add rich` | Add a package to the project |
| `uv remove rich` | Remove that package requirement |
| `uv run python practice/hello.py` | Run an ordinary Python file |
| `uv python install 3.14` | Install a Python version |
| `uv python pin 3.14` | Select a compatible Python version for the project |
| `uv run python --version` | Check the Python version the project uses |

`rich` is an example package. Practise adding and removing it in the separate project at the end of this guide.

Allow about 25 to 35 minutes, plus downloads. You need your clone and a separate PowerShell or Terminal window. No Python installation is required before installing uv.

## 1. Install uv

uv installs Python and the packages a project needs. Use the command for your operating system from [Astral's installation guide](https://docs.astral.sh/uv/getting-started/installation/).

**Windows PowerShell:**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux:**

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

These commands download and run Astral's installer. The PowerShell policy option applies to that new process. On a managed computer, use your institution's installation procedure if scripts are blocked.

Close and reopen the terminal, then check:

```sh
uv --version
```

Expect a version number. Restart VS Code too if it was already open, so its extensions can find uv. The shell finds programs through `PATH`, a list of folders to search; a newly opened application picks up installation changes.

## 2. Install the course packages

Enter your clone. If you used the README's location:

```sh
cd ~/university/GST.200UB
ls
uv sync
```

`ls` should show `pyproject.toml` and `uv.lock`. `uv sync` creates or updates `.venv`, the local Python environment. It can download a suitable Python interpreter when needed.

| Item | What it contains |
| --- | --- |
| `pyproject.toml` | The required Python version and package requirements |
| `uv.lock` | The resolved package versions |
| `.venv/` | The installed environment on this computer |

A **package** supplies reusable Python code. A **dependency** is a package this project needs. The course includes marimo with SQL support, DuckDB, and geospatial packages. The current Python requirement is `3.14.*`.

> [!IMPORTANT]
> Run `uv sync` after `git pull` to pick up changed package requirements. Do not run `uv init` inside this existing course project.

Check the result:

```sh
uv run python --version
uv run python -c "import marimo; import duckdb; print('Course imports work')"
```

Expect Python 3.14 and `Course imports work`. The `-c` option runs a short piece of Python written inside quotes. `import` loads a package.

## 3. Use the environment in VS Code

After syncing, open the course folder in VS Code and install the [Python and marimo extensions](vscode.md#5-install-python-and-marimo-support).

Open the Command Palette with **Cmd+Shift+P** on macOS or **Ctrl+Shift+P** on Windows/Linux. Choose **Python: Select Interpreter** and select the course `.venv`. When a marimo notebook asks for a kernel, select that same environment.

Open an existing notebook with **marimo: Open as marimo notebook**. The [marimo tutorial](marimo.md) explains creating and running cells. There is no notebook launch command to keep running in your terminal.

> [!TIP]
> If an import works with `uv run` but fails in a notebook, the notebook may be using another environment. Select the course `.venv` and use **marimo: Restart notebook kernel**.

## 4. Add and remove packages

For a project you maintain, adding a package is one command:

```sh
uv add rich
```

This installs the package and updates both `pyproject.toml` and `uv.lock`. Removing the requirement uses:

```sh
uv remove rich
```

uv removes it from the environment if nothing else requires it. See [managing dependencies](https://docs.astral.sh/uv/concepts/projects/dependencies/).

For the course clone, add a package when a lab or the instructor asks for it. Keep `pyproject.toml` and `uv.lock` together when recording a dependency change in Git. Use the separate exercise project below to experiment freely.

## 5. Run an ordinary Python file

A script is a text file of instructions executed from top to bottom. To try one, create `practice/hello.py` in VS Code and save:

```python
print("Hello from GST200B")
```

From the course root in your separate terminal:

```sh
uv run python practice/hello.py
```

Expect `Hello from GST200B`. `uv run` chooses the project environment, so you do not need to activate `.venv` manually. The [Python tutorial](python.md) teaches the language inside a marimo notebook in VS Code.

## 6. Install or change Python

Installing an interpreter and choosing it for a project are different steps:

```sh
uv python install 3.14
uv python pin 3.14
uv sync
uv run python --version
```

`install` downloads Python. `pin` writes the preferred version to `.python-version`. `sync` brings the environment into line with the project. A pin can select only a version compatible with `requires-python` in `pyproject.toml`. See [installing Python](https://docs.astral.sh/uv/guides/install-python/) and [Python versions](https://docs.astral.sh/uv/concepts/python-versions/).

Keep Python 3.14 for this course. If you maintain a different project and want to move from 3.13 to 3.14, check package compatibility, edit that project's `requires-python` if necessary, then install, pin, sync, and rerun its code. Pinning alone does not change which Python versions the project allows.

After switching versions, reselect the environment in VS Code and restart notebook kernels. Do not try to change the environment while those kernels are running.

## If a command fails

| Symptom | Next step |
| --- | --- |
| `uv` is not found | Reopen the terminal and check the installation output |
| No `pyproject.toml` found | Run `pwd` and navigate to the course root |
| Requested Python is incompatible | Check `requires-python`; the course currently requires 3.14 |
| A package download fails | Check your connection or institution's proxy; keep the error message |
| A package cannot be built or installed | Record the package, OS, Python version, and uv version for help |
| Notebook import fails after adding a package | Check its selected environment and restart its kernel |

## Documentation and a blog post

- [uv installation](https://docs.astral.sh/uv/getting-started/installation/) and [working on projects](https://docs.astral.sh/uv/guides/projects/): the everyday workflow.
- [Astral's "uv: Unified Python packaging"](https://astral.sh/blog/uv-unified-python-packaging): follow the Python installation and project-management examples.

## Exercise: manage a small project

1. In your separate terminal, create a project outside the course clone:

   ```sh
   cd ~/university
   mkdir uv-practice
   cd uv-practice
   uv init --python 3.14
   uv sync
   ```

   Use another folder name if `uv-practice` already contains work. Here `uv init` is appropriate because this is a new project.

2. Run `uv add rich`. Open this practice folder in VS Code and find the new requirement in `pyproject.toml`.
3. Create `hello.py` containing `print("My practice environment works")`, save, and run `uv run python hello.py`.
4. Run `uv remove rich` and check the project file again.
5. Run `uv python pin 3.14` and inspect `.python-version`. Confirm the selected version with `uv run python --version`.
6. Explain what `sync`, `add`, and `run` each changed. Why should you share the project files rather than copying `.venv` to a classmate?

You are done when the script runs and you can identify which file records package requirements and which records the Python preference. Return to the course folder before continuing.

<details>
<summary>Check your reasoning</summary>

`sync` installs the project's environment. `add` changes the requirements and installs the package. `run` executes a command using that environment. `pyproject.toml` records requirements, while `.python-version` records the pin. Another computer should install its own environment from those files and the lockfile.

</details>
