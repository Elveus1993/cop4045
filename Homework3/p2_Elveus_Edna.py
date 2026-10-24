"""
p2_Elveus_Edna.py

Problem 2: Parking permits (17 pts)

A small class hierarchy for parking permits, with a function that
summarizes a mixed list of permits.

Design decisions (documented per spec instructions):

* Spec issue, part e: the spec says "Use the methods from part d)", but
  part d is __str__/__repr__ while cost() is part c. We read the intent
  as: use cost() to compute the revenue and str() to print each line.
  summarize_list() therefore calls str(permit) for the printing and
  permit.cost() for the revenue.

* Rates live in a fee-schedule dict built in main() and passed into each
  permit's constructor. cost() looks the rates up; it never hardcodes
  them. A missing key raises KeyError, which is a programming error and
  is documented as a precondition.

* ParkingPermit.cost() raises NotImplementedError, so a subclass that
  forgets to override it fails loudly instead of silently billing 0.
  As a consequence, ParkingPermit.__str__ also raises for the base
  class, because it calls cost(). This is intentional: the base class
  is not meant to be instantiated on its own.

* Fee dict is stored by reference, not copied. This is deliberate: the
  schedule is shared and read-only across all permits, exactly as in a
  real system. Aliasing is safe here because nothing mutates it.

* Edge cases: months < 0 raises ValueError; vehicles < 0 raises
  ValueError. Zero months is allowed and costs 0. The "after the first"
  vehicle rule is max(0, vehicles - 1) * one_time, which correctly
  gives 0 for 0 or 1 vehicles.

* Money is formatted with f"${x:.2f}" everywhere, so output and test
  expectations match exactly.
"""

from typing import Dict, List


def testif(
    b: bool,
    testname: str,
    msgOK: str = "",
    msgFailed: str = "",
) -> bool:
    """Test function that prints Success/Failed based on the test result.

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


class ParkingPermit:
    """
    Base class for a parking permit.

    Stores the owner's name, the number of months purchased, and a
    reference to the fee schedule dict.

    Contract:
        Preconditions:  owner is a str; months is an int >= 0; fees is a
            dict containing whatever keys the concrete subclass needs.
        Postconditions: the three attributes are stored; cost() is a
            placeholder that subclasses must override; __str__ is only
            usable on subclasses that override cost().
    """

    def __init__(
        self, owner: str, months: int, fees: Dict[str, float]
    ) -> None:
        """
        Construct a base parking permit.

        Args:
            owner (str): The permit holder's name.
            months (int): Number of months purchased; must be >= 0.
            fees (Dict[str, float]): Shared fee schedule.

        Raises:
            ValueError: If months is negative.

        Preconditions:
            owner is a str; months is an int >= 0; fees is a dict
            shared across permits (stored by reference, not copied).
        Postconditions:
            self._owner, self._months, self._fees are set.
        """
        if months < 0:
            raise ValueError("months must be non-negative")
        self._owner: str = owner
        self._months: int = months
        self._fees: Dict[str, float] = fees

    def cost(self) -> float:
        """
        Return the total cost of the permit.

        Returns:
            float: Never returns; always raises.

        Raises:
            NotImplementedError: Always, because the base class has no
                rate of its own.

        Preconditions:  none.
        Postconditions: raises NotImplementedError.
        """
        raise NotImplementedError("subclasses must implement cost()")

    def __str__(self) -> str:
        """
        Return a human-readable one-line description.

        Returns:
            str: Owner, permit kind, months, and cost.

        Raises:
            NotImplementedError: If called on the base class, because
                cost() is not implemented there.

        Preconditions:  cost() is implemented (i.e. this is a subclass).
        Postconditions: returns a str.
        """
        kind = type(self).__name__
        return (
            f"{self._owner} ({kind}, {self._months} months): "
            f"${self.cost():.2f}"
        )

    def __repr__(self) -> str:
        """
        Return a debugging representation that could rebuild the object.

        Returns:
            str: A constructor-style string including the fee dict.

        Preconditions:  none.
        Postconditions: returns a str.
        """
        return (
            f"{type(self).__name__}({self._owner!r}, {self._months!r}, "
            f"{self._fees!r})"
        )


class StudentPermit(ParkingPermit):
    """
    A student parking permit.

    Cost: a per-month rate plus a one-time charge for every vehicle
    after the first.
    """

    def __init__(
        self,
        owner: str,
        months: int,
        fees: Dict[str, float],
        vehicles: int,
    ) -> None:
        """
        Construct a student permit.

        Args:
            owner (str): The student's name.
            months (int): Months purchased; must be >= 0.
            fees (Dict[str, float]): Must contain "student_monthly" and
                "vehicle_one_time".
            vehicles (int): Number of registered vehicles; must be >= 0.

        Raises:
            ValueError: If months or vehicles is negative.

        Preconditions:
            See Args; fees contains the two required keys.
        Postconditions:
            Base attributes set; self._vehicles set.
        """
        super().__init__(owner, months, fees)
        if vehicles < 0:
            raise ValueError("vehicles must be non-negative")
        self._vehicles: int = vehicles

    def cost(self) -> float:
        """
        Return the student permit cost.

        Returns:
            float: months * student_monthly
                + max(0, vehicles - 1) * vehicle_one_time.

        Raises:
            KeyError: If the fee schedule is missing a required key.

        Preconditions:
            self._fees has "student_monthly" and "vehicle_one_time".
        Postconditions:
            Returns a non-negative float; self is unchanged.
        """
        monthly = self._months * self._fees["student_monthly"]
        extra_vehicles = max(0, self._vehicles - 1)
        vehicle_fee = extra_vehicles * self._fees["vehicle_one_time"]
        return monthly + vehicle_fee

    def __str__(self) -> str:
        """
        Return a human-readable one-line description.

        Returns:
            str: Owner, "Student", months, vehicles, and cost.

        Preconditions:  none.
        Postconditions: returns a str.
        """
        return (
            f"{self._owner} (Student, {self._months} months, "
            f"{self._vehicles} vehicles): ${self.cost():.2f}"
        )

    def __repr__(self) -> str:
        """
        Return a debugging representation.

        Returns:
            str: Constructor-style string including the fee dict.

        Preconditions:  none.
        Postconditions: returns a str.
        """
        return (
            f"StudentPermit({self._owner!r}, {self._months!r}, "
            f"{self._fees!r}, {self._vehicles!r})"
        )


class FacultyPermit(ParkingPermit):
    """
    A faculty parking permit.

    Cost: a per-month rate, plus a per-month garage charge if garage
    access is included.
    """

    def __init__(
        self,
        owner: str,
        months: int,
        fees: Dict[str, float],
        garage: bool,
    ) -> None:
        """
        Construct a faculty permit.

        Args:
            owner (str): The faculty member's name.
            months (int): Months purchased; must be >= 0.
            fees (Dict[str, float]): Must contain "faculty_monthly" and
                "garage_monthly".
            garage (bool): Whether garage access is included.

        Raises:
            ValueError: If months is negative.

        Preconditions:
            See Args; fees contains the two required keys.
        Postconditions:
            Base attributes set; self._garage set.
        """
        super().__init__(owner, months, fees)
        self._garage: bool = garage

    def cost(self) -> float:
        """
        Return the faculty permit cost.

        Returns:
            float: months * faculty_monthly
                + (months * garage_monthly if garage else 0).

        Raises:
            KeyError: If the fee schedule is missing a required key.

        Preconditions:
            self._fees has "faculty_monthly" and "garage_monthly".
        Postconditions:
            Returns a non-negative float; self is unchanged.
        """
        monthly = self._months * self._fees["faculty_monthly"]
        garage_fee = (
            self._months * self._fees["garage_monthly"]
            if self._garage
            else 0
        )
        return monthly + garage_fee

    def __str__(self) -> str:
        """
        Return a human-readable one-line description.

        Returns:
            str: Owner, "Faculty", months, garage yes/no, and cost.

        Preconditions:  none.
        Postconditions: returns a str.
        """
        garage_text = "with garage" if self._garage else "no garage"
        return (
            f"{self._owner} (Faculty, {self._months} months, "
            f"{garage_text}): ${self.cost():.2f}"
        )

    def __repr__(self) -> str:
        """
        Return a debugging representation.

        Returns:
            str: Constructor-style string including the fee dict.

        Preconditions:  none.
        Postconditions: returns a str.
        """
        return (
            f"FacultyPermit({self._owner!r}, {self._months!r}, "
            f"{self._fees!r}, {self._garage!r})"
        )


def summarize_list(permits: List[ParkingPermit]) -> float:
    """
    Print each permit and return total revenue.

    Uses str() for printing and cost() for revenue. Does not use
    isinstance: it relies on every permit responding to both messages
    (polymorphism). For an empty list, prints nothing and returns 0.0.

    Args:
        permits (List[ParkingPermit]): A mixed list of permits.

    Returns:
        float: Total revenue across all permits.

    Preconditions:
        Every element supports str() and cost().
    Postconditions:
        Prints one line per permit; returns the sum of their costs.
    """
    total: float = 0.0
    for permit in permits:
        print(permit)
        total += permit.cost()
    return total


def main() -> None:
    """Demonstrate the permit classes and summarize_list with tests."""

    fees: Dict[str, float] = {
        "student_monthly": 25,
        "vehicle_one_time": 10,
        "faculty_monthly": 40,
        "garage_monthly": 15,
    }

    alice = StudentPermit("Alice", 3, fees, 2)
    bob = StudentPermit("Bob", 3, fees, 1)
    carol = FacultyPermit("Carol", 5, fees, True)
    dave = FacultyPermit("Dave", 5, fees, False)
    permits = [alice, bob, carol, dave]

    # --- individual cost checks (hand-computed) ---
    testif(alice.cost() == 85.0, "student 3mo/2veh",
           "$85.00", "wrong cost")
    testif(bob.cost() == 75.0, "student 3mo/1veh",
           "$75.00", "wrong cost")
    testif(carol.cost() == 275.0, "faculty 5mo/garage",
           "$275.00", "wrong cost")
    testif(dave.cost() == 200.0, "faculty 5mo/no garage",
           "$200.00", "wrong cost")

    # --- string formatting ---
    testif(str(alice) == "Alice (Student, 3 months, 2 vehicles): $85.00",
           "student __str__", "formatted line", "wrong format")
    testif(str(carol) == "Carol (Faculty, 5 months, with garage): $275.00",
           "faculty __str__", "formatted line", "wrong format")

        # --- repr actually rebuilds the object ---
    alice_repr = repr(alice)
    alice_rebuilt = eval(alice_repr, {
        "StudentPermit": StudentPermit,
        "FacultyPermit": FacultyPermit,
        "ParkingPermit": ParkingPermit,
    })
    testif(repr(alice_rebuilt) == alice_repr,
           "student __repr__ rebuilds",
           "eval(repr) reproduces the same repr string",
           "repr not rebuildable")
    testif(alice_rebuilt.cost() == alice.cost(),
           "rebuilt cost matches",
           "$85.00", "wrong cost")

    # --- base class cost() raises ---
    try:
        ParkingPermit("X", 1, fees).cost()
        testif(False, "base cost raises", "", "no exception raised")
    except NotImplementedError:
        testif(True, "base cost raises", "NotImplementedError raised", "")

    # --- base class __str__ raises (documented consequence) ---
    try:
        str(ParkingPermit("X", 1, fees))
        testif(False, "base __str__ raises", "", "no exception raised")
    except NotImplementedError:
        testif(True, "base __str__ raises",
               "NotImplementedError raised", "")

    # --- edge cases ---
    testif(StudentPermit("Z", 0, fees, 0).cost() == 0.0,
           "zero months/vehicles", "$0.00", "wrong cost")
    try:
        StudentPermit("Z", -1, fees, 0)
        testif(False, "negative months raises", "", "no exception raised")
    except ValueError:
        testif(True, "negative months raises", "ValueError raised", "")
    try:
        StudentPermit("Z", 1, fees, -1)
        testif(False, "negative vehicles raises", "", "no exception raised")
    except ValueError:
        testif(True, "negative vehicles raises", "ValueError raised", "")

    # --- part f: print the objects involved ---
    print()
    print("--- str() of each permit ---")
    for p in permits:
        print(str(p))

    print()
    print("--- repr() of each permit ---")
    for p in permits:
        print(repr(p))

    # --- summarize_list ---
    print()
    print("--- summarize_list ---")
    total = summarize_list(permits)
    print(f"Total revenue: ${total:.2f}")
    testif(total == 635.0, "mixed list total",
           "$635.00", "wrong total")
    testif(summarize_list([]) == 0.0, "empty list",
           "$0.00", "wrong total")


if __name__ == "__main__":
    main()