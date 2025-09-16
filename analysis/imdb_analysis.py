import json
from pathlib import Path
from typing import Dict, Any

import pandas as pd

DATA_URLS = {
    "title.basics.tsv.gz": "https://datasets.imdbws.com/title.basics.tsv.gz",
    "title.ratings.tsv.gz": "https://datasets.imdbws.com/title.ratings.tsv.gz",
}

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
OUTPUT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)


def download_data() -> None:
    import urllib.request

    for filename, url in DATA_URLS.items():
        path = DATA_DIR / filename
        if not path.exists():
            print(f"Downloading {filename}...")
            urllib.request.urlretrieve(url, path)
        else:
            print(f"Found cached {filename}")


def load_data() -> Dict[str, pd.DataFrame]:
    basics = pd.read_csv(
        DATA_DIR / "title.basics.tsv.gz",
        sep="\t",
        na_values="\\N",
        compression="gzip",
        dtype={
            "tconst": "string",
            "titleType": "category",
            "primaryTitle": "string",
            "originalTitle": "string",
            "isAdult": "Int64",
            "startYear": "string",
            "endYear": "string",
            "runtimeMinutes": "string",
            "genres": "string",
        },
        usecols=[
            "tconst",
            "titleType",
            "primaryTitle",
            "originalTitle",
            "isAdult",
            "startYear",
            "runtimeMinutes",
            "genres",
        ],
        low_memory=False,
    )

    ratings = pd.read_csv(
        DATA_DIR / "title.ratings.tsv.gz",
        sep="\t",
        na_values="\\N",
        compression="gzip",
        dtype={
            "tconst": "string",
            "averageRating": "float64",
            "numVotes": "int64",
        },
    )

    basics["startYear"] = pd.to_numeric(basics["startYear"], errors="coerce")
    basics["runtimeMinutes"] = pd.to_numeric(basics["runtimeMinutes"], errors="coerce")

    merged = basics.merge(ratings, on="tconst", how="inner")
    merged = merged[merged["isAdult"].isna() | (merged["isAdult"] == 0)]
    merged = merged.drop(columns=["isAdult"])
    merged = merged.rename(columns={"primaryTitle": "title"})

    return {"titles": merged}


def top_movies(df: pd.DataFrame, min_votes: int = 100_000, top_n: int = 10) -> pd.DataFrame:
    movies = df[df["titleType"] == "movie"].copy()
    movies = movies[movies["numVotes"] >= min_votes]
    movies = movies.dropna(subset=["startYear"])
    movies = movies.sort_values(by=["averageRating", "numVotes"], ascending=[False, False])
    return movies[["title", "startYear", "averageRating", "numVotes", "genres"]].head(top_n)


def top_recent_movies(
    df: pd.DataFrame, start_year: int = 2015, min_votes: int = 50_000, top_n: int = 10
) -> pd.DataFrame:
    movies = df[df["titleType"] == "movie"].copy()
    movies = movies[(movies["startYear"] >= start_year) & (movies["numVotes"] >= min_votes)]
    movies = movies.sort_values(by=["averageRating", "numVotes"], ascending=[False, False])
    return movies[["title", "startYear", "averageRating", "numVotes", "genres"]].head(top_n)


def movies_by_decade(df: pd.DataFrame, min_votes: int = 10_000) -> pd.DataFrame:
    movies = df[(df["titleType"] == "movie") & (df["numVotes"] >= min_votes)].copy()
    movies = movies.dropna(subset=["startYear"])
    movies["decade"] = (movies["startYear"] // 10) * 10
    movies = movies.dropna(subset=["decade"])
    stats = (
        movies.groupby("decade")
        .agg(
            avg_rating=("averageRating", "mean"),
            median_runtime=("runtimeMinutes", "median"),
            count=("tconst", "count"),
        )
        .sort_index()
    )
    stats = stats[stats.index >= 1920]
    stats.index = stats.index.astype("int64")
    return stats


def runtime_vs_rating(df: pd.DataFrame) -> pd.DataFrame:
    movies = df[(df["titleType"] == "movie") & df["runtimeMinutes"].notna()].copy()
    bins = [0, 90, 120, 150, 180, float("inf")]
    labels = ["<90 min", "90-119 min", "120-149 min", "150-179 min", "180+ min"]
    movies["runtime_bin"] = pd.cut(movies["runtimeMinutes"], bins=bins, labels=labels, right=False)
    summary = (
        movies.groupby("runtime_bin")
        .agg(
            avg_rating=("averageRating", "mean"),
            median_votes=("numVotes", "median"),
            count=("tconst", "count"),
        )
        .dropna()
    )
    return summary


def genre_performance(df: pd.DataFrame, min_votes: int = 50_000) -> pd.DataFrame:
    movies = df[(df["titleType"] == "movie") & (df["numVotes"] >= min_votes)].copy()
    movies = movies[movies["genres"].notna()]
    exploded = movies.assign(genre=movies["genres"].str.split(",")).explode("genre")
    summary = (
        exploded.groupby("genre")
        .agg(
            avg_rating=("averageRating", "mean"),
            median_year=("startYear", "median"),
            title_count=("tconst", "count"),
            total_votes=("numVotes", "sum"),
        )
        .sort_values(by="avg_rating", ascending=False)
    )
    summary = summary[summary["title_count"] >= 20]
    return summary


def tv_vs_movies(df: pd.DataFrame, min_votes: int = 20_000) -> pd.DataFrame:
    subset = df[df["numVotes"] >= min_votes]
    summary = (
        subset.groupby("titleType")
        .agg(
            avg_rating=("averageRating", "mean"),
            median_votes=("numVotes", "median"),
            count=("tconst", "count"),
        )
        .sort_values(by="count", ascending=False)
    )
    summary = summary[summary["count"] > 0]
    return summary


def yearly_rating_trend(df: pd.DataFrame, start_year: int = 1980, min_votes: int = 5_000) -> pd.DataFrame:
    movies = df[(df["titleType"] == "movie") & (df["numVotes"] >= min_votes)].copy()
    movies = movies.dropna(subset=["startYear"])
    movies = movies[movies["startYear"] >= start_year]
    summary = (
        movies.groupby("startYear")
        .agg(
            avg_rating=("averageRating", "mean"),
            median_votes=("numVotes", "median"),
            count=("tconst", "count"),
        )
        .sort_index()
    )
    summary.index = summary.index.astype("int64")
    return summary


def run_analysis() -> Dict[str, Any]:
    download_data()
    data = load_data()
    titles = data["titles"]

    results: Dict[str, Any] = {}

    top_movies_df = top_movies(titles)
    results["top_movies"] = top_movies_df.to_dict(orient="records")

    recent_movies_df = top_recent_movies(titles)
    results["top_recent_movies"] = recent_movies_df.to_dict(orient="records")

    decade_stats_df = movies_by_decade(titles)
    results["movies_by_decade"] = decade_stats_df.reset_index().to_dict(orient="records")

    runtime_df = runtime_vs_rating(titles)
    results["runtime_vs_rating"] = runtime_df.reset_index().to_dict(orient="records")

    genre_df = genre_performance(titles)
    results["genre_performance"] = genre_df.reset_index().to_dict(orient="records")

    tv_vs_movies_df = tv_vs_movies(titles)
    results["tv_vs_movies"] = tv_vs_movies_df.reset_index().to_dict(orient="records")

    yearly_trend_df = yearly_rating_trend(titles)
    results["yearly_rating_trend"] = yearly_trend_df.reset_index().to_dict(orient="records")

    output_path = OUTPUT_DIR / "results.json"
    output_path.write_text(json.dumps(results, indent=2))
    print(json.dumps(results, indent=2))
    return results


if __name__ == "__main__":
    run_analysis()
