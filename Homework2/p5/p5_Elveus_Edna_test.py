import unittest
import tempfile
import os
from p5_Elveus_Edna import (
    read_observations,
    station_statistics,
    station_outliers,
    write_statistics,
)

class TestWeatherFunctions(unittest.TestCase):

    def test_multiple_stations_and_negative_temps(self):
        data = """StationA,09:28:09 AM 04/20/2026,72.5
StationB,10:15:00 AM 04/19/2026,-20.0
"""
        with tempfile.NamedTemporaryFile(delete=False, mode='w') as tmp:
            tmp.write(data)
            fname = tmp.name
        obs, errs = read_observations(fname)
        os.remove(fname)
        self.assertEqual(len(errs), 0)
        self.assertIn("StationA", obs)
        self.assertIn("StationB", obs)
        self.assertEqual(obs["StationB"][0][1], -20.0)

    def test_duplicate_observations(self):
        data = """StationA,09:28:09 AM 04/20/2026,72.5
StationA,09:28:09 AM 04/20/2026,73.0
"""
        with tempfile.NamedTemporaryFile(delete=False, mode='w') as tmp:
            tmp.write(data)
            fname = tmp.name
        obs, errs = read_observations(fname)
        os.remove(fname)
        self.assertEqual(len(obs["StationA"]), 1)
        self.assertTrue(any("Duplicate" in msg for _, msg in errs))

    def test_invalid_temperature_range(self):
        data = "StationA,09:28:09 AM 04/20/2026,200.0\n"
        with tempfile.NamedTemporaryFile(delete=False, mode='w') as tmp:
            tmp.write(data)
            fname = tmp.name
        obs, errs = read_observations(fname)
        os.remove(fname)
        self.assertEqual(len(obs), 0)
        self.assertTrue(any("out of range" in msg for _, msg in errs))

    def test_statistics_calculation(self):
        observations = {
            "StationA": [
                ("09:28:09 AM 04/20/2026", 72.5),
                ("10:15:00 AM 04/19/2026", 70.0)
            ]
        }
        stats = station_statistics(observations)
        self.assertEqual(stats["StationA"]["min"], 70.0)
        self.assertEqual(stats["StationA"]["max"], 72.5)
        self.assertAlmostEqual(stats["StationA"]["mean"], 71.25)

    def test_outliers_detection(self):
        observations = {
            "StationA": [
                ("10:15:00 AM 04/19/2026", 70.0),
                ("09:28:09 AM 04/20/2026", 72.5)
            ],
            "StationB": [
                ("11:00:00 AM 04/20/2026", 85.0)
            ]
        }
        outliers = station_outliers(observations)
        self.assertIn("StationA", outliers)
        self.assertNotIn("StationB", outliers)

    def test_write_statistics_sorted_output(self):
        stats = {
            "StationB": {"min": 85.0, "max": 85.0, "mean": 85.0},
            "StationA": {"min": 70.0, "max": 72.5, "mean": 71.25}
        }
        with tempfile.NamedTemporaryFile(delete=False, mode='w') as tmp:
            fname = tmp.name
        write_statistics(fname, stats)
        with open(fname, 'r') as f:
            lines = f.readlines()
        os.remove(fname)
        # Ensure lexicographic order
        self.assertTrue(lines[0].startswith("StationA"))
        self.assertTrue(lines[1].startswith("StationB"))
        # Ensure one decimal place formatting
        self.assertIn("71.2", lines[0])

    def test_missing_input_file(self):
        fname = "nonexistent_file.txt"
        with self.assertRaises(FileNotFoundError):
            read_observations(fname)


if __name__ == "__main__":
    unittest.main()
