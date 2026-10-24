"""
p1_Elveus_Edna.py

Problem 1: NVector (17 pts)

A class representing a mathematical vector with element-wise and scalar
operations.

Design decisions (documented per spec instructions):

* Constructor dispatch: __init__(self, *args) accepts either
    - a single sequence (anything list() accepts): NVector([1, 2, 3]),
      NVector((3, 0, 1, -1)), NVector(range(3))
    - two or more numbers: NVector(3, 0, 1, -1)  -> length 4
  A single scalar (e.g. NVector(5)) raises TypeError from list(5).
  A single string raises TypeError explicitly. All elements are
  validated as numbers (Real) in both paths.

* Zero arguments: NVector() raises TypeError. The spec is silent; we
  choose to require at least one argument.

* zeros(n) for negative n: raises ValueError. Documented here.

* Item i formula: NVector * NVector returns the dot product (a number).
  NVector * number returns a new NVector (scalar multiplication).

* testif: the Appendix version (Success:/Failed:, "; " separator,
  defaults, returns b), with type annotations added per the spec's
  "full function type annotations" requirement.

* Operators return NotImplemented for unsupported types so Python can
  try the reflected method and then raise TypeError itself.
"""

from numbers import Real
from typing import Union


def testif(
    b: bool,
    testname: str,
    msgOK: str = "",
    msgFailed: str = "",
) -> bool:
    """Test function that prints PASS/FAIL based on the test result.

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


class NVector:
    """
    A one-dimensional mathematical vector.

    Elements are stored in an internal list. Supports construction from
    a sequence or from individual numbers, indexing (including negative
    indices), element-wise and scalar arithmetic, equality comparison,
    and a zeros() class method.

    Contract:
        Preconditions:  see __init__.
        Postconditions: elements are stored in a private list; the
                        caller's original sequence is never aliased.
    """

    def __init__(self, *args: Union[float, int, list, tuple]) -> None:
        """
        Construct an NVector.

        Args:
            *args: Either a single sequence (list, tuple, range, ...)
                whose items become the elements, or two or more numbers
                that become the elements.

        Raises:
            TypeError: If no arguments are given, if a single argument
                is a scalar or string, or if any element is not a number.

        Preconditions:
            * If len(args) == 1: args[0] must be a non-string sequence.
            * If len(args) >= 2: each arg must be a number (Real).
            * If len(args) == 0: raises TypeError.

        Postconditions:
            self._data is a new list of numbers. The caller's original
            sequence is copied, not aliased.
        """
        if len(args) == 0:
            raise TypeError("NVector requires at least one argument")
        if len(args) == 1:
            seq = args[0]
            if isinstance(seq, str):
                raise TypeError("NVector does not accept a string")
            self._data: list = list(seq)  # raises TypeError for scalars
        else:
            self._data = list(args)
        for x in self._data:
            if not isinstance(x, Real):
                raise TypeError("NVector elements must be numbers")

    # ---- basic protocol -------------------------------------------------

    def __len__(self) -> int:
        """
        Return the dimension of the vector.

        Returns:
            int: The number of elements.

        Preconditions:  none.
        Postconditions: returns a non-negative int.
        """
        return len(self._data)

    def __getitem__(self, index: int) -> float:
        """
        Return the element at index (negative indices allowed).

        Args:
            index (int): Position of the element (negative allowed).

        Returns:
            The element at that position.

        Raises:
            TypeError: If index is not an int.
            IndexError: If index is out of range.

        Preconditions:
            index is an int. Slicing is not supported.
        Postconditions:
            Returns self._data[index]; self is unchanged.
        """
        if not isinstance(index, int):
            raise TypeError("NVector indices must be integers")
        return self._data[index]

    def __setitem__(self, index: int, value: float) -> None:
        """
        Set the element at index to value.

        Args:
            index (int): Position to set (negative allowed).
            value: The new numeric value.

        Raises:
            TypeError: If index is not an int or value is not a number.
            IndexError: If index is out of range.

        Preconditions:
            index is an int (negative allowed); value is a number.
        Postconditions:
            self._data[index] == value.
        """
        if not isinstance(index, int):
            raise TypeError("NVector indices must be integers")
        if not isinstance(value, Real):
            raise TypeError("NVector elements must be numbers")
        self._data[index] = value

    def __str__(self) -> str:
        """
        Return a readable string like '<1, 2, 3>'.

        Returns:
            str: The formatted vector.

        Preconditions:  none.
        Postconditions: returns a str.
        """
        return "<" + ", ".join(str(x) for x in self._data) + ">"

    def __repr__(self) -> str:
        """
        Return an unambiguous string representation.

        Returns:
            str: A string like 'NVector([1, 2, 3])' that evaluates back
                to an equal NVector.

        Preconditions:  none.
        Postconditions: returns a str.
        """
        return "NVector(" + repr(self._data) + ")"

    # ---- equality -------------------------------------------------------

    def __eq__(self, other: object) -> bool:
        """
        Return True iff other is an NVector with equal elements.

        Args:
            other: The object to compare against.

        Returns:
            bool: True if other is an NVector with equal elements,
                False otherwise (including non-NVector objects).

        Preconditions:  none.
        Postconditions: returns a bool; does not raise.
        """
        if not isinstance(other, NVector):
            return False
        if len(self) != len(other):
            return False
        for i in range(len(self)):
            if self._data[i] != other._data[i]:
                return False
        return True

    def __ne__(self, other: object) -> bool:
        """
        Return the negation of __eq__.

        Args:
            other: The object to compare against.

        Returns:
            bool: True if the vectors differ or other is not an NVector.

        Preconditions:  none.
        Postconditions: returns a bool.
        """
        return not self.__eq__(other)

    # ---- arithmetic -----------------------------------------------------

    def __add__(
        self,
        other: Union["NVector", float, int],
    ) -> Union["NVector", type(NotImplemented)]:
        """
        Add an NVector element-wise, or a number to all elements.

        Args:
            other: An NVector of the same length, or a number.

        Returns:
            NVector: A new vector; self is unchanged.
            NotImplemented: If other is an unsupported type.

        Raises:
            ValueError: If other is an NVector of a different length.

        Preconditions:
            other is an NVector of the same length, or a number.
        Postconditions:
            Returns a new NVector; self is unchanged.
        """
        if isinstance(other, NVector):
            if len(self) != len(other):
                raise ValueError("cannot add NVectors of different lengths")
            return NVector([self._data[i] + other._data[i]
                            for i in range(len(self))])
        if isinstance(other, Real):
            return NVector([x + other for x in self._data])
        return NotImplemented

    def __radd__(
        self,
        other: Union["NVector", float, int],
    ) -> Union["NVector", type(NotImplemented)]:
        """
        Support number + NVector (e.g. 10 + v, and sum([v1, v2])).

        Args:
            other: A number (or 0, as used by sum()).

        Returns:
            NVector: A new vector; self is unchanged.
            NotImplemented: If other is an unsupported type.

        Preconditions:
            other is a number.
        Postconditions:
            Returns a new NVector; self is unchanged.
        """
        if isinstance(other, Real):
            return NVector([other + x for x in self._data])
        return NotImplemented

    def __mul__(
        self,
        other: Union["NVector", float, int],
    ) -> Union[float, "NVector", type(NotImplemented)]:
        """
        NVector * NVector -> dot product (a number).
        NVector * number  -> scalar multiplication (a new NVector).

        Note on spec item i: the literal formula "Σ A_i * B" for a number
        B would give a single number, but scalar multiplication is
        intended, so we return a vector for the number case.

        Args:
            other: An NVector of the same length, or a number.

        Returns:
            float: The dot product for the NVector case.
            NVector: A new vector for the number case.
            NotImplemented: If other is an unsupported type.

        Raises:
            ValueError: If other is an NVector of a different length.

        Preconditions:
            other is an NVector of the same length, or a number.
        Postconditions:
            Returns a number or a new NVector; self is unchanged.
        """
        if isinstance(other, NVector):
            if len(self) != len(other):
                raise ValueError("cannot dot NVectors of different lengths")
            total: float = 0
            for i in range(len(self)):
                total += self._data[i] * other._data[i]
            return total
        if isinstance(other, Real):
            return NVector([x * other for x in self._data])
        return NotImplemented

    def __rmul__(
        self,
        other: Union["NVector", float, int],
    ) -> Union[float, "NVector", type(NotImplemented)]:
        """
        Support number * NVector.

        Args:
            other: A number.

        Returns:
            NVector: A new vector; self is unchanged.
            NotImplemented: If other is an unsupported type.

        Preconditions:
            other is a number.
        Postconditions:
            Returns a new NVector; self is unchanged.
        """
        return self.__mul__(other)

    # ---- class method ---------------------------------------------------

    @classmethod
    def zeros(cls, n: int) -> "NVector":
        """
        Return a new NVector of dimension n, all elements 0.

        Args:
            n (int): The dimension; must be non-negative.

        Returns:
            NVector: A vector of n zeros (of type cls).

        Raises:
            TypeError: If n is not an int.
            ValueError: If n is negative.

        Preconditions:
            n is an int >= 0.
        Postconditions:
            Returns cls([0] * n).
        """
        if not isinstance(n, int):
            raise TypeError("zeros() requires an int")
        if n < 0:
            raise ValueError("zeros() requires a non-negative dimension")
        return cls([0] * n)


def main() -> None:
    """Run tests for NVector features a-i using testif()."""
    # a. construction from a sequence; copies, does not alias
    src = [1, 2, 3]
    v = NVector(src)
    testif(len(v) == 3, "construct from list", "length is 3", "wrong length")
    src[0] = 999
    testif(v[0] == 1, "constructor copies list",
           "original list not aliased", "original list was aliased")

    # a. tuple form (spec example)
    t = NVector((3, 0, 1, -1))
    testif(len(t) == 4, "construct from tuple", "length is 4", "wrong length")
    testif(t == NVector(3, 0, 1, -1), "tuple == args form",
           "both forms equal", "forms differ")

    # a. scalar alone raises TypeError
    try:
        NVector(5)
        testif(False, "scalar raises TypeError", "", "no exception raised")
    except TypeError:
        testif(True, "scalar raises TypeError", "TypeError raised", "")

    # b. two or more arguments become elements
    w = NVector(3, 0, 1, -1)
    testif(len(w) == 4, "construct from args", "length is 4", "wrong length")

    # c. __len__
    testif(len(NVector([1, 2])) == 2, "__len__", "returns 2", "wrong length")

    # d. spec example: x[-2] == 1 for x = NVector([3, 0, 1, -1])
    x = NVector([3, 0, 1, -1])
    testif(x[-2] == 1, "negative getitem (spec)", "x[-2] == 1", "wrong value")
    testif(x[0] == 3, "positive getitem", "x[0] == 3", "wrong value")

    # d. bad index on read raises IndexError
    try:
        _ = x[100]
        testif(False, "bad read index raises IndexError",
               "", "no exception raised")
    except IndexError:
        testif(True, "bad read index raises IndexError",
               "IndexError raised", "")

    # d. non-int index raises TypeError
    try:
        _ = x["a"]
        testif(False, "non-int index raises TypeError",
               "", "no exception raised")
    except TypeError:
        testif(True, "non-int index raises TypeError", "TypeError raised", "")

    # e. __setitem__ with negative indices
    y = NVector([10, 20, 30, 40, 50])
    y[-2] = 99
    testif(y[-2] == 99, "setitem works", "y[-2] == 99", "setitem failed")
    testif(y[3] == 99, "setitem negative index", "y[3] == 99", "wrong value")

    # e. invalid index raises IndexError
    try:
        y[100] = 1
        testif(False, "bad setitem index raises IndexError",
               "", "no exception raised")
    except IndexError:
        testif(True, "bad setitem index raises IndexError",
               "IndexError raised", "")

    # f. __str__
    testif(str(NVector([1, 2, 3])) == "<1, 2, 3>",
           "__str__", "format is <1, 2, 3>", "wrong format")

    # g. __eq__ and __ne__
    testif(NVector([1, 2]) == NVector([1, 2]),
           "__eq__ equal", "equal vectors compare equal", "not equal")
    testif(NVector([1, 2]) != NVector([1, 3]),
           "__ne__ different", "different vectors compare unequal", "equal")
    testif((NVector([1, 2]) != NVector([1, 2])) is False,
           "__ne__ equal", "equal vectors compare not-unequal", "wrong")
    testif((NVector([1, 2]) == NVector([1, 2, 3])) is False,
           "__eq__ different lengths",
           "different lengths not equal", "reported equal")
    testif((NVector([1, 2]) == [1, 2]) is False,
           "__eq__ non-NVector", "non-NVector returns False", "returned True")

    # h. __add__ and __radd__ (spec examples)
    a1 = NVector([3, 0, 1, -1])
    a2 = NVector([1, 2, 3, 4])
    testif(a1 + a2 == NVector([4, 2, 4, 3]),
           "NVector + NVector (spec)", "element-wise add", "wrong result")
    testif(a1 + 10 == NVector([13, 10, 11, 9]),
           "NVector + number (spec)", "adds number to all", "wrong result")
    testif(10 + a1 == NVector([13, 10, 11, 9]),
           "number + NVector", "radd works", "wrong result")
    testif(sum([a1, a2]) == NVector([4, 2, 4, 3]),
           "sum() uses __radd__", "sum works", "wrong result")

    # h. operators do not mutate operands
    before_a1 = NVector([3, 0, 1, -1])
    _ = a1 + a2
    _ = 10 + a1
    _ = a1 * 2
    testif(a1 == before_a1, "operators do not mutate",
           "a1 unchanged", "a1 was mutated")

    # i. __mul__ and __rmul__ (spec example)
    m1 = NVector([3, 0, 1, -1])
    m2 = NVector([1, 2, 3, 4])
    testif(m1 * m2 == 2, "NVector * NVector (spec)",
           "dot product is 2", "wrong dot product")
    testif(m1 * 2 == NVector([6, 0, 2, -2]),
           "NVector * number", "scalar multiply", "wrong result")
    testif(2 * m1 == NVector([6, 0, 2, -2]),
           "number * NVector", "rmul works", "wrong result")

    # j. zeros
    testif(NVector.zeros(3) == NVector([0, 0, 0]),
           "zeros(3)", "returns <0, 0, 0>", "wrong result")
    testif(NVector.zeros(0) == NVector([]),
           "zeros(0)", "returns empty vector", "wrong result")
    try:
        NVector.zeros(-1)
        testif(False, "zeros(-1) raises", "", "no exception raised")
    except ValueError:
        testif(True, "zeros(-1) raises", "ValueError raised", "")

    # error case: mismatched lengths
    try:
        NVector([1, 2]) + NVector([1, 2, 3])
        testif(False, "mismatched add raises", "", "no exception raised")
    except ValueError:
        testif(True, "mismatched add raises", "ValueError raised", "")

    # error case: unsupported type in multiplication
    try:
        NVector([1, 2]) * "a"
        testif(False, "unsupported mul raises", "", "no exception raised")
    except TypeError:
        testif(True, "unsupported mul raises", "TypeError raised", "")


if __name__ == "__main__":
    main()