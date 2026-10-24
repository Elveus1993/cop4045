"""Tests for file search and absolute paths."""

import unittest
from typing import List

from p6_Elveus_Edna import Entry, File, Folder, find_large_files


class FindLargeFilesTest(unittest.TestCase):
    """Test recursive file search behavior."""

    def setUp(self) -> None:
        """Create a fresh nested tree for each test."""
        self.root = Folder("root")
        self.parent_folder = Folder("parent")
        self.folder = Folder("folder")
        self.deepest_folder = Folder("deepest")
        self.root_file = File("root_file", 10)
        self.parent_file = File("parent_file", 7)
        self.folder_file = File("folder_file", 8)
        self.deep_file = File("deep_file", 12)
        self.small_file = File("small_file", 2)
        self.after_file = File("after_file", 4)

        self.root.add(self.root_file)
        self.root.add(self.parent_folder)
        self.root.add(self.after_file)
        self.parent_folder.add(self.parent_file)
        self.parent_folder.add(self.folder)
        self.folder.add(self.folder_file)
        self.folder.add(self.deepest_folder)
        self.deepest_folder.add(self.deep_file)
        self.deepest_folder.add(self.small_file)

    def test_file_threshold_includes_or_excludes_file(self) -> None:
        """Include a file above threshold and exclude one below."""
        self.assertEqual(
            find_large_files(self.root_file, 10),
            [self.root_file],
        )
        self.assertEqual(find_large_files(self.root_file, 11), [])

    def test_file_equal_to_threshold_is_included(self) -> None:
        """Include a file whose size equals the threshold."""
        self.assertEqual(
            find_large_files(self.folder_file, 8),
            [self.folder_file],
        )

    def test_folder_search_is_depth_first(self) -> None:
        """Find qualifying files in depth-first child order."""
        expected = [
            self.root_file,
            self.parent_file,
            self.folder_file,
            self.deep_file,
        ]
        results = find_large_files(self.root, 7)
        self.assertEqual(results, expected)
        self.assertTrue(all(isinstance(entry, File) for entry in results))
        self.assertNotIn(self.parent_folder, results)
        self.assertNotIn(self.folder, results)
        self.assertNotIn(self.deepest_folder, results)

    def test_thresholds_on_same_tree_return_different_lists(self) -> None:
        """Return different exact results for two thresholds."""
        self.assertEqual(
            find_large_files(self.root, 8),
            [self.root_file, self.folder_file, self.deep_file],
        )
        self.assertEqual(
            find_large_files(self.root, 11),
            [self.deep_file],
        )

    def test_empty_folder_returns_empty_list(self) -> None:
        """Return no files when searching an empty folder."""
        empty_folder = Folder("empty")
        self.assertEqual(find_large_files(empty_folder, 0), [])

    def test_invalid_inputs_raise_expected_errors(self) -> None:
        """Reject negative thresholds and non-entry arguments."""
        with self.assertRaises(ValueError):
            find_large_files(self.root, -1)
        with self.assertRaises(TypeError):
            find_large_files("not an entry", 0)


class AbsolutePathTest(unittest.TestCase):
    """Test paths from entries to their root."""

    def setUp(self) -> None:
        """Create a fresh entry hierarchy for each test."""
        self.root = Folder("root")
        self.parent_folder = Folder("parent")
        self.folder = Folder("folder")
        self.file = File("file", 5)
        self.root.add(self.parent_folder)
        self.parent_folder.add(self.folder)
        self.folder.add(self.file)

    def test_root_path_contains_only_root(self) -> None:
        """Return only the root for a root entry."""
        self.assertEqual(self.root.absolute_path(), [self.root])

    def test_file_path_lists_ancestors_in_order(self) -> None:
        """Return the file followed by its folders and root."""
        path: List[Entry] = self.file.absolute_path()
        self.assertEqual(
            len(path),
            4,
        )
        self.assertIs(path[0], self.file)
        self.assertIs(path[1], self.folder)
        self.assertIs(path[2], self.parent_folder)
        self.assertIs(path[3], self.root)

    def test_file_and_folder_inherit_absolute_path(self) -> None:
        """Provide absolute_path on both File and Folder."""
        self.assertEqual(
            self.file.absolute_path(),
            [self.file, self.folder, self.parent_folder, self.root],
        )
        self.assertEqual(
            self.folder.absolute_path(),
            [self.folder, self.parent_folder, self.root],
        )

    def test_paths_end_at_root_with_depth_based_length(self) -> None:
        """End each path at root with the expected path length."""
        paths_and_lengths = [
            (self.root.absolute_path(), 1),
            (self.parent_folder.absolute_path(), 2),
            (self.folder.absolute_path(), 3),
            (self.file.absolute_path(), 4),
        ]
        for path, expected_length in paths_and_lengths:
            self.assertIs(path[-1], self.root)
            self.assertEqual(len(path), expected_length)


if __name__ == "__main__":
    unittest.main()

