"""
Pythagorean Triple Finder
Problem 2 - CS Assignment
"""


def find_Pythagorean(n):
    """
    Find all Pythagorean triples (a, b, c) where 0 < a, b, c <= n.
    
    Uses a brute-force approach with three nested loops checking all
    possible combinations. This intentionally produces both (3,4,5) and
    (4,3,5) as separate triples since they represent different assignments
    to a and b, which is consistent with a pure brute-force interpretation.
    
    Args:
        n (int): Upper bound for values of a, b, and c
        
    Returns:
        list: List of tuples (a, b, c) where a^2 + b^2 = c^2
    """
    triples = []
    
    # Brute-force: check all possible values for a, b, and c
    for a in range(1, n + 1):
        for b in range(1, n + 1):
            for c in range(1, n + 1):
                if a**2 + b**2 == c**2:
                    triples.append((a, b, c))
    
    return triples


def main():
    """
    Main program: reads n, finds Pythagorean triples, and displays them.
    """
    # Read positive integer n from terminal
    n = int(input("Enter a positive integer n: "))
    
    # Ensure n is positive
    if n <= 0:
        print("Please enter a positive integer.")
        return
    
    # Find all Pythagorean triples
    triples = find_Pythagorean(n)
    
    # Display the resulting triples to the terminal
    if triples:
        print(f"\nFound {len(triples)} Pythagorean triple(s) for n = {n}:")
        for triple in triples:
            # Print in a clean format: (a, b, c)
            print(f"({triple[0]}, {triple[1]}, {triple[2]})")
    else:
        print(f"\nNo Pythagorean triples found for n = {n}.")


# Run the program
if __name__ == "__main__":
    main()