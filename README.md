# IMDb Ratings Analysis

This project pulls the public IMDb datasets from [datasets.imdbws.com](https://datasets.imdbws.com/) and distills a handful of data stories about what audiences love to watch. The analysis script downloads the raw TSV dumps, filters out adult titles, and computes summary tables that are saved to `analysis/results.json` for easy reuse.【F:analysis/imdb_analysis.py†L7-L217】【F:analysis/results.json†L1-L735】

## Reproducing the analysis

1. (Optional) create and activate a virtual environment.
2. Install dependencies with `pip install -r requirements.txt` (only `pandas` is required).【F:requirements.txt†L1-L1】
3. Run `python analysis/imdb_analysis.py`. The script will download `title.basics.tsv.gz` and `title.ratings.tsv.gz` into `data/` (ignored by git) and regenerate `analysis/results.json` with all computed aggregates.【F:analysis/imdb_analysis.py†L7-L217】

## Highlights from the dataset

### All-time top rated feature films (≥100k votes)

| Rank | Title | Year | Avg rating | Votes |
| --- | --- | --- | --- | --- |
| 1 | The Shawshank Redemption | 1994 | 9.3 | 3,097,823 |
| 2 | The Godfather | 1972 | 9.2 | 2,159,074 |
| 3 | The Dark Knight | 2008 | 9.1 | 3,072,860 |
| 4 | The Lord of the Rings: The Return of the King | 2003 | 9.0 | 2,106,514 |
| 5 | Schindler's List | 1993 | 9.0 | 1,545,131 |
| 6 | The Godfather Part II | 1974 | 9.0 | 1,451,174 |
| 7 | 12 Angry Men | 1957 | 9.0 | 947,874 |
| 8 | The Lord of the Rings: The Fellowship of the Ring | 2001 | 8.9 | 2,140,137 |
| 9 | Inception | 2010 | 8.8 | 2,729,689 |
| 10 | Fight Club | 1999 | 8.8 | 2,514,096 |

These titles span six decades, yet the all-time leaderboard is dominated by dramas and crime sagas with massive vote counts (millions of ballots each).【F:analysis/results.json†L2-L72】

### Recent fan favorites (2015 onward, ≥50k votes)

| Rank | Title | Year | Avg rating | Votes |
| --- | --- | --- | --- | --- |
| 1 | 12th Fail | 2023 | 8.7 | 155,960 |
| 2 | Jai Bhim | 2021 | 8.6 | 229,264 |
| 3 | Soorarai Pottru | 2020 | 8.6 | 129,501 |
| 4 | Rocketry: The Nambi Effect | 2022 | 8.6 | 61,081 |
| 5 | Parasite | 2019 | 8.5 | 1,099,224 |
| 6 | Dune: Part Two | 2024 | 8.5 | 665,441 |
| 7 | The Kashmir Files | 2022 | 8.5 | 577,307 |
| 8 | Spider-Man: Across the Spider-Verse | 2023 | 8.5 | 479,915 |
| 9 | Sita Ramam | 2022 | 8.5 | 78,638 |
| 10 | Avengers: Endgame | 2019 | 8.4 | 1,388,012 |

Highly rated recent releases are strikingly global—Indian dramas occupy four of the top five slots, while genre blockbusters like *Dune: Part Two* and *Spider-Man: Across the Spider-Verse* show that crowd-pleasing tentpoles can earn elite scores when they resonate widely.【F:analysis/results.json†L74-L145】

### Ratings have been drifting downward

Grouping well-voted films (≥10k votes) by decade shows a steady drop in mean ratings: from 7.82 in the 1920s down to 6.33 in the 2020s, despite runtimes holding near two hours. Production volume also exploded—from 30 films in the 1920s to 3,700+ in the 2010s—suggesting that the long tail of modern releases pulls averages down.【F:analysis/results.json†L146-L212】

A yearly view for popular movies (≥5k votes) since 1980 confirms the slide: average scores were around 6.7 in the early 1980s but hover near 6.2 after 2020, even as the number of widely rated titles surpasses 500 per year.【F:analysis/results.json†L458-L733】

### Runtime matters

Longer movies receive better audience scores. Sub-90-minute releases average 6.12, while films running 180+ minutes climb to 6.93. Viewers also award more votes to longer features—the median title in the 150–179 minute band earns 180 votes versus just 45 votes for short features—indicating deeper engagement with epic runtimes.【F:analysis/results.json†L214-L243】

### Genre winners

Among films with at least 50k votes, Westerns (7.55) and War stories (7.55) lead the pack, followed closely by documentaries (7.49) and biographies (7.33). Even broader genres like Animation and Drama stay above 7.1 when they draw substantial audiences—the drama category alone amasses 445 million votes across 2,262 titles.【F:analysis/results.json†L246-L295】

### Screen format perspectives

Heavily rated TV series average 7.79, comfortably above the 6.67 average for comparably popular movies. Single standout TV episodes (≥20k votes) soar even higher at 8.72, reflecting how franchise high points inspire fans to vote. Video games are an outlier with a 9.01 average across 40 releases, showing the enthusiasm of the gaming audience.【F:analysis/results.json†L394-L455】

## Generated outputs

Running the script produces:

- `analysis/results.json` – machine-readable aggregates covering top films, genre performance, runtime groups, and yearly trends.【F:analysis/results.json†L1-L735】
- `analysis/output.json` – a console capture of the same JSON payload (useful for quick inspection).【F:analysis/output.json†L1-L737】

Feel free to adapt `analysis/imdb_analysis.py` to explore other slices of the IMDb universe, such as specific countries or additional title types.【F:analysis/imdb_analysis.py†L83-L217】
