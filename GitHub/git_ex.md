# 🧑🏻‍💻 Github Basics
---

## 1. Git Setup :)

1. create an account on [GitHub](https://github.com/)
2. install [Git](https://git-scm.com/downloads)
3. create a new repository on GitHub (`repository` -> `new`)
    - select a name for the repository (e.g., `GIS_ANALYSIS`)
    - select the repository to be private or public
    - initialize the repository with a README file
    - initialize the repository with a `.gitignore` file for Python
    - choose a license (e.g., MIT)
4. clone the repository on your local machine using the command `git clone <repository-url>`
> [!TIP]
> you'll might need to create a personal access token to clone the repository (👀 see [here](https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token))

**Your first repository is ready!** 🎉 


## 2. On your local machine

1. update the README file with a title, author name, and date. Check the status of your repository with the command `git status`. You have new files that have been modified.
2. add the changes to the staging area using the command `git add .`. Check the status of your repository.
> [!TIP]
> your can use `git add <file-name>` to add a specific file to the staging area
3. commit the changes using the command `git commit -m "YOUR MESSAGE"`. Check the status of your repository.
> [!NOTE]
> your message should be short, meaningful, and written in the past tense. No date or file name are needed because it is already linked to your commit.
> You can verify your commit with the command `git log` (use q to exit).
> The git log command shows the history of the commits in the repository with information such as the commit id, author, date, and message
4. push the changes to the remote repository using the command `git push origin main`
> [!NOTE]
> `main` is the default branch name, but it can be different depending on the repository
5. check if the changes are correctly pushed to GitHub

**Your did your first commit!** 🎉


## 3. On github

1. modify the README file with additional information, such as a short description of the repository
2. commit the changes directly on the main branch via the GitHub interface
3. check if the changes are correctly committed

## 4. On your local machine

1. modify the README file with additional information such as the date of the exercise
2. try commit your changes and push them to the remote repository 
```bash
    git add .
    git commit -m "Updated README with the date of the exercise"
    git push origin main
```
> [!NOTE]
> you will get an error message because the remote repository has been updated since your last commit

> [!IMPORTANT] 
> you should always pull the changes from the remote repository with `git pull` before pushing your changes to avoid conflicts
> a good workflow is to always pull the changes from the remote repository before starting to work on your local repository
> example of a good workflow:
> ```bash
> git pull
> 'Resolve conflicts if needed'
> git add .
> git commit -m "Updated README with the date of the exercise"
> git push origin main
> ```

> [!TIP]
> sometimes you might have to save your changes before pulling the changes from the remote repository
> you can use `git stash` to save your changes before pulling and `git stash pop` to apply the changes back
3. Let's try to solve the conflict by pulling the changes from the remote repository and applying the changes to your local repository
- ```bash
    git pull
  ```
> [!IMPORTANT] 
> if you are lucky you won't have any conflicts and the changes will be automatically merged, you can now push your changes.
> 🚧 This is not often the case, and you might have to solve the conflicts manually
- you can use `git status` to see the files with conflicts
- you can use a text editor (e.g., VSCode) to solve the conflicts
> [!TIP]
> the conflicts are marked in the file with `<<<<<<< HEAD`, `=======`, and `>>>>>>> <commit-id>`
> you need to remove the markers and keep the changes you want to keep
- once the conflicts are solved, you can add the changes to the staging area, commit the changes, and push them to the remote repository
- ```bash
    git add .
    git commit -m "Solved conflicts"
    git push origin main
  ```
4. check on github if the changes are correctly pushed

**You completed your first conflict resolution!** 🎉 

>[!NOTE]
> On your repository in settings you can add collaborators to your repository. Collaborators can push changes to the repository.
> You can use the same workflow to collaborate with your fellow students on a project.