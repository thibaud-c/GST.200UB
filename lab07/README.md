# 🤖 PPGIS Analysis with Git and Natural Language Processing

## Libraries to use:

- [transformers](https://huggingface.co/transformers/v3.0.2/main_classes/pipelines.html)
> Used to load ML models from Hugging Face

```python
# if not already install, you can install it with
!pip install torch transformers -q
import transformers as pipeline
```

<br>

## 💡 Objectives

By the end of this exercise, you will:
- Understand the basic Git commands for forking, cloning, committing, and pushing changes.
- Run spatial queries and handle geospatial data using `duckdb` and `geopandas`.
- Apply a transformer-based NLP pipeline to classify sentiments in user-generated geospatial data.
- Produce a visualisation of the classified data on an interactive map.

<br>

## 🎯 Goal of the exercise

You have been hired by the city of Tampere to analyze the geospatial data collected from the citizens. The city conducted a large survey to collect feedback on city location that are liked and disliked by the population. The survey collected the feedback in the form of text comments and the location of the comments. The city wants to understand the sentiment of the comments and visualize the positive and negative comments on a map. The officials shared with you a github link with a parquet file.

<br>

## 🛝 Step-by-step guide

### 🧑🏻‍💻 Github Basics
---

#### 1. Git Setup

1. create an account on [GitHub](https://github.com/)
2. install [Git](https://git-scm.com/downloads)
3. create a new repository on GitHub (`repository` -> `new`)
    - select a name for the repository (e.g., `tampere_sentiment_analysis`)
    - select the repository to be public
    - initialize the repository with a README file
    - initialize the repository with a `.gitignore` file for Python
    - choose a license (e.g., MIT)
4. clone the repository on your local machine using the command `git clone <repository-url>`
> [!TIP]
> you'll need to create a personal access token to clone the repository (👀 see [here](https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token))

**Your first repository is ready!** 🎉 


#### 2. On your local machine

1. update the README file with the name of the repository and the objectives of the exercise. Check the status of your repository with the command `git status`
2. add the changes to the staging area using the command `git add .`. Check the status of your repository.
> [!TIP]
> your can use `git add <file-name>` to add a specific file to the staging area
3. commit the changes using the command `git commit -m "YOUR MESSAGE"`. Check the status of your repository.
> [!NOTE]
> your message should be short, meaningful, and written in the past tense. No date is needed because it is already linked to your commit.
> You can verify your commit with the command `git log` (use q to exit).
> The git log command shows the history of the commits in the repository with information such as the commit id, author, date, and message
4. push the changes to the remote repository using the command `git push origin main`
> [!NOTE]
> `main` is the default branch name, but it can be different depending on the repository
5. check if the changes are correctly pushed on github


**Your did your first commit!** 🎉


#### 3. On github

1. modify the README file with additional information such as your name as author
2. commit the changes directly on the main branch via the GitHub interface
3. check if the changes are correctly committed

#### 4. On your local machine

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
- you can use a text editor to solve the conflicts
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


### 🤖 PPGIS Data Analysis with NLP
---

#### 1. Load the data from the parquet file

The data is available in a parquet file on GitHub: [tampere_sentiment_analysis.parquet](https://github.com/thibaud-c/GST.200UB/blob/main/lab07/data/mock_ppgis_data.parquet)
> [!NOTE]
> The geometry is projected in the Finish crs: `EPSG:3067`


1. Load the data from the parquet file using `geopandas.read_parquet()` (see documentation [here](https://geopandas.org/en/stable/docs/reference/api/geopandas.read_parquet.html)) or `duckdb`
> [!NOTE]
> remember duckDB can read by default parquet files, so you can use the query `SELECT * FROM ...` to load the data
>
> you should also load the spatial extension of duckdb to handle the geometry column `LOAD spatial`
2. Check some basic information about the data such as the number of rows, columns, and the first rows of the data
> [!TIP]
> you can use `DESCRIBE` or `SUMMARIZE` from duckdb to get information about the data
3. if you are using duckdb, you should convert the SQL output in a geodataframe
> [!TIP]
> Export the geometry from the parquet in text using the function `ST_AsText(geometry_column) as geometry`
>
> Define the geometry column in the geodataframe using `geopandas.GeoSeries.from_wkt(geometry_column_in_dataframe)`


#### 2. Create Sentiment Analysis Pipeline

1. Choose a transformer-based NLP pipeline from the [Hugging Face library](https://huggingface.co/models)
    - select the task, section `Natural Language Processing` -> `text-classification`
    - click on the model of your choice (e.g. `cardiffnlp/twitter-roberta-base-sentiment-latest`)
    - Read the information of the model, outputs, examples
2. Create a pipeline from the example, you need to use the `pipeline` function from the `transformers` library (see documentation [here](https://huggingface.co/docs/transformers/en/main_classes/pipelines))
3. Test the pipeline with a simple sentence (e.g., _"I love this place, it's amazing"_)

❓ **What is the sentiment of the sentence?** 🤔 
❓ **Which is the output of the pipeline?** 🤖 


#### 3. Apply the pipeline to the comments and visualize the results

1. Apply the pipeline to the comments in the dataset.
> [!TIP]
> <details>
>    <summary>💡 Are you blocked? </summary>
>    <br>
> You can use the `apply()` method of the geodataframe to apply the pipeline to each comment in the dataset.
> </details>

2. Add the sentiment as a new column in the geodataframe
3. Visualize the comments on a map using `folium` or `KeplerGL`

#### 🥊 Challenges

- Aggregate the sentiment of the comments by district and create 2 choropleth maps to visualize the positive and negative comments in the city.
- Push your notebook solution to the remote GitHub repository

--- 

**Congratulations! 🎉 You have successfully completed the exercise.** 