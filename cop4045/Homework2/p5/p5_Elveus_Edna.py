"""
Problem 5 - Weather Station Analyzer with Coding Agent Help
Homework 2 - CS Assignment

Assembled from six coding-agent (Copilot) prompts/responses:
    (a) read_observations
    (b) station_statistics
    (c) station_outliers
    (d) write_statistics
    (e) unittest suite -- kept in a separate test file, not here
    (f) main()
"""

import datetime
import sys


def read_observations(filename):
    """Read daily temperature observations for weather stations.

    Each line in filename has format: station,date,temperature
    date is an ordinary string like "09:28:09 AM 04/20/2026".
    temperature is a float valid only if -100.0 <= temperature <= 150.0.

    Args:
        filename: path to the input file.

    Returns:
        tuple: (observations, errors)
            observations: dict mapping station -> list of
                (date_string, temperature) tuples, sorted by date.
            errors: list of (line_number, error_message) tuples.
    """
    observations = {}
    errors = []
    seen = set()  # track duplicates using parsed datetime

    with open(filename, 'r') as f:
        for line_number, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                errors.append((line_number, "Empty line"))
                continue

            parts = line.split(',')
            if len(parts) != 3:
                errors.append((line_number, "Malformed line"))
                continue

            station, date_str, temp_str = parts

            # Parse temperature
            try:
                temperature = float(temp_str)
            except ValueError:
                errors.append((line_number, "Invalid temperature format"))
                continue

            if not (-100.0 <= temperature <= 150.0):
                errors.append((line_number, "Temperature out of range"))
                continue

            # Parse date for validation and sorting
            try:
                date_obj = datetime.datetime.strptime(
                    date_str, "%I:%M:%S %p %m/%d/%Y"
                )
            except ValueError:
                errors.append((line_number, "Invalid date format"))
                continue

            # Check duplicates
            key = (station, date_obj)
            if key in seen:
                errors.append((line_number, "Duplicate station/date"))
                continue
            seen.add(key)

            # Store original date string with temperature
            if station not in observations:
                observations[station] = []
            observations[station].append((date_str, temperature))

    # Sort each station's list by parsed datetime, but keep original string
    for station in observations:
        observations[station].sort(
            key=lambda x: datetime.datetime.strptime(
                x[0], "%I:%M:%S %p %m/%d/%Y"
            )
        )

    return observations, errors


def station_statistics(observations):
    """Compute min, max, and mean temperature for each station.

    Args:
        observations: dict mapping station -> list of
            (date_string, temperature) tuples.

    Returns:
        dict: station -> {"min": float, "max": float, "mean": float}.
    """
    stats = {}

    for station, records in observations.items():
        if not records:
            # Handle case where station has no valid records
            stats[station] = {
                "min": None,
                "max": None,
                "mean": None
            }
            continue

        temps = [temp for _, temp in records]
        min_temp = min(temps)
        max_temp = max(temps)
        mean_temp = sum(temps) / len(temps)

        stats[station] = {
            "min": min_temp,
            "max": max_temp,
            "mean": mean_temp
        }

    return stats


def station_outliers(observations):
    """Identify stations whose latest temperature exceeds their mean.

    Uses station_statistics and a dictionary comprehension.

    Args:
        observations: dict mapping station -> list of
            (date_string, temperature) tuples, sorted by date.

    Returns:
        dict: outlying station -> (date, temperature, mean) tuple.
    """
    stats = station_statistics(observations)
    return {
        station: (latest[0], latest[1], stats[station]["mean"])
        for station, records in observations.items()
        if records and (latest := records[-1])[1] > stats[station]["mean"]
    }


def write_statistics(filename, statistics):
    """Write station statistics to a file.

    Stations are written in lexicographic order. Numeric values are
    formatted with exactly one digit after the decimal point.

    Args:
        filename: path to the output file.
        statistics: dict from station_statistics.

    Returns:
        None
    """
    with open(filename, 'w') as f:
        for station in sorted(statistics.keys()):
            stats = statistics[station]
            min_val = (
                f"{stats['min']:.1f}" if stats['min'] is not None else "None"
            )
            max_val = (
                f"{stats['max']:.1f}" if stats['max'] is not None else "None"
            )
            mean_val = (
                f"{stats['mean']:.1f}" if stats['mean'] is not None
                else "None"
            )

            f.write(f"{station},{min_val},{max_val},{mean_val}\n")


def main():
    """Read observations file and output filename from sys.argv, print
    statistics and outliers, and write statistics to the output file.

    Catches file access errors gracefully and exits with a nonzero
    status code on failure.

    Returns:
        None
    """
    if len(sys.argv) != 3:
        print("Usage: python weather.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    try:
        observations, errors = read_observations(input_file)
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(2)
    except PermissionError:
        print(f"Error: Permission denied when accessing '{input_file}'.")
        sys.exit(3)
    except Exception as e:
        print(f"Unexpected error reading '{input_file}': {e}")
        sys.exit(4)

    # Print errors if any
    if errors:
        print("Errors encountered while reading observations:")
        for line_num, msg in errors:
            print(f"  Line {line_num}: {msg}")

    # Compute statistics and outliers
    statistics = station_statistics(observations)
    outliers = station_outliers(observations)

    print("\nStation Statistics:")
    for station in sorted(statistics.keys()):
        stats = statistics[station]
        if stats['min'] is not None:
            print(
                f"{station}: min={stats['min']:.1f} "
                f"max={stats['max']:.1f} mean={stats['mean']:.1f}"
            )
        else:
            print(f"{station}: No valid data")

    print("\nOutliers (latest temp > mean):")
    if outliers:
        for station, (date, temp, mean) in outliers.items():
            print(f"{station}: latest={temp:.1f} (on {date}), mean={mean:.1f}")
    else:
        print("None")

    # Write statistics to output file
    try:
        write_statistics(output_file, statistics)
        print(f"\nStatistics written to '{output_file}'")
    except PermissionError:
        print(f"Error: Permission denied when writing to '{output_file}'.")
        sys.exit(5)
    except Exception as e:
        print(f"Unexpected error writing '{output_file}': {e}")
        sys.exit(6)

    sys.exit(0)


if __name__ == "__main__":
    main()