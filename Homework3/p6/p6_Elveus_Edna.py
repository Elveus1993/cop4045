"""Represent entries in a file system hierarchy."""

from __future__ import annotations

from typing import List, Optional, Tuple


class Entry:
    """Represent a named entry with an optional parent.

    Args:
        name: The entry's name.
        parent: The parent entry, or None when this is a root.
    """

    def __init__(self, name: str, parent: Optional[Entry] = None) -> None:
        """Initialize an entry.

        Args:
            name: The entry's name.
            parent: The parent entry, or None when this is a root.
        """
        self.name: str = name
        self._parent: Optional[Entry] = parent

    def parent(self) -> Optional[Entry]:
        """Return the parent entry.

        Returns:
            The parent entry, or None when this is a root.
        """
        return self._parent

    def size(self) -> int:
        """Return the size of this entry.

        Raises:
            NotImplementedError: This method must be implemented by a subclass.
        """
        raise NotImplementedError

    def absolute_path(self) -> List[Entry]:
        """Return this entry and its ancestors up to the root.

        Returns:
            A list starting with this entry and ending with the root.

        Example:
            >>> root = Entry("root")
            >>> child = Entry("child", root)
            >>> [e.name for e in child.absolute_path()]
            ['child', 'root']
        """
        if self._parent is None:
            return [self]
        return [self] + self._parent.absolute_path()


class File(Entry):
    """Represent a file with a fixed size in bytes.

    Args:
        name: The file's name.
        bytes_used: The number of bytes used by the file.
        parent: The parent entry, or None when this is a root.
    """

    def __init__(
        self,
        name: str,
        bytes_used: int,
        parent: Optional[Entry] = None,
    ) -> None:
        """Initialize a file.

        Args:
            name: The file's name.
            bytes_used: The number of bytes used by the file.
            parent: The parent entry, or None when this is a root.

        Raises:
            ValueError: If bytes_used is negative.
        """
        super().__init__(name, parent)
        if bytes_used < 0:
            raise ValueError("bytes_used cannot be negative")
        self.bytes_used: int = bytes_used

    def size(self) -> int:
        """Return the file size in bytes.

        Returns:
            The number of bytes used by the file.
        """
        return self.bytes_used


class Folder(Entry):
    """Represent a folder containing entries.

    Args:
        name: The folder's name.
        parent: The parent entry, or None when this is a root.
    """

    def __init__(self, name: str, parent: Optional[Entry] = None) -> None:
        """Initialize an empty folder.

        Args:
            name: The folder's name.
            parent: The parent entry, or None when this is a root.
        """
        super().__init__(name, parent)
        self._children: List[Entry] = []

    def add(self, entry: Entry) -> None:
        """Add an entry as a child of this folder.

        Args:
            entry: The entry to add.

        Raises:
            TypeError: If entry is not an Entry.
            ValueError: If entry belongs to another parent or is already
                a child of this folder.
        """
        if not isinstance(entry, Entry):
            raise TypeError("entry must be an Entry")
        if entry._parent is not None and entry._parent is not self:
            raise ValueError("entry already has a different parent")
        if any(child is entry for child in self._children):
            raise ValueError("entry is already a child of this folder")
        self._children.append(entry)
        entry._parent = self

    def size(self) -> int:
        """Return the combined size of this folder's children.

        Returns:
            The total size of all children, including nested folders.
        """
        return sum(child.size() for child in self._children)

    def children(self) -> Tuple[Entry, ...]:
        """Return this folder's children as an immutable tuple.

        Returns:
            A new tuple containing all child entries.
        """
        return tuple(self._children)


def find_large_files(entry: Entry, minimum_size: int) -> List[File]:
    """Find files at least the given size, recursively.

    For a File, returns a one-item list if its size is at least
    minimum_size, or an empty list otherwise. For a Folder, recursively
    searches its children in depth-first order and combines their matching
    files; the folder's total size is not compared. An empty Folder returns
    an empty list.

    Args:
        entry: The entry to search.
        minimum_size: The minimum file size to include.

    Returns:
        Matching File objects in depth-first child order.

    Raises:
        TypeError: If entry is not an Entry.
        ValueError: If minimum_size is negative.
    """
    if not isinstance(entry, Entry):
        raise TypeError("entry must be an Entry")
    if minimum_size < 0:
        raise ValueError("minimum_size cannot be negative")

    if isinstance(entry, File):
        if entry.size() >= minimum_size:
            return [entry]
        return []

    if isinstance(entry, Folder):
        matches: List[File] = []
        for child in entry.children():
            matches.extend(find_large_files(child, minimum_size))
        return matches

    return []


def _print_tree(entry: Entry, depth: int = 0) -> None:
    """Print an entry and its descendants with indentation.

    Args:
        entry: The entry to print.
        depth: The current indentation depth.

    Returns:
        None.
    """
    print(f"{'  ' * depth}{entry.name}: {entry.size()} bytes")
    if isinstance(entry, Folder):
        for child in entry.children():
            _print_tree(child, depth + 1)


def _entry_names(entries: List[Entry]) -> List[str]:
    """Return the names of entries.

    Args:
        entries: The entries whose names are returned.

    Returns:
        The entry names in the same order as entries.
    """
    return [entry.name for entry in entries]


def main() -> None:
    """Demonstrate folder sizes, file thresholds, and absolute paths.

    Args:
        None.

    Returns:
        None.
    """
    root: Folder = Folder("root")
    projects: Folder = Folder("projects")
    source: Folder = Folder("source")
    module: Folder = Folder("module")

    root_file: File = File("readme.txt", 100)
    project_file: File = File("notes.txt", 250)
    source_file: File = File("config.txt", 50)
    deep_file: File = File("data.bin", 400)

    root.add(projects)
    root.add(root_file)
    projects.add(source)
    projects.add(project_file)
    source.add(module)
    source.add(source_file)
    module.add(deep_file)

    print("Tree:")
    _print_tree(root)

    print("\nPart f, size:")
    root_size: int = root.size()
    expected_total: int = 100 + 250 + 50 + 400
    print(f"Root size: {root_size} bytes")
    print(f"Expected total (100 + 250 + 50 + 400): {expected_total} bytes")
    print(f"Root size matches expected total: {root_size == expected_total}")
    print(f"Source folder size: {source.size()} bytes")

    print("\nPart f, thresholds:")
    for threshold in (200, 350):
        files: List[File] = find_large_files(root, threshold)
        file_details: List[str] = [
            f"{file_entry.name} ({file_entry.size()} bytes)"
            for file_entry in files
        ]
        print(f"Minimum size {threshold} bytes: {file_details}")

    print("\nPart g, absolute_path:")
    for entry in (deep_file, source, root):
        path_names: List[str] = _entry_names(entry.absolute_path())
        print(f"{entry.name} names: {path_names}")
        print(f"{entry.name} path: {' <- '.join(path_names)}")


if __name__ == "__main__":
    main()
