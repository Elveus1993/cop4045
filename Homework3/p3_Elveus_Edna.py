# Copyright 2017, 2013, 2011 Pearson Education, Inc., W.F. Punch & R.J.Enbody
"""Predator-Prey simulation with Humans.

Adapted from program13-14.py. Adds a Human class that hunts
predators, on top of the existing Animal / Prey / Predator / Island
hierarchy.

Design decisions:

* Human subclasses Animal, not Predator. Island.count_predators() uses
  isinstance(animal, Predator); if Human were a Predator subclass it
  would be miscounted as a predator. Also check_grid() uses exact type
  comparison, so check_grid(Predator) correctly ignores Humans.

* Human constructor signature is (island, x=0, y=0, s="H"), matching
  the call Animal.breed() makes on self.__class__.

* Per-turn order: hunt (Humans only) -> move -> breed -> clock_tick.
  hunt() sets moved=True on success so move() skips.

* Hunt clock rule: the hunt clock resets to Human.hunt_time after every
  hunt ATTEMPT (success or failure). This matches the spec's "Every
  Human.hunt_time ticks ... if a Predator is in a neighboring cell":
  the human tries on a fixed cadence whether or not a predator happens
  to be adjacent, rather than falling into a try-every-tick loop after
  a single miss.

* Starvation: starve_clock starts at Human.starve_time and is reset to
  that value whenever hunt() succeeds (i.e. when the Human actually
  eats). clock_tick decrements all clocks and removes the Human when
  starve_clock <= 0.

* Convergence rule: all three population counts unchanged for
  CONVERGE_TICKS consecutive ticks (defined below). Extinction of one
  or two species does not break the loop; the run continues until
  convergence or MAX_TICKS.

* random.seed(42) is set at module import (see bottom of file, in the
  __main__ block) so screenshots are reproducible without resetting
  the RNG on every call to main().
"""
import random
from typing import List, Optional, Tuple, Union

import matplotlib.pyplot as plt


CONVERGE_TICKS = 20
MAX_TICKS = 1000


class Island(object):
    """Island: n x n grid where zero value indicates not occupied.

    Note on the name count_humans: it is both a parameter to __init__
    and init_animals and the name of a method on this class. Inside
    __init__ the name refers to the parameter; outside it resolves to
    the method. They do not conflict at runtime.
    """

    def __init__(self, n: int, prey_count: int = 0,
                 predator_count: int = 0,
                 count_humans: int = 0) -> None:
        """Initialize grid to all 0's, then fill with animals.

        Args:
            n: side length of the square grid.
            prey_count: number of Prey to place initially.
            predator_count: number of Predators to place initially.
            count_humans: number of Humans to place initially.
        """
        self.grid_size: int = n
        self.grid: List[List[Union[int, "Animal"]]] = []
        for i in range(n):
            row: List[Union[int, "Animal"]] = [0] * n
            self.grid.append(row)
        self.init_animals(prey_count, predator_count, count_humans)

    def init_animals(self, prey_count: int, predator_count: int,
                     count_humans: int = 0) -> None:
        """Place initial Prey, Predators, and Humans at random positions.

        Args:
            prey_count: number of Prey to place.
            predator_count: number of Predators to place.
            count_humans: number of Humans to place.
        """
        count = 0
        while count < prey_count:
            x = random.randint(0, self.grid_size - 1)
            y = random.randint(0, self.grid_size - 1)
            if not self.animal(x, y):
                new_prey = Prey(island=self, x=x, y=y)
                count += 1
                self.register(new_prey)
        count = 0
        while count < predator_count:
            x = random.randint(0, self.grid_size - 1)
            y = random.randint(0, self.grid_size - 1)
            if not self.animal(x, y):
                new_predator = Predator(island=self, x=x, y=y)
                count += 1
                self.register(new_predator)
        count = 0
        while count < count_humans:
            x = random.randint(0, self.grid_size - 1)
            y = random.randint(0, self.grid_size - 1)
            if not self.animal(x, y):
                new_human = Human(island=self, x=x, y=y)
                count += 1
                self.register(new_human)

    def clear_all_moved_flags(self) -> None:
        """Clear the moved flag on every animal in the grid."""
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if self.grid[x][y]:
                    self.grid[x][y].clear_moved_flag()  # type: ignore

    def size(self) -> int:
        """Return size of the island: one dimension."""
        return self.grid_size

    def register(self, animal: "Animal") -> None:
        """Register animal with island at its current coordinates."""
        x = animal.x
        y = animal.y
        self.grid[x][y] = animal

    def remove(self, animal: "Animal") -> None:
        """Remove animal from island, leaving a 0 in its cell."""
        x = animal.x
        y = animal.y
        self.grid[x][y] = 0

    def animal(self, x: int, y: int) -> Union[int, "Animal"]:
        """Return animal at (x, y), or -1 if off the island."""
        if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
            return self.grid[x][y]
        else:
            return -1

    def __str__(self) -> str:
        """String representation; (0, 0) is in the lower left corner."""
        s = ""
        for j in range(self.grid_size - 1, -1, -1):
            for i in range(self.grid_size):
                if not self.grid[i][j]:
                    s += "{:<2s}".format('.' + "  ")
                else:
                    s += "{:<2s}".format((str(self.grid[i][j])) + "  ")
            s += "\n"
        return s

    def count_prey(self) -> int:
        """Count all Prey on the island."""
        count = 0
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                animal = self.animal(x, y)
                if animal and isinstance(animal, Prey):
                    count += 1
        return count

    def count_predators(self) -> int:
        """Count all Predators on the island."""
        count = 0
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                animal = self.animal(x, y)
                if animal and isinstance(animal, Predator):
                    count += 1
        return count

    def count_humans(self) -> int:
        """Count all Humans on the island."""
        count = 0
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                animal = self.animal(x, y)
                if animal and isinstance(animal, Human):
                    count += 1
        return count


class Animal(object):
    """Base class for all animals on the island.

    Subclasses (Prey, Predator, Human) set their own clock attributes
    as class attributes before any instance is created.
    """

    def __init__(self, island: Island, x: int = 0, y: int = 0,
                 s: str = "A") -> None:
        """Initialize an animal and its position.

        Args:
            island: the Island it lives on.
            x: initial x coordinate.
            y: initial y coordinate.
            s: single-character display string.
        """
        self.island: Island = island
        self.name: str = s
        self.x: int = x
        self.y: int = y
        self.moved: bool = False

    def position(self) -> Tuple[int, int]:
        """Return coordinates of current position."""
        return self.x, self.y

    def __str__(self) -> str:
        """Return the display character."""
        return self.name

    def check_grid(self, type_looking_for: type = int) -> Union[int, Tuple[int, int]]:
        """Look in the 8 directions from the animal's location and
        return the first location that has an object of the specified
        type (exact type, not isinstance). Return 0 if none.

        Args:
            type_looking_for: exact class to look for.

        Returns:
            (x, y) tuple of the first matching neighbor, or 0.
        """
        offset = [(-1, 1), (0, 1), (1, 1), (-1, 0),
                  (1, 0), (-1, -1), (0, -1), (1, -1)]
        result: Union[int, Tuple[int, int]] = 0
        for i in range(len(offset)):
            x = self.x + offset[i][0]
            y = self.y + offset[i][1]
            if not 0 <= x < self.island.size() or \
               not 0 <= y < self.island.size():
                continue
            if type(self.island.animal(x, y)) == type_looking_for:
                result = (x, y)
                break
        return result

    def move(self) -> None:
        """Move to an open, neighboring position, if any."""
        if not self.moved:
            location = self.check_grid(int)
            if location:
                self.island.remove(self)
                self.x = location[0]
                self.y = location[1]
                self.island.register(self)
                self.moved = True

    def breed(self) -> None:
        """Breed a new Animal of the same class if a neighbor cell is
        empty and the breed clock has reached 0.
        """
        if self.breed_clock <= 0:  # type: ignore[attr-defined]
            location = self.check_grid(int)
            if location:
                self.breed_clock = self.breed_time  # type: ignore[attr-defined]
                the_class = self.__class__
                new_animal = the_class(self.island,
                                       x=location[0], y=location[1])
                self.island.register(new_animal)

    def clear_moved_flag(self) -> None:
        """Reset the moved flag for the next turn."""
        self.moved = False


class Prey(Animal):
    """A Prey animal (displayed as 'O')."""

    def __init__(self, island: Island, x: int = 0, y: int = 0,
                 s: str = "O") -> None:
        """Initialize a Prey with its breed clock."""
        Animal.__init__(self, island, x, y, s)
        self.breed_clock: int = self.breed_time  # type: ignore[attr-defined]

    def clock_tick(self) -> None:
        """Tick the Prey's breed clock."""
        self.breed_clock -= 1


class Predator(Animal):
    """A Predator animal (displayed as 'X') that eats Prey."""

    def __init__(self, island: Island, x: int = 0, y: int = 0,
                 s: str = "X") -> None:
        """Initialize a Predator with its breed and starve clocks."""
        Animal.__init__(self, island, x, y, s)
        self.starve_clock: int = self.starve_time  # type: ignore[attr-defined]
        self.breed_clock: int = self.breed_time    # type: ignore[attr-defined]

    def clock_tick(self) -> None:
        """Tick both clocks; die if starved."""
        self.breed_clock -= 1
        self.starve_clock -= 1
        if self.starve_clock <= 0:
            self.island.remove(self)

    def eat(self) -> None:
        """Eat an adjacent Prey if one exists, move into its cell,
        and reset the starve clock.
        """
        if not self.moved:
            location = self.check_grid(Prey)
            if location:
                self.island.remove(
                    self.island.animal(location[0], location[1]))
                self.island.remove(self)
                self.x = location[0]
                self.y = location[1]
                self.island.register(self)
                self.starve_clock = self.starve_time  # type: ignore[attr-defined]
                self.moved = True


class Human(Animal):
    """A Human is an Animal that hunts Predators (displayed as 'H').

    Humans do not kill Prey. check_grid(Predator) uses exact type
    comparison, so Prey and other Humans are ignored.

    Class attributes (set from main()):
        breed_time:  ticks between breeding attempts.
        starve_time: ticks a Human can go without eating a Predator
                     before dying.
        hunt_time:   ticks between hunting attempts (the hunt clock
                     resets after every attempt, success or failure).
    """

    def __init__(self, island: Island, x: int = 0, y: int = 0,
                 s: str = "H") -> None:
        """Initialize a Human and its three clocks."""
        Animal.__init__(self, island, x, y, s)
        self.breed_clock: int = self.breed_time  # type: ignore[attr-defined]
        self.starve_clock: int = self.starve_time  # type: ignore[attr-defined]
        self.hunt_clock: int = self.hunt_time     # type: ignore[attr-defined]

    def clock_tick(self) -> None:
        """Tick all three clocks; remove the Human if starved."""
        self.breed_clock -= 1
        self.starve_clock -= 1
        self.hunt_clock -= 1
        if self.starve_clock <= 0:
            self.island.remove(self)

    def hunt(self) -> None:
        """Attempt to hunt.

        On every tick when hunt_clock <= 0, look for an adjacent
        Predator. If found, move into its cell, remove the Predator,
        reset starve_clock and hunt_clock, and set moved=True.

        Whether or not a Predator is found, the hunt clock resets to
        Human.hunt_time so the Human tries on a fixed cadence, per
        the spec's "Every Human.hunt_time ticks" wording.
        """
        if self.moved:
            return
        if self.hunt_clock > 0:
            return
        # Attempt is happening now; reset the clock either way.
        self.hunt_clock = self.hunt_time  # type: ignore[attr-defined]
        location = self.check_grid(Predator)
        if location:
            self.island.remove(
                self.island.animal(location[0], location[1]))
            self.island.remove(self)
            self.x = location[0]
            self.y = location[1]
            self.island.register(self)
            self.starve_clock = self.starve_time  # type: ignore[attr-defined]
            self.moved = True


def main(predator_breed_time: int = 6,
         predator_starve_time: int = 3,
         initial_predators: int = 10,
         prey_breed_time: int = 3,
         initial_prey: int = 50,
         size: int = 10,
         human_breed_time: int = 5,
         human_starve_time: int = 8,
         human_hunt_time: int = 2,
         initial_humans: int = 12) -> None:
    """Run the simulation, plot the three populations, print the grids.

    Stops when all three counts are unchanged for CONVERGE_TICKS
    consecutive ticks, or after MAX_TICKS. Extinction of one or two
    species does not end the run.

    Defaults chosen so all three populations survive to the end and
    interact visibly. The seed is set in __main__ (not here), so
    repeated calls to main() do not reset the RNG.

    Args:
        predator_breed_time: Predator breed period.
        predator_starve_time: Predator starve period.
        initial_predators: starting Predator count.
        prey_breed_time: Prey breed period.
        initial_prey: starting Prey count.
        size: grid side length.
        human_breed_time: Human breed period.
        human_starve_time: Human starve period.
        human_hunt_time: Human hunt period.
        initial_humans: starting Human count.
    """
    Predator.breed_time = predator_breed_time
    Predator.starve_time = predator_starve_time
    Prey.breed_time = prey_breed_time
    Human.breed_time = human_breed_time
    Human.starve_time = human_starve_time
    Human.hunt_time = human_hunt_time

    predator_list: List[int] = []
    prey_list: List[int] = []
    human_list: List[int] = []

    isle = Island(size, initial_prey, initial_predators,
                  count_humans=initial_humans)
    print("Initial island:")
    print(isle)
    print("Initial counts: prey={}, predators={}, humans={}".format(
        isle.count_prey(), isle.count_predators(), isle.count_humans()))

    prev: Optional[Tuple[int, int, int]] = None
    stable_ticks = 0

    for i in range(MAX_TICKS):
        isle.clear_all_moved_flags()
        for x in range(size):
            for y in range(size):
                animal = isle.animal(x, y)
                if animal:
                    if isinstance(animal, Predator):
                        animal.eat()
                    elif isinstance(animal, Human):
                        animal.hunt()
                    animal.move()
                    animal.breed()
                    animal.clock_tick()

        prey_count = isle.count_prey()
        predator_count = isle.count_predators()
        human_count = isle.count_humans()
        prey_list.append(prey_count)
        predator_list.append(predator_count)
        human_list.append(human_count)

        if not i % 10:
            print("tick {}: prey={}, predators={}, humans={}".format(
                i, prey_count, predator_count, human_count))

        current = (prey_count, predator_count, human_count)
        if current == prev:
            stable_ticks += 1
            if stable_ticks >= CONVERGE_TICKS:
                print("Converged at tick {}: {}".format(i, current))
                break
        else:
            stable_ticks = 0
        prev = current
    else:
        print("Reached MAX_TICKS = {}".format(MAX_TICKS))

    print("Final island:")
    print(isle)
    print("Final counts: prey={}, predators={}, humans={}".format(
        isle.count_prey(), isle.count_predators(), isle.count_humans()))

    plt.figure(figsize=(10, 6))
    plt.plot(prey_list, label="Prey")
    plt.plot(predator_list, label="Predators")
    plt.plot(human_list, label="Humans")
    plt.xlabel("Tick")
    plt.ylabel("Population")
    plt.title("Predator-Prey Simulation with Humans -- "
              "Edna Elveus")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Seed here so main() does not reset it on every call.
    random.seed(42)
    main(
        predator_breed_time=6,
        predator_starve_time=3,
        initial_predators=10,
        prey_breed_time=3,
        initial_prey=50,
        size=10,
        human_breed_time=5,
        human_starve_time=8,
        human_hunt_time=2,
        initial_humans=12,
    )