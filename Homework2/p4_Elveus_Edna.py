"""
Problem 4 - IMDB Movie Data Analysis
Homework 2 - CS Assignment

Analyzes IMDB top-rated and top-grossing data against a casts file to
find director/actor collaborations and top-grossing actors.

Note: The assignment doc lists the filename as p3_Lastname_Firstname.py,
but that conflicts with Problem 3. Using p4_Lastname_Firstname.py instead.

Data files are expected in a 'data_files' folder:
    data_files/imdb-top-rated.csv
    data_files/imdb-top-grossing.csv
    data_files/imdb-top-casts.csv

Top-down design: both parts (a) and (b) share two subproblems:
    1. Load a CSV file into a lookup dict keyed by (title, year).
    2. Walk the casts file and cross-reference each movie against a lookup.
Helper functions are provided for both patterns so (a) and (b) stay
short and focused on their own aggregation logic.
"""

import csv


# ---------------------------------------------------------------- helpers

def load_csv_lookup(filename: str, value_column: str) -> dict:
    """
    Load a CSV with a (title, year) key into a dict.

    Assumes columns: Rank, Title, Year, <value_column>.

    Args:
        filename: Path to the CSV file.
        value_column: Name of the 4th column to use as the dict value.

    Returns:
        dict: Mapping (title, year) -> value from value_column.
              Year is stored as int, value as float.

    Raises:
        Exception: Re-raises any exception after printing a friendly message.
    """
    try:
        lookup = {}
        with open(filename, 'r', encoding='utf-8', newline='') as infile:
            reader = csv.DictReader(infile)
            for row in reader:
                key = (row['Title'].strip(), int(row['Year']))
                lookup[key] = float(row[value_column])
        return lookup
    except Exception as e:
        print(f"Error loading '{filename}': {e}")
        raise


def iter_casts(filename: str):
    """
    Yield parsed rows from the casts CSV.

    The casts file has no header. Columns:
        Title, Year, Director, Actor1..Actor5

    Args:
        filename: Path to the casts CSV.

    Yields:
        tuple: (title, year, director, [actor1..actor5])

    Raises:
        Exception: Re-raises any exception after printing a friendly message.
    """
    try:
        with open(filename, 'r', encoding='utf-8', newline='') as infile:
            reader = csv.reader(infile)
            for row in reader:
                if len(row) < 3:
                    continue
                title = row[0].strip()
                year = int(row[1])
                director = row[2].strip()
                actors = [a.strip() for a in row[3:] if a.strip()]
                yield (title, year, director, actors)
    except Exception as e:
        print(f"Error reading '{filename}': {e}")
        raise


def display_ranked(title: str, rows: list, limit=None) -> None:
    """
    Print a ranked list of results.

    Args:
        title: Header text for the list.
        rows: List of (label, count) tuples, already sorted descending.
        limit: Optional int; if given, only the first `limit` rows print.

    Returns:
        None
    """
    print(title)
    print("-" * len(title))
    shown = rows if limit is None else rows[:limit]
    for i, (label, count) in enumerate(shown, start=1):
        print(f"{i:3d}. {label}  ({count})")
    if limit is not None and len(rows) > limit:
        print(f"  ... ({len(rows) - limit} more)")
    print()


# ------------------------------------------------------------ part (a)

def display_top_collaborations(
    rated_file: str,
    casts_file: str,
    limit=None
) -> None:
    """
    Display director/actor pairs ranked by number of top-rated films.

    A "collaboration" is counted once for each (director, actor) pair
    appearing in the same qualifying movie. A movie with 5 actors
    contributes 5 collaborations.

    Args:
        rated_file: Path to imdb-top-rated.csv.
        casts_file: Path to imdb-top-casts.csv.
        limit: Optional int to truncate the displayed list.

    Returns:
        None

    Raises:
        Exception: Re-raises exceptions from the loading helpers.
    """
    try:
        # Subproblem 1: load top-rated into a lookup keyed by (title, year)
        rated_lookup = load_csv_lookup(rated_file, 'IMDb Rating')

        # Subproblem 2: walk the casts file, cross-reference each movie,
        # and aggregate (director, actor) pair counts.
        collab_counts = {}
        for title, year, director, actors in iter_casts(casts_file):
            if (title, year) not in rated_lookup:
                continue
            for actor in actors:
                pair = (director, actor)
                collab_counts[pair] = collab_counts.get(pair, 0) + 1

        # Sort descending by count
        ranked = sorted(
            collab_counts.items(),
            key=lambda item: item[1],
            reverse=True
        )
        rows = [(f"{d} + {a}", c) for (d, a), c in ranked]

        display_ranked(
            "Top Director/Actor Collaborations (top-rated films)",
            rows,
            limit=limit
        )
    except Exception as e:
        print(f"Error in display_top_collaborations: {e}")
        raise


# ------------------------------------------------------------ part (b)

def display_top_actors(
    grossing_file: str,
    casts_file: str,
    limit=None
) -> None:
    """
    Display actors ranked by total USA box office across top-grossing films.

    For each movie in the casts file that also appears in the top-grossing
    lookup, that movie's USA box office is credited to every listed actor.

    Args:
        grossing_file: Path to imdb-top-grossing.csv.
        casts_file: Path to imdb-top-casts.csv.
        limit: Optional int to truncate the displayed list.

    Returns:
        None

    Raises:
        Exception: Re-raises exceptions from the loading helpers.
    """
    try:
        # Subproblem 1: load top-grossing into a lookup keyed by (title, year)
        grossing_lookup = load_csv_lookup(grossing_file, 'USA Box Office')

        # Subproblem 2: walk the casts file, cross-reference each movie,
        # and aggregate box office per actor.
        actor_totals = {}
        for title, year, director, actors in iter_casts(casts_file):
            key = (title, year)
            if key not in grossing_lookup:
                continue
            box_office = grossing_lookup[key]
            for actor in actors:
                actor_totals[actor] = actor_totals.get(actor, 0.0) + box_office

        # Sort descending by total box office
        ranked = sorted(
            actor_totals.items(),
            key=lambda item: item[1],
            reverse=True
        )
        rows = [(actor, f"${total:,.0f}") for actor, total in ranked]

        display_ranked(
            "Top Actors by USA Box Office (top-grossing films)",
            rows,
            limit=limit
        )
    except Exception as e:
        print(f"Error in display_top_actors: {e}")
        raise


# ------------------------------------------------------------ part (c)

def main() -> None:
    """
    Test parts (a) and (b) on the IMDB data files.

    Returns:
        None
    """
    rated_file = 'data_files/imdb-top-rated.csv'
    grossing_file = 'data_files/imdb-top-grossing.csv'
    casts_file = 'data_files/imdb-top-casts.csv'

    print("=" * 60)
    print("PART (a): Top Director/Actor Collaborations")
    print("=" * 60)
    display_top_collaborations(rated_file, casts_file, limit=10)

    print("=" * 60)
    print("PART (b): Top Actors by USA Box Office")
    print("=" * 60)
    display_top_actors(grossing_file, casts_file, limit=10)


if __name__ == "__main__":
    main()