# University of Graz: GST200B

Course materials for GST200B, winter semester 2026. We use Python, marimo, and DuckDB to work with geographic data, including OpenStreetMaps and Overture Maps. This repository contains the exercises, supporting tutorials, and solutions released during the course.

## Before the first class

A **GitHub account is required**. Create one at [GitHub](https://github.com/signup), then install [Git](https://git-scm.com/downloads), [VS Code](https://code.visualstudio.com/download), and [uv](tutorials/uv.md#1-install-uv).

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

You should see a version number. If the command is not found, finish the [Git installation](tutorials/git.md#1-install-git-and-sign-in-to-github), close the terminal, and open it again.

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

`cd ~` takes you to your home folder. `mkdir` creates a folder, and `cd` enters it. If `university` already exists, skip `mkdir university`, it is recommanded to use the folder you usually use for your classes. The clone creates a local `GST.200UB` folder containing the files and their Git history. The `git config` command tells this copy to merge incoming updates into your local work. You should see `README.md`, `tutorials`, and `pyproject.toml`. See [terminal navigation](tutorials/cli.md) if you get lost.

> [!IMPORTANT]
> Clone once. Keep using this same folder throughout the course so you can receive new materials with `git pull`.

### Prepare your environment

From the `GST.200UB` folder in your terminal:

```sh
uv sync
```

This installs the project's Python environment. Then open VS Code, choose **File > Open Folder**, and select `GST.200UB`. Follow the [VS Code setup](tutorials/vscode.md) to install the Python and marimo extensions and select the course's `.venv` environment.

To open a lab notebook, select its `.py` file, press **Cmd+Shift+P** on macOS or **Ctrl+Shift+P** on Windows/Linux, then choose **marimo: Open as marimo notebook**.

## At the beginning of each class

Save your work and shut down any open notebook kernel before receiving updates. In your separate terminal, enter the course folder. If you used the location above:

```sh
# navigate to your preferred location
cd ~/university/GST.200UB
git status
```

If you have changed files, [save those changes in Git first](tutorials/git.md#3-save-your-work-before-pulling). When your working tree is ready:

```sh
git pull
uv sync
```

The instructor will push new exercises, corrections, and solutions between classes. `git pull` brings those changes into your existing copy. `uv sync` installs any changed package requirements. Reopen the notebook in VS Code after the update.

> [!NOTE]
> Your edits and an instructor update may change the same lines. This is a normal merge conflict. Follow [the conflict-resolution walkthrough](tutorials/git.md#5-resolve-a-merge-conflict) to keep the changes you need from both versions.

## Find the materials

Use the lab instructions for tasks. The tutorials are supporting material for learning or revisiting the tools.

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
