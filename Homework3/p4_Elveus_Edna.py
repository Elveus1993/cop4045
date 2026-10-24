"""Non-interactive text editor (Problem 4).

File name note: the handout header says "p1_Elveus_Edna.py", which is
a typo. The correct file is "p4_Elveus_Edna.py".

Spec issues resolved and documented:

* `from` is a Python reserved keyword and cannot be a parameter name.
  ed_read uses `start` instead, with the same meaning as the spec's
  `from`.

* File I/O errors (FileNotFoundError, IOError) are NOT caught. The
  spec says these functions "should not catch (except:)" file I/O
  errors; they propagate to the caller. No try/except wraps any
  open/read/write in this module.

* The handout mentions test_ed_write; there is no ed_write function.
  That name only illustrates the test-naming pattern. Our tests are
  test_ed_find and test_ed_replace.

* Overlapping matches: ed_find uses non-overlapping matching, so
  "aa" in "aaa" gives [0], not [0, 1]. This matches str.find.

* Empty search_str: ed_find and ed_replace raise ValueError.

* Negative occurrence other than -1: ed_replace raises ValueError.

* ed_read with start > to returns "" (empty half-open range).
  Negative start raises ValueError. to < -1 raises ValueError.
  start or to greater than len(content) raises IndexError.
  start == len(content) with to == -1 (or to == len) returns "".

* Encoding and newlines: every open() uses encoding="utf-8" and
  newline="". The latter disables Windows text-mode \r\n -> \n
  translation so that indices and character counts are consistent
  across platforms.

* Atomicity: all validation and computation happen before any write.
  The file is opened for writing only after every check has passed
  and the new content string is fully built. A write that fails
  halfway through cannot be made fully atomic without a rename trick,
  which is outside this assignment's scope; that is documented as a
  limitation.

* ed_append returns the number of CHARACTERS written, not bytes.
  With UTF-8, "é" is 1 character but 2 bytes; we return 1.

* ed_append creates the file if it does not exist (open mode 'a').
  ed_read, ed_find, and ed_replace raise FileNotFoundError from
  open('r') if the file is missing, and never modify the file.
"""

import os
import tempfile
from typing import List


def testif(
    b: bool,
    testname: str,
    msgOK: str = "",
    msgFailed: str = "",
) -> bool:
    """Test function that prints Success/Failed based on the result.

    Args:
        b (bool): The test result.
        testname (str): Name of the test.
        msgOK (str): Message to print if the test passes.
        msgFailed (str): Message to print if the test fails.

    Returns:
        bool: The value of b.
    """
    if b:
        print("Success: " + testname + "; " + msgOK)
    else:
        print("Failed: " + testname + "; " + msgFailed)
    return b


def ed_read(filename: str, start: int = 0, to: int = -1) -> str:
    """Read a half-open range [start, to) from a UTF-8 file.

    Args:
        filename (str): Path to the file.
        start (int): First character index to include (0-based).
        to (int): One-past-the-last character index to include;
            -1 means "to the end of the file".

    Returns:
        str: The substring content[start:to].

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If start < 0, or to < -1.
        IndexError: If start > len(content) or to > len(content).

    Preconditions:
        filename names a readable UTF-8 file; start is an int;
        to is an int >= -1.

    Postconditions:
        The file is unchanged. Returns a str; returns "" if
        start >= to after validation.
    """
    with open(filename, "r", encoding="utf-8", newline="") as f:
        content = f.read()

    if start < 0:
        raise ValueError("start must be non-negative")
    if to == -1:
        to = len(content)
    elif to < -1:
        raise ValueError("to must be >= -1")
    if start > len(content):
        raise IndexError(
            f"start={start} exceeds file length {len(content)}")
    if to > len(content):
        raise IndexError(
            f"to={to} exceeds file length {len(content)}")
    if start > to:
        return ""
    return content[start:to]


def ed_find(filename: str, search_str: str) -> List[int]:
    """Find all non-overlapping occurrences of search_str.

    Args:
        filename (str): Path to the file.
        search_str (str): Non-empty string to search for.

    Returns:
        List[int]: 0-based starting indices, in increasing order.
            Empty list if search_str does not occur.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If search_str is empty.

    Preconditions:
        filename names a readable UTF-8 file; search_str is non-empty.

    Postconditions:
        The file is unchanged. Returns a list of ints.
    """
    if search_str == "":
        raise ValueError("search_str must be non-empty")
    with open(filename, "r", encoding="utf-8", newline="") as f:
        content = f.read()
    positions: List[int] = []
    pos = 0
    while True:
        pos = content.find(search_str, pos)
        if pos == -1:
            break
        positions.append(pos)
        pos += len(search_str)  # non-overlapping
    return positions


def ed_replace(
    filename: str,
    search_str: str,
    replace_with: str,
    occurrence: int = -1,
) -> int:
    """Replace one or all non-overlapping occurrences.

    Args:
        filename (str): Path to the file.
        search_str (str): Non-empty string to search for.
        replace_with (str): Replacement string.
        occurrence (int): -1 replaces all occurrences; >= 0 replaces
            only that occurrence (0 is the first).

    Returns:
        int: The number of replacements made.

    Raises:
        FileNotFoundError: If the file does not exist (from ed_find).
        ValueError: If search_str is empty, or occurrence < -1.

    Preconditions:
        filename names a readable UTF-8 file; search_str is non-empty;
        occurrence is -1 or >= 0.

    Postconditions:
        If at least one replacement was made, the file has been
        overwritten with the new content. If occurrence >= number of
        matches, the file is unchanged. Returns an int.
    """
    if search_str == "":
        raise ValueError("search_str must be non-empty")
    if occurrence < -1:
        raise ValueError("occurrence must be -1 or >= 0")

    positions = ed_find(filename, search_str)
    if occurrence == -1:
        targets = positions
    else:
        if occurrence >= len(positions):
            return 0
        targets = [positions[occurrence]]
    if not targets:
        return 0

    with open(filename, "r", encoding="utf-8", newline="") as f:
        content = f.read()
    new_content = content
    # Replace from right to left so earlier indices stay valid.
    for pos in reversed(targets):
        new_content = (
            new_content[:pos]
            + replace_with
            + new_content[pos + len(search_str):]
        )
    with open(filename, "w", encoding="utf-8", newline="") as f:
        f.write(new_content)
    return len(targets)


def ed_append(filename: str, string: str) -> int:
    """Append string to the file, creating it if needed.

    Args:
        filename (str): Path to the file (created if absent).
        string (str): Content to append.

    Returns:
        int: The number of CHARACTERS written (not bytes). With
            UTF-8, "é" is 1 character but 2 bytes; we return 1.

    Raises:
        TypeError: If string is not a str.

    Preconditions:
        filename is a str; string is a str.

    Postconditions:
        The file exists and ends with string. Returns len(string).
    """
    if not isinstance(string, str):
        raise TypeError("string must be a str")
    with open(filename, "a", encoding="utf-8", newline="") as f:
        f.write(string)
    return len(string)


def test_ed_find() -> None:
    """Test ed_find with testif.

    Preconditions:
        The filesystem allows creation of a temp file.

    Postconditions:
        Prints Success/Failed lines; removes the temp file.
    """
    fd, path = tempfile.mkstemp(suffix=".txt")
    os.close(fd)
    try:
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write("01234567890123456789")

        testif(ed_find(path, "345") == [3, 13],
               "ed_find 345", "returns [3, 13]", "wrong positions")
        testif(ed_find(path, "356") == [],
               "ed_find 356", "returns []", "wrong result")
        testif(ed_find(path, "0123") == [0, 10],
               "ed_find 0123", "returns [0, 10]", "wrong result")
        testif(ed_find(path, "89") == [8, 18],
               "ed_find 89", "returns [8, 18]", "wrong result")
        # non-overlapping: "0120120" has "012" at [0, 3], not [0, 3, 1]
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write("0120120")
        testif(ed_find(path, "012") == [0, 3],
               "ed_find non-overlapping",
               "returns [0, 3]", "wrong positions")

        try:
            ed_find(path, "")
            testif(False, "ed_find empty", "", "no exception raised")
        except ValueError:
            testif(True, "ed_find empty", "ValueError raised", "")

        try:
            ed_find(path + ".nonexistent", "a")
            testif(False, "ed_find missing", "", "no exception raised")
        except FileNotFoundError:
            testif(True, "ed_find missing",
                   "FileNotFoundError raised", "")
    finally:
        if os.path.exists(path):
            os.remove(path)


def test_ed_replace() -> None:
    """Test ed_replace with testif.

    Preconditions:
        The filesystem allows creation of a temp file.

    Postconditions:
        Prints Success/Failed lines; removes the temp file.
    """
    fd, path = tempfile.mkstemp(suffix=".txt")
    os.close(fd)
    try:
        # Spec example: replace occurrence 1 (the second occurrence).
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write("01234567890123456789")
        n = ed_replace(path, "345", "ABCDE", 1)
        testif(n == 1, "ed_replace occ=1 count",
               "returns 1", "wrong count")
        with open(path, "r", encoding="utf-8", newline="") as f:
            result = f.read()
        testif(result == "0123456789012ABCDE6789",
               "ed_replace occ=1 content",
               "0123456789012ABCDE6789", "wrong content")

        # Spec example: replace all.
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write("01234567890123456789")
        n = ed_replace(path, "345", "ABCDE", -1)
        testif(n == 2, "ed_replace all count",
               "returns 2", "wrong count")
        with open(path, "r", encoding="utf-8", newline="") as f:
            result = f.read()
        testif(result == "012ABCDE6789012ABCDE6789",
               "ed_replace all content",
               "012ABCDE6789012ABCDE6789", "wrong content")

        # Occurrence 0 (first occurrence).
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write("01234567890123456789")
        n = ed_replace(path, "345", "ZZZ", 0)
        testif(n == 1, "ed_replace occ=0 count",
               "returns 1", "wrong count")
        with open(path, "r", encoding="utf-8", newline="") as f:
            result = f.read()
        testif(result == "012ZZZ67890123456789",
               "ed_replace occ=0 content",
               "012ZZZ67890123456789", "wrong content")

        # Occurrence too large: no change, return 0.
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write("01234567890123456789")
        n = ed_replace(path, "345", "XYZ", 5)
        testif(n == 0, "ed_replace occ too large count",
               "returns 0", "wrong count")
        with open(path, "r", encoding="utf-8", newline="") as f:
            result = f.read()
        testif(result == "01234567890123456789",
               "ed_replace occ too large content",
               "file unchanged", "file changed")

        # Negative occurrence other than -1: ValueError, file unchanged.
        try:
            ed_replace(path, "345", "X", -2)
            testif(False, "ed_replace occ=-2",
                   "", "no exception raised")
        except ValueError:
            testif(True, "ed_replace occ=-2",
                   "ValueError raised", "")
        with open(path, "r", encoding="utf-8", newline="") as f:
            result = f.read()
        testif(result == "01234567890123456789",
               "ed_replace unchanged after ValueError",
               "file unchanged", "file changed")

        # Empty search_str: ValueError.
        try:
            ed_replace(path, "", "X", 0)
            testif(False, "ed_replace empty search",
                   "", "no exception raised")
        except ValueError:
            testif(True, "ed_replace empty search",
                   "ValueError raised", "")
    finally:
        if os.path.exists(path):
            os.remove(path)


def main() -> None:
    """Demonstrate all four ed_ functions and run the automated tests.

    Preconditions:
        The filesystem allows creation of a temp file.

    Postconditions:
        Prints the results of the tests, a demonstration of every
        ed_ function on a known content, and removes the temp file.
    """
    print("=== Automated tests ===")
    test_ed_find()
    test_ed_replace()
    print()

    print("=== Demonstration ===")
    fd, path = tempfile.mkstemp(suffix=".txt")
    os.close(fd)
    # Delete so ed_append demonstrates file creation.
    os.remove(path)
    try:
        # ed_append creates the file and returns character count.
        n = ed_append(path, "01234567890123456789")
        print(f"ed_append('0123...') -> {n} characters")
        print(f"Content: {ed_read(path)!r}")

        # ed_read variants.
        print(f"ed_read(3, 9) = {ed_read(path, 3, 9)!r}")
        print(f"ed_read(3)    = {ed_read(path, 3)!r}")
        print(f"ed_read()     = {ed_read(path)!r}")

        # ed_read raises IndexError on out-of-range; file unchanged.
        before = ed_read(path)
        try:
            ed_read(path, 0, 1000)
        except IndexError as e:
            print(f"ed_read(0, 1000) raised IndexError: {e}")
        after = ed_read(path)
        print(f"File unchanged after IndexError: {before == after}")

        # ed_find examples from the spec.
        print(f"ed_find('345') = {ed_find(path, '345')}")
        print(f"ed_find('356') = {ed_find(path, '356')}")

        # ed_replace: all occurrences.
        count = ed_replace(path, "345", "ABCDE", -1)
        print(f"ed_replace('345', 'ABCDE', -1) -> {count} replacements")
        print(f"Content: {ed_read(path)!r}")

        # ed_replace: one occurrence.
        os.remove(path)
        ed_append(path, "01234567890123456789")
        count = ed_replace(path, "345", "ABCDE", 1)
        print(f"ed_replace('345', 'ABCDE', 1) -> {count} replacement")
        print(f"Content: {ed_read(path)!r}")
    finally:
        if os.path.exists(path):
            os.remove(path)
        print()
        print("Temporary file removed.")


if __name__ == "__main__":
    main()