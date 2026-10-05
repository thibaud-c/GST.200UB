# 4. Receive class updates and save your work with Git

[Tutorial index](README.md) · Previous: [Terminal and paths](03_cli.md) · Next: [marimo](05_marimo.md)

## Cheatsheet

Run commands in your class directory clone, using a separate PowerShell or Terminal window.

| Command | Use |
| --- | --- |
| `git status` | See changed files and any unfinished merge |
| `git diff` | Read unstaged changes to tracked files |
| `git add lab_01/exercise.py` | Select a file's current changes for the next commit |
| `git diff --staged` | Check that selection |
| `git commit -m "Complete the area calculation"` | Record the selected changes locally |
| `git pull` | Fetch and merge the instructor's updates |
| `git log --oneline -5` | View the five most recent commits |
| `git merge --abort` | Cancel an unfinished merge and return to the pre-merge state |

Replace the lab filename with the file you actually edited. Save your files and commit edits to tracked files before pulling. This makes it easier to resolve or abort a merge without losing edits. Check section 4 for how to read `git status`, including local practice files.

Allow about 40 to 60 minutes. GitHub is required for the course. You will use your course clone, then deliberately create a conflict in a separate practice repository.

## 1. Install Git and sign in to GitHub

Create an account at [GitHub](https://github.com/signup) and sign in through your browser. You will use it to access course materials and raise issues.

Install [Git](https://git-scm.com/downloads) for your operating system. On Windows, allow the installer to make Git available from the command line. On macOS, running `git --version` may offer to install Apple's command-line tools. On Linux, follow the instructions for your distribution.

Close and reopen your separate terminal, then run:

```sh
git --version
```

You should see a version number. Git is the program on your computer; GitHub is the website hosting the repository. A public repository can be cloned without signing in, but you still need your account to participate in the class.

## 2. Clone once and configure your copy

Follow [the course cloning steps](../README.md#clone-the-course-repository) if you have not cloned it yet. Otherwise, enter your existing clone:

```sh
cd ~/university/GST.200UB
git remote -v
git status
```

`origin` is Git's short name for the source repository. It should point to `https://github.com/thibaud-c/GST.200UB.git`. Do not run `git init` inside this clone. It already has history.

Set your identity for local commits. Replace both example values:

```sh
git config user.name "Your Name"
git config user.email "your-address@example.com"
git config pull.rebase false
```

The first two commands record the author of your commits. They do not sign you in. The third tells this repository to merge incoming updates into your local history when you use `git pull`.

These settings apply only to this clone. For email privacy, copy the exact no-reply address shown in your [GitHub email settings](https://github.com/settings/emails). See [GitHub's commit-email guide](https://docs.github.com/en/account-and-profile/how-tos/email-preferences/setting-your-commit-email-address).

## 3. Save your work before pulling

Git already tracks the files delivered in your course clone, meaning it records their versions. A new file you create starts as untracked. `git add` starts tracking it; `git commit` records the selected version in local history.

There are three different actions:

| Action | Result |
| --- | --- |
| Save in VS Code | Writes your file to disk |
| Commit in Git | Records selected file changes in local history |
| Push | Uploads commits to a repository where you have write permission |

You can make local commits in your course clone without permission to push to the instructor's repository. Receiving materials uses `git pull`; follow the lab's instructions for submitting your work.

> [!IMPORTANT]
> Do not run `git push` to the instructor's course repository. Your exercise commits stay on your computer; you do not need to push them to receive updates. Use GitHub issues or discussions to suggest course improvements. Push group work only to your group's separate repository, as explained in section 7.

Suppose you edited `lab_01/exercise.py`. Save it in VS Code and shut down its notebook kernel before updating files. In the terminal:

```sh
git status
git diff
git add lab_01/exercise.py
git diff --staged
git commit -m "Save my Lab 01 progress"
```

`git add` stages the named file, meaning it selects that file's current contents for the next commit. `git diff --staged` lets you review the selection. The commit records it locally, even if the exercise is unfinished.

> [!TIP]
> Stage named files. Avoid `git add .` while learning, because it can include downloads, notebook caches, or unrelated changes. `git diff` does not display the contents of new, untracked files; inspect them in VS Code.

If `git status` lists other edits to tracked files, review and commit those named files too. The course's `.gitignore` hides local environments and notebook caches from the list of untracked files. Do not commit credentials or large downloaded datasets. A clean working tree is the simplest starting point for a pull.

## 4. Pull at the beginning of class

Save your files and shut down open notebook kernels. From the course root, check your copy **before** pulling:

```sh
git status
```

Read the message before choosing the next step:

| `git status` shows | What to do before `git pull` |
| --- | --- |
| `nothing to commit, working tree clean` | You can pull |
| `Changes not staged for commit`, such as `modified: lab_01/exercise.py` | Review with `git diff`, stage the named files, then commit your progress using section 3 |
| `Changes to be committed` | Review with `git diff --staged`, then commit the selected changes |
| `Untracked files`, such as `practice/` | These files are on disk but have not been added to Git; read the practice-file note below |
| `Unmerged paths` or a merge still in progress | Finish or abort that merge using section 5 before pulling again |

An “ahead by … commits” message can simply reflect your local exercise commits. It is not an instruction to push to the instructor's repository. `git status` describes your local copy; `git pull` contacts GitHub to check for new materials.

> [!NOTE]
> Files you create during the tutorials, such as `practice/learning_log.md` and `practice/duckdb_parks.py`, are your local practice work. You can leave them untracked and still pull if incoming files do not use the same paths. They remain on your computer, but Git has no saved history for them. To record a practice file locally, stage its exact filename and commit it as in section 3. You do not need to stage the entire `practice` folder. If Git says an incoming file would overwrite an untracked file, move your file to a backup folder outside the clone using VS Code or your file manager, then retry.

Once your tracked edits are committed and no merge is unfinished:

```sh
git pull
uv sync
```

`git pull` fetches new commits from GitHub and merges them into your current branch. It can add new lab files, update instructions, and bring in solutions without replacing your entire folder. `uv sync` updates the Python environment if the package requirements changed. If uv is not installed yet, complete [uv sections 1 and 2](01_uv.md#1-install-uv) before running it.

| Git reports | Meaning |
| --- | --- |
| `Already up to date` | Your copy already has the available updates |
| `Fast-forward` | Git advanced to newer commits without combining separate edits |
| A successful merge | Git combined local and incoming history |
| `CONFLICT` | Some changes need your decision; follow the next section |
| Local changes would be overwritten | Git stopped before merging; save and commit those files, then pull again |

A successful merge may open an editor for a commit message. Keep the proposed message, save, and close the editor. If the terminal opens Vim, press Escape, type `:wq`, then Enter. In Nano, press Ctrl+O, Enter, then Ctrl+X. To accept the proposed message without opening an editor on a future pull, use `git pull --no-edit`.

Once the pull finishes successfully, reopen the notebook in VS Code.

## 5. Resolve a merge conflict

A conflict can happen when you and the instructor edit the same part of an exercise. Git keeps both versions and asks you to decide what the combined file should contain.

1. Run `git status`. It lists the files that need attention.
2. In VS Code, open the conflicted file as text. For a marimo `.py` file, use **Reopen Editor With > Text Editor** from the tab's context menu if needed. Keep its kernel shut down.
3. Find the conflict markers. A simplified example looks like this:

   ```text
   <<<<<<< HEAD
   area_limit = 0.5
   =======
   area_limit = 1.0
   >>>>>>> incoming-commit
   ```

   The part above `=======` is your current version. The part below is the incoming version. The labels after `>>>>>>>` vary.

4. Read the updated instructions and decide what to keep. For example, if the instructor corrected the required threshold, the result might be:

   ```python
   area_limit = 1.0
   # My earlier experiment used 0.5 hectares.
   ```

5. Remove all three marker lines and any content you do not want. Resolve every conflict in the file, then save.
6. Repeat for each conflicted file. Check the result:

   ```sh
   git diff --check
   git status
   ```

7. Stage each resolved file with `git add`. Saving or accepting a version in VS Code does not tell Git that the conflict is resolved; staging does. Review the result, then finish the merge:

   ```sh
   git add lab_01/exercise.py
   git status
   git diff --staged
   git commit -m "Merge class updates and keep my lab work"
   git status
   ```

   After `git add`, that file should no longer appear under `Unmerged paths`. If another file still does, resolve and stage it before committing. Git may say **All conflicts fixed but you are still merging**; the commit completes the merge.

8. Run `uv sync`, reopen the notebook in VS Code, and run its cells to check the result.

> [!IMPORTANT]
> VS Code's **Accept Current**, **Accept Incoming**, and **Accept Both** buttons are shortcuts, not decisions about correctness. Accepting both notebook versions can duplicate variable definitions or break Python structure. Read the resulting code and run it.

If you need to stop an unresolved merge, use `git merge --abort`. Because you committed your work first, Git can return to that pre-merge state. Do not use `git reset --hard` or a force-push to make a conflict disappear. The [Git merge guide](https://git-scm.com/docs/git-merge) explains resolution and aborting.

## 6. Use discussions/issues to improve the course

Use [the course Discussions page](https://github.com/thibaud-c/GST.200UB/discussions) (or [Issues page](https://github.com/thibaud-c/GST.200UB/issues)) for errors, ideas, or useful resources. Search existing issues first, then open **New discussion/issue** with a specific title and enough information to act on. A reproducible error report should include the file, command or cell, expected result, actual message, and operating system.

Useful contributions count as participation. Follow [the issue-writing steps in the course README](../README.md#help-improve-the-class). Do not create an issue just to report that a tutorial worked.

## 7. Work in a group repository

Keep your course clone for receiving materials. For each project, one member creates a separate repository on GitHub and invites the others through **Settings > Collaborators**. Choose visibility with the instructor. Never put participant responses in it.

1. The owner creates the repository with a README. Each member clones that repository into a sibling folder, outside the course clone.
2. Copy one complete starter folder's contents into the group repository. Copy the group contract too.
3. Configure your commit name and email there, as in section 2. Run `git config pull.rebase false` in this clone as well.
4. Before editing, run `git pull`. Agree who edits which file. Save, stage named files, review, and commit as above.
5. Run `git push` to share committed work. Use Git's browser sign-in flow when prompted. A normal GitHub password is not used as an HTTPS Git password. Never paste tokens into project files or shared messages.
6. Other members run `git pull` to receive the changes. If a push is rejected because the remote has newer commits, pull, resolve any conflict, test, then push again.

`git remote -v` tells you where a push will go. A permission error in the instructor's repository usually means you are in the course clone instead of the group repository. Each member keeps their own local clone; avoid editing one shared cloud-synced folder simultaneously.

## Documentation and a blog walkthrough

- [Git pull](https://git-scm.com/docs/git-pull) and [Git merge](https://git-scm.com/docs/git-merge): receiving updates and completing merges.
- [GitHub: resolving a merge conflict from the command line](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/addressing-merge-conflicts/resolving-a-merge-conflict-using-the-command-line): illustrated conflict-resolution steps.
- [GitHub's beginner guide to essential Git commands](https://github.blog/developer-skills/github/top-12-git-commands-every-developer-must-know/): revisit `status`, `diff`, `add`, and `commit`.

## Exercise: resolve a conflict on purpose

Use a separate folder for this controlled exercise, so the course history stays usable. A **branch** is a named line of development. Here two branches stand in for your work and an instructor update.

1. In your terminal, create the separate practice repository and configure your identity (see [section 2](#2-clone-once-and-configure-your-copy) and [creating folders, CLI section 4](03_cli.md#4-create-and-enter-a-folder)):

   ```sh
   cd ~/university
   mkdir gst-merge-practice
   cd gst-merge-practice
   git init -b main
   git config user.name "Your Name"
   git config user.email "your-address@example.com"
   ```

   Replace the name and email. If that practice folder already contains work, choose a new name.

2. Open this folder in a new VS Code window. Create `notes.md` containing `Minimum area: 1 hectare`. Save and commit it, then create a branch with `git switch -c` (see [section 3](#3-save-your-work-before-pulling) and [creating a file, VS Code section 4](02_vscode.md#4-create-a-file-and-preview-it)):

   ```sh
   git add notes.md
   git commit -m "Record the initial area threshold"
   git switch -c instructor-update
   ```

3. Change the line to `Minimum area: 2 hectares`, save, and commit. `git switch main` then returns you to the original branch (see [section 3](#3-save-your-work-before-pulling)):

   ```sh
   git add notes.md
   git commit -m "Update the required threshold"
   git switch main
   ```

4. The file returns to the original version. Change its line to `Minimum area: 0.5 hectares`, save, and commit. `git merge instructor-update` brings in the other branch (see [section 3](#3-save-your-work-before-pulling) and [section 5](#5-resolve-a-merge-conflict)):

   ```sh
   git add notes.md
   git commit -m "Try a smaller threshold"
   git merge instructor-update
   ```

5. Expect a conflict in `notes.md`. Resolve it by keeping the required threshold of 2 hectares and adding a separate sentence recording your 0.5-hectare experiment (see [section 5](#5-resolve-a-merge-conflict)).
6. Save, run `git diff --check`, stage `notes.md`, and commit the resolution. Check `git status` (see [section 5, steps 6 and 7](#5-resolve-a-merge-conflict)).
7. Explain why Git could not choose the threshold for you, and why committing before a class update helps you recover your work (see [section 3](#3-save-your-work-before-pulling) and [section 5](#5-resolve-a-merge-conflict)).

You are done when there are no conflict markers, Git reports a clean working tree, and both pieces of information are in the file. Return to your course folder afterward.

<details>
<summary>Check your work</summary>

One possible result is:

```text
Minimum area: 2 hectares
My earlier experiment used 0.5 hectares.
```

Finish with:

```sh
git add notes.md
git commit -m "Resolve the threshold conflict"
git status
```

The exercise uses `git merge` directly. A class `git pull` performs a fetch followed by a merge under our configuration, so the conflict-resolution steps are the same.

</details>
