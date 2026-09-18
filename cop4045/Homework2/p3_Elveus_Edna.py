"""
Problem 3 - Social Network
Homework 2 - CS Assignment

Data structure:
    sn = {
        'alice': ('Alice Smith', ['maria']),
        ...
    }
Each key is a username; each value is a tuple:
(full_name, [list_of_friend_usernames]).
"""

import csv

from testif import testif


def add_user(sn: dict, username: str, fullname: str) -> bool:
    """
    Add a new user with no friends yet.

    Args:
        sn: The social network dictionary.
        username: Unique username for the new user.
        fullname: Full display name for the new user.

    Returns:
        bool: True if the user was added, False if username already exists.

    Raises:
        Exception: Re-raises any exception after printing a friendly message.
    """
    try:
        if username in sn:
            return False
        sn[username] = (fullname, [])
        return True
    except Exception as e:
        print(f"Error adding user '{username}': {e}")
        raise


def add_friend(sn: dict, user1: str, user2: str) -> bool:
    """
    Add a mutual friend link between user1 and user2.

    Design decision: if the two are already friends (link already exists),
    this returns True without duplicating the link, treating the operation
    as idempotent.

    Args:
        sn: The social network dictionary.
        user1: First username.
        user2: Second username.

    Returns:
        bool: True on success, False if either username does not exist.

    Raises:
        Exception: Re-raises any exception after printing a friendly message.
    """
    try:
        if user1 not in sn or user2 not in sn:
            return False

        friends1 = sn[user1][1]
        friends2 = sn[user2][1]

        if user2 not in friends1:
            friends1.append(user2)
        if user1 not in friends2:
            friends2.append(user1)

        return True
    except Exception as e:
        print(f"Error adding friend link '{user1}' <-> '{user2}': {e}")
        raise


def get_friends(sn: dict, user1: str, distance: int) -> list:
    """
    Return all friends reachable within `distance` hops from user1.

    Uses breadth-first traversal in layers, tracking a visited set so
    cycles don't cause infinite loops or duplicate results.

    Args:
        sn: The social network dictionary.
        user1: Starting username.
        distance: Maximum number of hops (>= 0).

    Returns:
        list: Usernames of all friends reachable within `distance` hops.
            Empty list if user1 is not in sn or distance <= 0.

    Raises:
        Exception: Re-raises any exception after printing a friendly message.
    """
    try:
        if user1 not in sn or distance <= 0:
            return []

        visited = {user1}
        result = []
        current_layer = [user1]

        for _ in range(distance):
            next_layer = []
            for user in current_layer:
                for friend in sn[user][1]:
                    if friend not in visited:
                        visited.add(friend)
                        result.append(friend)
                        next_layer.append(friend)
            current_layer = next_layer
            if not current_layer:
                break

        return result
    except Exception as e:
        print(f"Error getting friends for '{user1}': {e}")
        raise


def save_network(filename: str, sn: dict) -> None:
    """
    Save the social network dictionary to a CSV file.

    Format: one row per user, columns:
        username, full_name, friend1;friend2;friend3

    Friends are joined with ';' inside a single CSV field, and the csv
    module handles any needed quoting so the comma delimiter stays
    unambiguous.

    Args:
        filename: Path to the CSV file to write.
        sn: The social network dictionary.

    Returns:
        None

    Raises:
        Exception: Re-raises any exception after printing a friendly message.
    """
    try:
        with open(filename, 'w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(['username', 'full_name', 'friends'])
            for username, (fullname, friends) in sn.items():
                writer.writerow([username, fullname, ';'.join(friends)])
        print(f"Successfully saved network to '{filename}'.")
    except Exception as e:
        print(f"Error saving network to '{filename}': {e}")
        raise


def load_network(filename: str) -> dict:
    """
    Load a social network dictionary from a CSV file saved by save_network.

    Args:
        filename: Path to the CSV file to read.

    Returns:
        dict: Reconstructed social network dictionary with the same
            structure produced by save_network.

    Raises:
        Exception: Re-raises any exception after printing a friendly message.
    """
    try:
        sn = {}
        with open(filename, 'r', newline='') as infile:
            reader = csv.reader(infile)
            header = next(reader, None)  # skip header row

            for row in reader:
                if not row:
                    continue
                username = row[0]
                fullname = row[1]
                friends_field = row[2] if len(row) > 2 else ''
                friends = (
                    friends_field.split(';') if friends_field else []
                )
                sn[username] = (fullname, friends)

        return sn
    except Exception as e:
        print(f"Error loading network from '{filename}': {e}")
        raise


def test() -> None:
    """
    Run testif-based tests for parts (a) through (e).

    Uses the testif function from Module 2 to check each function.

    Returns:
        None
    """
    print("=== Running testif tests ===")

    # Helper to build a fresh network for each test
    def fresh():
        return {
            'alice': ('Alice Smith', ['maria']),
            'maria': ('Maria Cortez', ['alice', 'joe', 'david']),
            'joe': ('Joseph Adams', ['maria', 'eve']),
            'eve': ('Evelyn Cooper', ['joe']),
            'david': ('David Benson', ['maria']),
        }

    # ---- Part (a) ----
    sn = fresh()
    testif(
        add_user(sn, 'frank', 'Frank Miller') is True,
        "add_user_new",
        "new user added",
        "expected True"
    )
    testif(
        sn['frank'] == ('Frank Miller', []),
        "add_user_empty_friends",
        "friends list is empty",
        f"got {sn.get('frank')}"
    )
    testif(
        add_user(sn, 'alice', 'Duplicate') is False,
        "add_user_duplicate",
        "duplicate rejected",
        "expected False"
    )

    # ---- Part (b) ----
    sn = fresh()
    testif(
        add_friend(sn, 'alice', 'joe') is True,
        "add_friend_valid",
        "mutual link added",
        "expected True"
    )
    testif(
        'joe' in sn['alice'][1] and 'alice' in sn['joe'][1],
        "add_friend_mutual",
        "both sides updated",
        "not mutual"
    )
    testif(
        add_friend(sn, 'alice', 'ghost') is False,
        "add_friend_missing",
        "missing user rejected",
        "expected False"
    )

    # ---- Part (c) ----
    sn = fresh()
    testif(
        sorted(get_friends(sn, 'alice', 1)) == ['maria'],
        "get_friends_d1",
        "distance 1 correct",
        f"got {get_friends(sn, 'alice', 1)}"
    )
    d2 = sorted(get_friends(sn, 'alice', 2))
    testif(
        d2 == ['david', 'joe', 'maria'],
        "get_friends_d2",
        "distance 2 correct",
        f"got {d2}"
    )
    d3 = sorted(get_friends(sn, 'alice', 3))
    testif(
        d3 == ['david', 'eve', 'joe', 'maria'],
        "get_friends_d3",
        "distance 3 correct",
        f"got {d3}"
    )
    testif(
        get_friends(sn, 'ghost', 1) == [],
        "get_friends_missing",
        "missing user -> empty",
        "expected []"
    )

    # ---- Part (d) + (e) ----
    sn = fresh()
    save_network('test_sn.csv', sn)
    loaded = load_network('test_sn.csv')
    testif(
        loaded == sn,
        "save_load_roundtrip",
        "round-trip preserves data",
        f"got {loaded}"
    )


def main() -> None:
    """
    Main program: tests all social network functions.

    Returns:
        None
    """
    # Build the initial network from the assignment
    sn = {
        'alice': ('Alice Smith', ['maria']),
        'maria': ('Maria Cortez', ['alice', 'joe', 'david']),
        'joe': ('Joseph Adams', ['maria', 'eve']),
        'eve': ('Evelyn Cooper', ['joe']),
        'david': ('David Benson', ['maria']),
    }

    print("=== Part (a): add_user ===")
    print(f"add 'frank': {add_user(sn, 'frank', 'Frank Miller')}")
    print(f"add 'alice' again: {add_user(sn, 'alice', 'Alice S.')}")
    print(f"frank's entry: {sn['frank']}")
    print()

    print("=== Part (b): add_friend ===")
    print(f"add alice <-> joe: {add_friend(sn, 'alice', 'joe')}")
    print(f"alice's friends: {sn['alice'][1]}")
    print(f"joe's friends: {sn['joe'][1]}")
    print(f"add alice <-> ghost: {add_friend(sn, 'alice', 'ghost')}")
    print()

    print("=== Part (c): get_friends ===")
    for d in (1, 2, 3, 4):
        print(f"distance={d} from alice: {sorted(get_friends(sn, 'alice', d))}")
    print(f"ghost: {get_friends(sn, 'ghost', 2)}")
    print()

    print("=== Part (d): save_network ===")
    save_network('p3_network.csv', sn)
    print()

    print("=== Part (e): load_network ===")
    loaded = load_network('p3_network.csv')
    print(f"Loaded {len(loaded)} users.")
    print(f"Matches original: {loaded == sn}")
    print()

    print("=== Part (g): testif tests ===")
    test()

if __name__ == "__main__":
    main()