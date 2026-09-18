"""
Problem 2 - Comprehensions
Homework 2 - CS Assignment

This script demonstrates list and dict comprehensions for six tasks:
(a) Pythagorean-like quadruples
(b) Lowercase + length filter
(c) Name reformatting
(d) Anagram pairs across two lists
(e) Dict comprehension: string -> length
(f) Dict comprehension: vowel positions
"""


def part_a() -> list:
    """
    Return all tuples (a, b, c, d) of distinct integers in [1, 10]
    satisfying a^2 + b^2 = c^2 + d^2.

    Returns:
        list: List of (a, b, c, d) tuples meeting the constraints.
    """
    return [
        (a, b, c, d)
        for a in range(1, 11)
        for b in range(1, 11)
        for c in range(1, 11)
        for d in range(1, 11)
        if a**2 + b**2 == c**2 + d**2
        and len({a, b, c, d}) == 4
    ]


def part_b(words: list) -> list:
    """
    Return (lowercase_word, length) tuples for words shorter than 5 chars.

    Args:
        words: List of strings to filter and transform.

    Returns:
        list: List of (str, int) tuples.
    """
    return [
        (word.lower(), len(word))
        for word in words
        if len(word) < 5
    ]


def part_c(names: list) -> list:
    """
    Reformat full names to 'First M. Last' form.

    Args:
        names: List of 'First Middle Last' formatted strings.

    Returns:
        list: List of reformatted name strings.
    """
    return [
        f"{parts[0]} {parts[1][0]}. {parts[2]}"
        for parts in (name.split() for name in names)
    ]


def part_d(lst1: list, lst2: list) -> list:
    """
    Return (w1, w2) tuples where w1 in lst1 and w2 in lst2 are anagrams
    of each other (case-insensitive).

    Args:
        lst1: First list of words.
        lst2: Second list of words.

    Returns:
        list: List of (str, str) anagram pairs.
    """
    return [
        (w1, w2)
        for w1 in lst1
        for w2 in lst2
        if sorted(w1.lower()) == sorted(w2.lower())
    ]


def part_e(s: list) -> dict:
    """
    Return dict mapping each string in s to its length.

    Args:
        s: List of strings.

    Returns:
        dict: {word: len(word)} mapping.
    """
    return {word: len(word) for word in s}


def part_f(text: str) -> dict:
    """
    Return dict mapping index -> character for each vowel in text
    (case-insensitive).

    Args:
        text: Input string to scan for vowels.

    Returns:
        dict: {index: vowel_char} for every vowel occurrence.
    """
    return {
        index: char
        for index, char in enumerate(text)
        if char.lower() in 'aeiou'
    }


def main() -> None:
    """
    Run all parts and print their results to the terminal.
    """
    # Part (a)
    print("=== Part (a): Pythagorean-like quadruples ===")
    result_a = part_a()
    print(f"Found {len(result_a)} quadruples.")
    for quad in result_a[:10]:  # Show first 10 for readability
        print(f"  {quad}")
    if len(result_a) > 10:
        print(f"  ... ({len(result_a) - 10} more)")
    print()

    # Part (b)
    print("=== Part (b): Lowercase + length filter ===")
    words_b = ['One', 'SEVEN', 'three', 'two', 'Ten']
    print(f"Input: {words_b}")
    print(f"Result: {part_b(words_b)}")
    print()

    # Part (c)
    print("=== Part (c): Name reformatting ===")
    names_c = ['Christopher Ashton Kutcher', 'Elizabeth Stamatina Fey']
    print(f"Input: {names_c}")
    print(f"Result: {part_c(names_c)}")
    print()

    # Part (d)
    print("=== Part (d): Anagram pairs ===")
    lst1_d = ["Spam", "Trams", "Elbows", "Tops", "Astral"]
    lst2_d = ["Bowels", "Sample", "Altars", "Stop", "Course", "Smart"]
    print(f"lst1: {lst1_d}")
    print(f"lst2: {lst2_d}")
    print(f"Result: {part_d(lst1_d, lst2_d)}")
    print()

    # Part (e)
    print("=== Part (e): Dict comprehension: string -> length ===")
    s_e = ['one', 'two', 'three']
    print(f"Input: {s_e}")
    print(f"Result: {part_e(s_e)}")
    print()

    # Part (f)
    print("=== Part (f): Dict comprehension: v  owel positions ===")
    text_f = "Hello world"
    print(f"Input: {text_f!r}")
    print(f"Result: {part_f(text_f)}")


if __name__ == "__main__":
    main()