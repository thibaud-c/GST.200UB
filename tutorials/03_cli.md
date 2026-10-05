# 3. Find your way around the terminal

[Tutorial index](README.md) · Previous: [VS Code](02_vscode.md) · Next: [Git and GitHub](04_git.md)

## Cheatsheet

Run these in a separate PowerShell or Terminal window.

| Command | Use |
| --- | --- |
| `pwd` | Show your current folder |
| `ls` | List its contents |
| `cd ~/university/GST.200UB` | Enter the clone, if you used the README's location |
| `cd tutorials` | Enter a child folder |
| `cd ..` | Move up one folder |
| `mkdir practice` | Create a folder, if it does not already exist |
| `cd "field notes"` | Enter a folder whose name contains a space |
| **Ctrl+C** | Interrupt a running command |

Allow about 25 to 35 minutes. Start with the course root open in VS Code and the `practice` folder from [tutorial 2, section 4](02_vscode.md#4-create-a-file-and-preview-it).

You will learn to check your location, list files, create a folder, and explain a relative path.

## 1. What is a command line?

A command-line interface, or CLI, lets you ask a program to do something by typing a command. The terminal is the application window you type into. The shell interprets your command and starts the requested program.

Open **PowerShell** from the Windows Start menu, **Terminal** from Applications > Utilities on macOS, or your Linux terminal application. Place it beside VS Code. On macOS the shell is usually zsh; on Linux it is often bash.

Enter the clone before trying the examples. If you followed the README:

```sh
cd ~/university/GST.200UB
# If you chose another location, use that path instead.
```

You might see a prompt such as this:

```text
PS C:\Users\Sam\Documents\GST.200UB>
```

The prompt is already there. Type after it. Enter this command and press Enter:

```sh
pwd
```

It reports the terminal's **working directory**, the folder used to resolve relative paths. In PowerShell, `pwd` is a short name for `Get-Location`. The result should identify your course root. The exact path will differ from the example.

> [!IMPORTANT]
> VS Code and your terminal keep their own locations. Clicking a file in VS Code does not move the terminal into its folder. Check the terminal's location with `pwd` whenever a file seems to be missing.

## 2. Look before you move

These commands work in the three shells used here:

```sh
ls
cd tutorials
pwd
ls
cd ..
pwd
```

Read the result after each line.

| Command | Meaning | Expected observation |
| --- | --- | --- |
| `ls` | List the current folder | At the course root, you see `pyproject.toml` |
| `cd tutorials` | Change directory to the child named `tutorials` | Usually no output on success |
| `pwd` | Show the current location | The path now ends in `tutorials` |
| `ls` | List that folder | You see files such as `03_cli.md` |
| `cd ..` | Move to the parent directory | You return to the course root |

PowerShell uses `Get-ChildItem` for `ls` and `Set-Location` for `cd`. We use the short names for navigation, but other commands and options can differ between shells. The [PowerShell location guide](https://learn.microsoft.com/en-us/powershell/scripting/samples/managing-current-location?view=powershell-7.5) explains its full commands.

## 3. Understand paths

A path describes where a file or folder is located.

| Path | Meaning |
| --- | --- |
| `.` | The current directory |
| `..` | The parent directory |
| `tutorials/03_cli.md` | A relative path, starting from the current directory |
| `/Users/Sam/Documents/GST.200UB` | An example absolute path on macOS |
| `/home/sam/Documents/GST.200UB` | An example absolute path on Linux |
| `C:\Users\Sam\Documents\GST.200UB` | An example absolute path on Windows |
| `~` | Your user home directory in our three shells |

An absolute path starts at a filesystem root or drive. A relative path depends on where you begin. From the course root, this tutorial is `tutorials/03_cli.md`. From inside `practice`, it is `../tutorials/03_cli.md`.

Windows often displays backslashes in paths. The relative paths with forward slashes used in these tutorials also work with PowerShell's navigation commands.

> [!CAUTION]
> Use relative paths for course data so another person can use the same folder structure. A relative path still needs the correct starting folder.

Try reading the first lines of this tutorial from the course root.

**Windows PowerShell:**

```powershell
Get-Content tutorials/03_cli.md -TotalCount 5 -Encoding UTF8
```

**macOS/Linux:**

```sh
head -n 5 tutorials/03_cli.md
```

These commands display text; they do not edit it.

> [!TIP]
> If PowerShell displays wrongly encoded characters, read it with `-Encoding UTF8`, as above. UTF-8 tells PowerShell how to decode the text. The course files use UTF-8; you do not need to change the file to fix this display problem. See [Microsoft's Get-Content reference](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-content#-encoding).

### Relative paths in a notebook

A relative path starts at Python's **working directory**, which need not be the folder open in your separate terminal. Return to this example once you have created a notebook using [marimo section 2](05_marimo.md#2-open-or-create-a-notebook). Save your notebook first. The VS Code marimo extension normally starts its kernel in the notebook's folder. Check this in a Python cell when you first use files:

```python
from pathlib import Path
Path.cwd()
```

For `practice/duckdb_parks.py`, the expected working folder is `practice`. With that starting point:

| Path in Python or SQL | File in the repository |
| --- | --- |
| `data/parks.csv` | `practice/data/parks.csv` |
| `learning_log.md` | `practice/learning_log.md` |
| `../README.md` | The course README |

If the output is the course root instead, use `practice/data/parks.csv`. If you move the working folder or launch the notebook another way, recheck the path. Do not guess or paste a personal absolute path into shared code.

Try `Path("learning_log.md").exists()` in another cell. It should return `True` after the VS Code exercise. Moving around in a separate terminal does not change the notebook's working folder. We do not need a notebook-directory helper for these examples.

## 4. Create and enter a folder

Run from the course root:

```sh
cd practice
mkdir "field notes"
cd "field notes"
pwd
cd ..
cd ..
```

`mkdir` creates a directory. Quotes keep `field notes` together as one path even though it contains a space. At the end, you should be back at the course root. Check with `pwd` and `ls`.

> [!TIP]
> Press Tab after typing part of a folder name to complete it. Press the Up arrow to recall an earlier command. Using names such as `field_notes` avoids needing quotes in many commands.

If the folder already exists, you can use it. You do not need to run `mkdir` again.

## 5. Read a command in pieces

Later you will use:

```text
uv run python --version
```

If you completed [uv section 2](01_uv.md#2-install-the-course-packages), you can run this from the course root. Otherwise, finish that setup first.

- `uv` is the program being started.
- `run` asks it to run another command in the project environment.
- `python` is the program uv will run.
- `--version` asks Python to print its version.

An option such as `--version` changes what a command does. A path such as `tutorials/03_cli.md` is an argument giving the command something to work on. Options belong to particular programs; do not assume every program supports the same ones.

## 6. Stop a running command

**Ctrl+C in the terminal** interrupts a running program. For example, it can stop a Python script launched with `uv run python`. If the terminal has selected text, clear the selection first so the shortcut interrupts instead of copying.

> [!CAUTION]
> Terminal deletion commands can remove files without sending them to the Recycle Bin or Trash. This tutorial does not require deleting anything. Use your file manager when cleaning up practice files.

## If a command fails

| Message or symptom | Likely cause and next step |
| --- | --- |
| `No such file or directory` or `Cannot find path` | Use `pwd` and `ls`; check the spelling and starting folder |
| `command not found` or `is not recognized` | Check the program name and whether it is installed |
| The shell shows `>` or `>>` and waits | You may have left a quote open; press Ctrl+C and enter the complete line again |
| A path with spaces fails | Put the whole path in straight quotes |
| Permission denied | Check that you are working in your own course folder; do not add administrator privileges just to silence the error |

## Documentation and another explanation

- [PowerShell location documentation](https://learn.microsoft.com/en-us/powershell/scripting/samples/managing-current-location?view=powershell-7.5): checking and changing your current folder.
- [Ubuntu's command-line tutorial](https://ubuntu.com/tutorials/command-line-for-beginners): a written walkthrough of navigation. Its commands target Unix shells; use our PowerShell alternatives on Windows.
- [PowerShell for beginners by Shane Young](https://learn.microsoft.com/en-us/shows/mvp-windows-and-devices-for-it/powershell-beginners): an introduction for Windows users. Focus on help and command discovery (also useful for macOS/Linux users).

## Exercise: navigate without guessing

1. From the course root, enter `practice` and create a folder named `site_visit` (see [section 4](#4-create-and-enter-a-folder)).
2. Enter `site_visit`. Predict what `pwd` will print, then run it (see [section 2](#2-look-before-you-move)).
3. Navigate from there to `tutorials` using one relative path with `cd` (see [section 3](#3-understand-paths)).
4. List its files, then return to the course root (see [section 2](#2-look-before-you-move)).
5. Add a note to `practice/learning_log.md` explaining why `tutorials/03_cli.md` works from the course root but not from `practice/site_visit` (see [section 3](#3-understand-paths) and [editing Markdown, VS Code section 4](02_vscode.md#4-create-a-file-and-preview-it)).

You are done when you can make the trip and explain the two parent-directory steps.

<details>
<summary>Check your work</summary>

```sh
cd practice
mkdir site_visit
cd site_visit
pwd
cd ../../tutorials
ls
cd ..
```

`../../tutorials` goes up from `site_visit` to `practice`, up to the course root, then down into `tutorials`. A relative path begins at the terminal's current directory.

</details>
