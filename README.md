# Advanced GIS Analysis 2: Reproducible spatial analysis with Python

University of Graz: GST200B

Course materials for GST200B, winter semester 2026. We use Python, marimo, and DuckDB to work with geographic data, including OpenStreetMaps and Overture Maps. This repository contains the exercises, supporting tutorials, and solutions released during the course.

## Before the first class

A **GitHub account is required**. Create one at [GitHub](https://github.com/signup), then install [Git](https://git-scm.com/downloads) and clone the repository below. Next, follow [tutorial 1: uv](tutorials/01_uv.md) to install uv and prepare the environment before [tutorial 2: VS Code](tutorials/02_vscode.md).

No previous experience with these tools is assumed. The [tutorials](tutorials/README.md) explain the setup and provide cheatsheets you can return to during class.

### Clone the course repository

Open a separate terminal application:

- Windows: open **PowerShell** from the Start menu.
- macOS: open **Terminal** from Applications > Utilities.
- Linux: open your distribution's **Terminal** application.

Run each line below and wait for it to finish. First check that Git is installed:

```sh
git --version
```

You should see a version number. If the command is not found, finish the [Git installation](tutorials/04_git.md#1-install-git-and-sign-in-to-github), close the terminal, and open it again.

Next, create a place for your coursework and clone the repository:

```sh
cd ~
mkdir university
# or navigate to your preferred location
cd university
git clone https://github.com/thibaud-c/GST.200UB.git
cd GST.200UB
git config pull.rebase false
ls
```

`cd ~` takes you to your home folder. `mkdir` creates a folder, and `cd` enters it. **It is recommanded to use the folder you usually use for your classes**, the `university` folder is only an example. The clone creates a local `GST.200UB` folder containing the files and their Git history. The `git config` command tells this copy to merge incoming updates into your local work. You should see `README.md`, `tutorials`, and `pyproject.toml`. See [terminal navigation](tutorials/03_cli.md) if you get lost.

> [!IMPORTANT]
> Clone once. Keep using this same folder throughout the course so you can receive new materials with `git pull`.

### Prepare your environment

First complete [uv installation, tutorial 1 section 1](tutorials/01_uv.md#1-install-uv). Then, from the `GST.200UB` folder in your separate terminal:

```sh
uv sync
```

This installs the project's Python environment. Then open VS Code, choose **File > Open Folder**, and select `GST.200UB`. Follow the [VS Code setup](tutorials/02_vscode.md) to install the Python and marimo extensions and select the course's `.venv` environment.

To open a lab notebook, select its `.py` file, press **Cmd+Shift+P** on macOS or **Ctrl+Shift+P** on Windows/Linux, then choose **marimo: Open as marimo notebook**.

## At the beginning of each class

Save your work and shut down any open notebook kernel before receiving updates. In your separate terminal, enter the course folder. If you used the location above:

```sh
# navigate to your preferred location
cd ~/university/GST.200UB
git status
```

Read the [pre-pull status guide, Git section 4](tutorials/04_git.md#4-pull-at-the-beginning-of-class). It explains modified files, local practice files, and unfinished merges. When your working tree is ready:

```sh
git pull
uv sync
```

New exercises, corrections, and solutions with be updated between classes. `git pull` brings those changes into your existing copy. `uv sync` installs any changed package requirements. Reopen the notebook in VS Code after the update.

> [!NOTE]
> Your edits and an update may change the same lines. This is a normal merge conflict. Follow [the conflict-resolution walkthrough](tutorials/04_git.md#5-resolve-a-merge-conflict) to keep the changes you need from both versions.

## Find the materials

Use the lab instructions for tasks. The tutorials are supporting material for learning or revisiting the tools.

- [Lab 01: average distance to BILLA in Graz](lab_01/README.md): instructions, source post, and marimo notebook.
- [Lab 02: EDA and crime hotspot analysis](lab_02/README.md): source paper, training examples, and marimo exercise.
- [Lab 03: network analysis and routing in Graz](lab_03/README.md): graph training and two paper adaptations.
- [Lab 04: how close is "close"?](lab_04/README.md): local LLM practice and an adaptation of Figures 1–4.
- [Tutorials and cheatsheets](tutorials/README.md): setup, Python, SQL, code practices, and visualization.

## Help improve the class

Reporting errors, suggesting ideas, and sharing useful resources through GitHub discussions **counts as participation**.

1. Open the repository's [Discussions page](https://github.com/thibaud-c/GST.200UB/discussions) and check whether someone has already raised the topic.
2. If so, add a useful detail to the existing discussion. Otherwise, select **New discussion**.
3. Use a specific title, such as `Lab 01: CSV path does not work on Windows` or `Resource: video explaining spatial joins`.
4. For an error, include the file and step, what you ran, what you expected, and the complete error message. Include your operating system.
5. For an idea or resource, explain which course topic it helps with and add the link.
6. Select **Create** or **Submit**, depending on the form shown.

Keep passwords, tokens, and personal data out of discussions. 

## AI use

AI has been used to draft, review, and improve the course materials.
