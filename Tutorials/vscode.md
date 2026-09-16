# 1. Open and edit files with VS Code

[Tutorial index](README.md) · Next: [The terminal and paths](cli.md)

## Cheatsheet

| Action | How |
| --- | --- |
| Open the course | **File > Open Folder**, select `GST.200UB` |
| Save a file | **Cmd+S** on macOS; **Ctrl+S** on Windows/Linux |
| Find an action | **Cmd+Shift+P** on macOS; **Ctrl+Shift+P** on Windows/Linux |
| Preview Markdown | Command Palette > **Markdown: Open Preview to the Side** |
| Open a notebook | Command Palette > **marimo: Open as marimo notebook** |
| Create a notebook | Command Palette > **Create: New marimo notebook** |

Allow about 20 to 30 minutes. Start with the repository you cloned using the [course README](../README.md#clone-the-course-repository).

By the end, you should be able to open the course root, create and save a text file, and preview Markdown.

## 1. Install the editor

Download [Visual Studio Code](https://code.visualstudio.com/download) for your operating system and follow the installer. On macOS, move the application to Applications if prompted. On Windows, use the user installer unless your institution provides another installation method. On Linux, choose the package for your distribution.

Open VS Code from your application menu. You may skip account sign-in, themes, and AI setup. They are not needed for these exercises.

> [!NOTE]
> VS Code edits files. Installing it does not install the course's Python environment. We will do that with [uv](uv.md).

## 2. Open the course folder

1. Choose **File > Open Folder**.
2. Select the cloned `GST.200UB` folder containing `pyproject.toml`.
3. In the Explorer on the left, check that you can see `README.md`, `tutorials`, `pyproject.toml`, and `uv.lock`.
4. Click `README.md` to open it.

If a Workspace Trust dialog appears, trust the folder only if it is the course copy you intended to open. Trust allows VS Code to run tools supplied by that folder. See [Workspace Trust](https://code.visualstudio.com/docs/editing/workspaces/workspace-trust) for details.

The Explorer is a view of real files on your computer. Renaming or deleting a file there also changes it on disk.

## 3. Find the parts you will use

| Part | How to open it | What you do there |
| --- | --- | --- |
| Explorer | **View > Explorer** | Browse files and folders |
| Editor | Click a file in Explorer | Read and change the file's contents |
| Command Palette | **View > Command Palette** | Search for editor actions by name |
| Extensions | **View > Extensions** | Add language support when needed |

The [interface guide](https://code.visualstudio.com/docs/editing/getting-started/userinterface) explains the other panels. You do not need to learn them all now.

> [!TIP]
> Use the Command Palette when you cannot remember a shortcut. Type a few words from the action, such as `Markdown: Open Preview to the Side`.

## 4. Create a file and preview it

1. Right-click an empty area in Explorer and choose **New Folder**. Name it `practice`.
2. Right-click `practice` and choose **New File**. Name it `learning_log.md`.
3. Paste the following into the editor, then use **File > Save**.

```markdown
# My GST200B learning log

I opened the course folder in VS Code.

## A question to revisit

How does Python find a file on my computer?
```

The `.md` ending means Markdown, a plain-text format for headings, links, and lists. `#` creates a heading; `##` creates a smaller heading. Blank lines separate paragraphs.

With this file active, open the Command Palette and choose **Markdown: Open Preview to the Side**. You should see a large title and a smaller heading in the preview. Change the question, save, and watch the preview update. The [Markdown documentation](https://code.visualstudio.com/docs/languages/markdown) covers links and other formatting.

> [!IMPORTANT]
> Save with **Ctrl+S** on Windows/Linux or **Cmd+S** on macOS before running a file. A dot on the editor tab usually means the file contains unsaved changes.

### Markdown notation to keep handy

| Write this in a `.md` file | Meaning |
| --- | --- |
| `# Title` | Main heading |
| `## Section` | Section heading |
| `**important**` | Bold text |
| `*term*` | Italic text |
| `` `area_ha` `` | Inline code |
| `- A point` | Bullet list item |
| `1. A step` | Numbered list item |
| `[Course](../README.md)` | Link with a relative path |
| `> A quotation` | Blockquote |
| `- [ ] Try the exercise` | Unchecked task box |

Put blank lines around paragraphs, lists, and code blocks. To display several lines of code, put three backticks \`\`\` on a line before and after them. Add the language after the opening backticks, such as `python`.


## 5. Install Python and marimo support

In **View > Extensions**, search for and install:

- **Python**, published by **Microsoft**.
- **marimo**, published by **marimo-team**. Check the [official extension page](https://marketplace.visualstudio.com/items?itemName=marimo-team.vscode-marimo) if several results look similar.

Complete the [uv setup](uv.md) in your separate terminal application. After `uv sync` creates `.venv`, return to VS Code and open the Command Palette. Choose **Python: Select Interpreter** and select the course's `.venv`.

If it is not listed, choose **Enter interpreter path** and browse to:

- Windows: `.venv/Scripts/python.exe`
- macOS/Linux: `.venv/bin/python`

This selects the program that runs Python. The [Python environment guide](https://code.visualstudio.com/docs/python/environments) explains how the editor discovers environments.

## 6. Open a lab as a notebook

1. Click the lab's `.py` file in Explorer.
2. Press **Cmd+Shift+P** on macOS or **Ctrl+Shift+P** on Windows/Linux.
3. Search for **marimo: Open as marimo notebook** and select it.
4. When asked for a kernel or environment, select the course's `.venv` interpreter. The kernel is the Python process executing your cells.

Use this existing project environment rather than creating a separate sandbox for each lab. You should see editable cells and their outputs inside VS Code. For a new notebook, use **Create: New marimo notebook**, save it with a `.py` extension, and choose the same environment.

> [!TIP]
> Keep PowerShell or Terminal open beside VS Code for `git pull` and `uv sync`. Notebook cells run inside VS Code through the marimo extension. The [marimo tutorial](marimo.md) walks through the first notebook.

## If something looks wrong

| Symptom | Try this |
| --- | --- |
| Explorer shows only one file | Use **File > Open Folder** and select the course root |
| You see another `GST.200UB` folder inside Explorer | Open that inner folder containing `pyproject.toml` |
| The file is named `learning_log.md.txt` | Rename it to `learning_log.md` in Explorer |
| The preview shows old text | Save and check that the preview belongs to the file you edited |
| The marimo command is missing | Check that the marimo extension is installed and enabled; reload VS Code |
| A notebook cannot import a package | Run `uv sync`, select the course `.venv` as its kernel, then restart that kernel |

## Documentation and a video

- [VS Code interface documentation](https://code.visualstudio.com/docs/editing/getting-started/userinterface): look up the Explorer, editor, and Command Palette.
- [Microsoft's getting started video](https://code.visualstudio.com/docs/introvideos/basics): follow the folder-opening and file-editing demonstration. Skip the AI features for this course.

## Exercise: leave yourself a useful note

1. Add a `## What I can do now` heading to `practice/learning_log.md`.
2. Under it, write two bullet points describing actions you actually performed.
3. Add a Markdown link to the [course README](../README.md). Work out the relative path from your file in `practice`.
4. Save, preview, close the file tab, and reopen it from Explorer.
5. Reflect in one sentence: what is the difference between closing a tab and deleting a file?

You are done when the reopened file contains your changes and the preview displays a working link.

<details>
<summary>Check your work</summary>

Use `- ` before each bullet. The link from `practice/learning_log.md` is `[Course README](../README.md)`. The two dots mean the parent folder. Closing a tab leaves the file on disk; deleting removes it.

</details>
