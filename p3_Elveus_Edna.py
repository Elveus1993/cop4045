"""
Duplicate Substring Finder
Problem 3 - CS Assignment
"""


def find_dup_str(s, n):
    """
    Find the first-occurring substring of length n that appears at least twice
    non-overlapping in string s.
    
    Uses a brute-force nested loop approach with string slicing and plain
    equality comparisons (no str.find()).
    
    Args:
        s (str): The string to search in
        n (int): Length of substring to find
        
    Returns:
        str: The first duplicated substring of length n, or "" if none exists
    """
    if n <= 0 or len(s) < 2 * n:
        return ""
    
    # Slide window across the string
    for i in range(len(s) - n + 1):
        candidate = s[i:i+n]
        
        # Check for non-overlapping duplicate starting at position j
        # j must be at least i + n to ensure non-overlapping
        for j in range(i + n, len(s) - n + 1):
            if s[j:j+n] == candidate:
                return candidate
    
    return ""


def find_max_dup(s):
    """
    Find the longest duplicated substring in string s.
    
    Starts from the maximum possible length (len(s)//2) and works downward,
    using find_dup_str internally to check each length.
    
    Args:
        s (str): The string to search in
        
    Returns:
        str: The longest duplicated substring, or "" if none exists
    """
    # Maximum possible length for a non-overlapping duplicate
    max_len = len(s) // 2
    
    # Try from largest to smallest length
    for n in range(max_len, 0, -1):
        result = find_dup_str(s, n)
        if result != "":
            return result
    
    return ""


def test_find_dup_str():
    """
    Test function for find_dup_str - reads s and n from terminal.
    """
    print("\n--- Testing find_dup_str ---")
    s = input("Enter string s: ")
    n = int(input("Enter length n: "))
    
    result = find_dup_str(s, n)
    print(f"Result: '{result}'")


def test_find_max_dup():
    """
    Test function for find_max_dup - reads s from terminal.
    """
    print("\n--- Testing find_max_dup ---")
    s = input("Enter string s: ")
    
    result = find_max_dup(s)
    print(f"Longest duplicated substring: '{result}'")


def main():
    """
    Main program: runs both test functions.
    """
    test_find_dup_str()
    test_find_max_dup()


# Run the program
if __name__ == "__main__":
    main()