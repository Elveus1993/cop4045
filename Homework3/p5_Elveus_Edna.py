"""Recursion exercises (Problem 5).

File name note: the handout header says "p2_Elveus_Edna.py" in every
part, which is a typo. The correct file is "p5_Elveus_Edna.py".

Other notes:

* Figure 1b's text description in the handout contradicts itself
  ("branches at the bottom or at the top?"). The drawing here matches
  the interpretation "petiole at the bottom, two child leaves at the
  top", which is what the PDF figure shows.

* Figure 2's caption says "Problem 1" and shows level 8. Neither
  affects what is submitted.

* run_Cnk is not defined in the spec. It is defined here to print
  Cnk_m values for interesting (n, k) pairs, comparing memoized
  and non-memoized timings so memoization is visibly working.

* Type annotations are not required for Problem 5 but are included
  for consistency with Problems 1-4.
"""

import time
import turtle
from typing import Any, List, Sequence, Tuple


# ============================================================
# Part a: draw_leaf_straight / draw_leaf_curved (turtle)
# ============================================================

_LEAF_ANGLE = 45      # degrees between the two branches at each tip
_LEAF_SHRINK = 0.7    # length multiplier per recursion level
_LEAF_CURVE = 2       # degrees turned per step in the curved stem
_LEAF_STEPS = 10      # number of steps per curved stem


def draw_leaf_straight(level: int, length: float) -> None:
    """Draw a straight-edged recursive leaf.

    Args:
        level: recursion depth; 1 draws a single stem.
        length: length of the petiole (the lower straight stem).

    Preconditions:
        level is a positive int; length is a positive number.
        The turtle is at the drawing origin facing East.

    Postconditions:
        The leaf is drawn, and the turtle is returned to its
        starting position and heading.
    """
    start_x, start_y = turtle.pos()
    start_heading = turtle.heading()
    turtle.left(90)
    _draw_leaf_straight_rec(level, length)
    turtle.up()
    turtle.goto(start_x, start_y)
    turtle.setheading(start_heading)
    turtle.down()


def _draw_leaf_straight_rec(level: int, length: float) -> None:
    """Draw one straight leaf subtree; restore position and heading."""
    start_x, start_y = turtle.pos()
    start_heading = turtle.heading()

    if level == 1:
        turtle.forward(length)
    else:
        turtle.forward(length)
        tip_x, tip_y = turtle.pos()
        tip_heading = turtle.heading()

        turtle.left(_LEAF_ANGLE)
        _draw_leaf_straight_rec(level - 1, length * _LEAF_SHRINK)
        turtle.up()
        turtle.goto(tip_x, tip_y)
        turtle.setheading(tip_heading)
        turtle.down()

        turtle.right(_LEAF_ANGLE)
        _draw_leaf_straight_rec(level - 1, length * _LEAF_SHRINK)
        turtle.up()
        turtle.goto(tip_x, tip_y)
        turtle.setheading(tip_heading)
        turtle.down()

    turtle.up()
    turtle.goto(start_x, start_y)
    turtle.setheading(start_heading)
    turtle.down()


def draw_leaf_curved(level: int, length: float) -> None:
    """Draw a curved recursive leaf (extra credit).

    Args:
        level: recursion depth; 1 draws a single curved stem.
        length: arc length of the petiole.

    Preconditions:
        level is a positive int; length is a positive number.

    Postconditions:
        The curved leaf is drawn; the turtle is restored to its
        starting position and heading.
    """
    start_x, start_y = turtle.pos()
    start_heading = turtle.heading()
    turtle.left(90)
    _draw_leaf_curved_rec(level, length)
    turtle.up()
    turtle.goto(start_x, start_y)
    turtle.setheading(start_heading)
    turtle.down()


def _draw_curved_segment(length: float) -> None:
    """Draw a gently curved segment of total arc length `length`."""
    step_len = length / _LEAF_STEPS
    for _ in range(_LEAF_STEPS):
        turtle.forward(step_len)
        turtle.left(_LEAF_CURVE)


def _draw_leaf_curved_rec(level: int, length: float) -> None:
    """Draw one curved leaf subtree; restore position and heading."""
    start_x, start_y = turtle.pos()
    start_heading = turtle.heading()

    if level == 1:
        _draw_curved_segment(length)
    else:
        _draw_curved_segment(length)
        tip_x, tip_y = turtle.pos()
        tip_heading = turtle.heading()

        turtle.left(_LEAF_ANGLE)
        _draw_leaf_curved_rec(level - 1, length * _LEAF_SHRINK)
        turtle.up()
        turtle.goto(tip_x, tip_y)
        turtle.setheading(tip_heading)
        turtle.down()

        turtle.right(_LEAF_ANGLE)
        _draw_leaf_curved_rec(level - 1, length * _LEAF_SHRINK)
        turtle.up()
        turtle.goto(tip_x, tip_y)
        turtle.setheading(tip_heading)
        turtle.down()

    turtle.up()
    turtle.goto(start_x, start_y)
    turtle.setheading(start_heading)
    turtle.down()


# ============================================================
# Part b: strB
# ============================================================

_DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def strB(n: int, base: int = 10) -> str:
    """Convert a non-negative int to its string form in a given base.

    Args:
        n: non-negative integer to convert.
        base: integer in [2, 26]; digits 10-25 use 'A'-'Z'.

    Returns:
        The representation of n in the given base.

    Raises:
        TypeError: If n or base is not an int.
        ValueError: If n < 0, or base is outside [2, 26].

    Preconditions:
        n >= 0; 2 <= base <= 26.

    Postconditions:
        Returns a non-empty string. strB(0) == '0'.
    """
    if not isinstance(n, int) or not isinstance(base, int):
        raise TypeError("n and base must be ints")
    if n < 0:
        raise ValueError("n must be non-negative")
    if not (2 <= base <= 26):
        raise ValueError("base must be between 2 and 26")
    return _strB_rec(n, base)


def _strB_rec(n: int, base: int) -> str:
    """Recursive worker; assumes n >= 0 and 2 <= base <= 26."""
    if n < base:
        return _DIGITS[n]
    return _strB_rec(n // base, base) + _DIGITS[n % base]


# ============================================================
# Part c: Cnk_m (memoized binomial coefficient)
# ============================================================

def Cnk_m(n: int, k: int) -> int:
    """Memoized recursive binomial coefficient C(n, k).

    Uses C(n, k) = C(n-1, k-1) + C(n-1, k) with C(n, 0) = C(n, n) = 1.

    Args:
        n: top of the binomial; must be >= 0.
        k: bottom of the binomial; must be >= 0.

    Returns:
        C(n, k) as an int (0 when k > n, by convention).

    Raises:
        TypeError: If n or k is not an int.
        ValueError: If n or k is negative.

    Preconditions:
        n >= 0; k >= 0.

    Postconditions:
        Returns a non-negative int. Each (n, k) pair is computed
        at most once thanks to the per-call memo dict.
    """
    if not isinstance(n, int) or not isinstance(k, int):
        raise TypeError("n and k must be ints")
    if n < 0 or k < 0:
        raise ValueError("n and k must be non-negative")

    memo: dict = {}

    def rec(n: int, k: int) -> int:
        if k > n:
            return 0
        if k == 0 or k == n:
            return 1
        key = (n, k)
        if key in memo:
            return memo[key]
        result = rec(n - 1, k - 1) + rec(n - 1, k)
        memo[key] = result
        return result

    return rec(n, k)


def _Cnk_naive(n: int, k: int) -> int:
    """Non-memoized binomial, used only by run_Cnk for comparison."""
    if k > n:
        return 0
    if k == 0 or k == n:
        return 1
    return _Cnk_naive(n - 1, k - 1) + _Cnk_naive(n - 1, k)


def run_Cnk() -> None:
    """Print Cnk_m values for interesting (n, k) pairs.

    Compares memoized timings with non-memoized timings on the same
    inputs, so memoization is visibly working. Defined here because
    the spec references run_Cnk but does not define it.
    """
    pairs = [(5, 2), (10, 5), (15, 7), (20, 10), (22, 11)]
    header = f"{'pair':<10}{'memo (ms)':>14}{'naive (ms)':>14}{'result':>22}"
    print(header)
    print("-" * len(header))
    for n, k in pairs:
        t0 = time.perf_counter()
        r1 = Cnk_m(n, k)
        t1 = time.perf_counter()
        r2 = _Cnk_naive(n, k)
        t2 = time.perf_counter()
        assert r1 == r2, "memo and naive disagree"
        print(f"({n},{k}){'':<4}{(t1 - t0) * 1000:>14.3f}"
              f"{(t2 - t1) * 1000:>14.3f}{r1:>22}")

    # A larger pair that is intractable naively but instant memoized.
    t0 = time.perf_counter()
    big = Cnk_m(60, 30)
    t1 = time.perf_counter()
    print(f"\nC(60, 30) memoized = {big}   "
          f"[{(t1 - t0) * 1000:.3f} ms]")


# ============================================================
# Part d: make_pairs
# ============================================================

def make_pairs(
    seq1: Sequence[Any], seq2: Sequence[Any]
) -> List[Tuple[Any, Any]]:
    """Pair elements of seq1 and seq2 by index, up to the shorter one.

    Args:
        seq1: any sequence.
        seq2: any sequence.

    Returns:
        List of (seq1[i], seq2[i]) tuples, in order.

    Preconditions:
        seq1 and seq2 are sequences.

    Postconditions:
        len(result) == min(len(seq1), len(seq2)); the inputs are
        unchanged.
    """
    return _make_pairs(seq1, seq2, [])


def _make_pairs(
    seq1: Sequence[Any],
    seq2: Sequence[Any],
    acc: List[Tuple[Any, Any]],
) -> List[Tuple[Any, Any]]:
    """Recursive worker carrying the accumulator."""
    if not seq1 or not seq2:
        return acc
    acc.append((seq1[0], seq2[0]))
    return _make_pairs(seq1[1:], seq2[1:], acc)


# ============================================================
# testif (Appendix style)
# ============================================================

def testif(
    b: bool,
    testname: str,
    msgOK: str = "",
    msgFailed: str = "",
) -> bool:
    """Print Success/Failed based on the test result; return b."""
    if b:
        print("Success: " + testname + "; " + msgOK)
    else:
        print("Failed: " + testname + "; " + msgFailed)
    return b


# ============================================================
# Unit tests
# ============================================================

def test_strB() -> None:
    """Four unit tests for strB."""
    testif(strB(0) == "0", "strB(0)", "'0'", "wrong result")
    testif(strB(255, 16) == "FF",
           "strB(255, 16)", "'FF'", "wrong result")
    testif(strB(27, 3) == "1000",
           "strB(27, 3)", "'1000'", "wrong result")
    testif(strB(1000000, 2) == "11110100001001000000",
           "strB(1000000, 2)", "20-bit string", "wrong result")

    # invalid input
    try:
        strB(-1)
        testif(False, "strB(-1) raises", "", "no exception")
    except ValueError:
        testif(True, "strB(-1) raises", "ValueError", "")
    try:
        strB(5, 1)
        testif(False, "strB(5, 1) raises", "", "no exception")
    except ValueError:
        testif(True, "strB(5, 1) raises", "ValueError", "")
    try:
        strB(5, 27)
        testif(False, "strB(5, 27) raises", "", "no exception")
    except ValueError:
        testif(True, "strB(5, 27) raises", "ValueError", "")


def test_Cnk_m() -> None:
    """Four unit tests for Cnk_m."""
    testif(Cnk_m(5, 2) == 10, "C(5, 2)", "10", "wrong result")
    testif(Cnk_m(10, 5) == 252, "C(10, 5)", "252", "wrong result")
    testif(Cnk_m(20, 10) == 184756,
           "C(20, 10)", "184756", "wrong result")
    testif(Cnk_m(7, 0) == 1 and Cnk_m(7, 7) == 1,
           "C(n, 0) == C(n, n) == 1", "1", "wrong result")

    # invalid input
    try:
        Cnk_m(-1, 0)
        testif(False, "Cnk_m(-1, 0) raises", "", "no exception")
    except ValueError:
        testif(True, "Cnk_m(-1, 0) raises", "ValueError", "")


def test_make_pairs() -> None:
    """Five unit tests for make_pairs."""
    testif(make_pairs([1, 2, 3], ["a", "b", "c"])
           == [(1, "a"), (2, "b"), (3, "c")],
           "equal lengths", "matched pairs", "wrong result")
    testif(make_pairs([1, 2], ["a", "b", "c", "d"])
           == [(1, "a"), (2, "b")],
           "first shorter", "stops at first", "wrong result")
    testif(make_pairs([1, 2, 3, 4], ["a", "b"])
           == [(1, "a"), (2, "b")],
           "second shorter", "stops at second", "wrong result")
    testif(make_pairs([], ["a", "b"]) == [],
           "first empty", "[]", "wrong result")
    testif(make_pairs([], []) == [],
           "both empty", "[]", "wrong result")


# ============================================================
# main
# ============================================================

def main() -> None:
    """Run all Problem 5 tests, run_Cnk, and the leaf drawing."""
    print("=== strB tests ===")
    test_strB()

    print("\n=== Cnk_m tests ===")
    test_Cnk_m()

    print("\n=== run_Cnk ===")
    run_Cnk()

    print("\n=== make_pairs tests ===")
    test_make_pairs()

    print("\n=== Leaf drawing ===")
    print("Opening turtle window (draw_leaf_straight(6, 120)).")
    print("Close the window to exit.")

    # Give the leaf room to breathe: an 800x800 canvas gives us
    # coordinates roughly -400..+400 in each axis, so starting at
    # (0, -250) leaves ~470 pixels of margin above the tallest tip.
    turtle.setup(800, 800)
    turtle.title("Edna Elveus - FAU ID: <YOUR_FAU_ID>")
    turtle.hideturtle()
    turtle.speed(0)
    turtle.delay(0)

    # Position and orient the turtle BEFORE calling the drawing
    # function. draw_leaf_straight saves the current position and
    # heading, turns left 90 degrees to stand the leaf up, draws, and
    # restores the state, so we need the turtle facing East here.
    turtle.up()
    turtle.goto(0, -250)
    turtle.setheading(0)  # face East
    turtle.down()

    draw_leaf_straight(6, 120)
    turtle.done()


if __name__ == "__main__":
    main()