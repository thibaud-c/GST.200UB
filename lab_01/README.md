# Lab 01: average distance to a supermarket in Graz

How far is a location in Graz from its nearest BILLA-family store? Your task is
to propose a way to estimate an average distance, implement it, and question
what that number tells you. At home, repeat the analysis for the SPAR family.

Start with the picture in [Arthur A.'s LinkedIn post about distances to Migros
in Switzerland](https://www.linkedin.com/posts/carbonateturi_you-are-on-average-only-78-km-away-from-activity-7234914074541633536-m11_/).
Before opening the worked tutorial, sketch how you might produce a similar
analysis for Graz:

- What input data would you need, and where could you get it?
- What do you think the colours or shapes represent? Check the legend.
- What would you measure, and what exactly would you average?
- Which choices cannot be recovered from the picture alone?

Keep your first idea, even if you change it later. The notebook then explains
the approach chosen for this exercise so you can compare it with your proposal.

## Start here

If course updates are available, save your work, run `git pull`, then `uv sync`
in a separate terminal in the course folder. See the [Git tutorial](../tutorials/04_git.md)
if you need help.

Open [exercise.py](exercise.py) in VS Code and choose **marimo: Open as marimo
notebook** from the Command Palette. Select the course `.venv` kernel.

- **Start:** write your proposed approach before reading the method.
- **Part A:** try some examples of the library you will use.
- **Part B:** complete the function bodies and run the following test cells.
  They show whether the checks passed and explain failures.
- Keep short answers to the reflection questions beside your results.

> [!TIP]
> Return to your initial sketch at the end. Which choices changed, and what
> evidence made you change them?
