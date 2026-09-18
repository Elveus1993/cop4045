"""
Caesar Cipher with Frequency Analysis
Problem 5 - CS Assignment
"""


def caesar_cipher(text, shift):
    """
    Encrypt text using Caesar cipher with the given shift.
    
    Shifts each letter by shift positions, preserving spaces, punctuation,
    and original casing. Uses string indexing and loops for mechanics.
    
    Args:
        text (str): The plaintext to encrypt
        shift (int): Number of positions to shift each letter
        
    Returns:
        str: The encrypted text
    """
    result = []
    
    for i in range(len(text)):
        char = text[i]
        
        # Check if character is a letter
        if 'a' <= char <= 'z':
            # Lowercase letter
            base = ord('a')
            position = ord(char) - base
            new_position = (position + shift) % 26
            result.append(chr(base + new_position))
        elif 'A' <= char <= 'Z':
            # Uppercase letter
            base = ord('A')
            position = ord(char) - base
            new_position = (position + shift) % 26
            result.append(chr(base + new_position))
        else:
            # Non-letter: preserve as-is
            result.append(char)
    
    return ''.join(result)


def caesar_decipher(ciphertext, shift):
    """
    Decrypt text encrypted with Caesar cipher.
    
    Simply calls caesar_cipher with negative shift.
    
    Args:
        ciphertext (str): The encrypted text to decrypt
        shift (int): The shift used for encryption
        
    Returns:
        str: The decrypted text
    """
    return caesar_cipher(ciphertext, -shift)


def letter_frequency(text):
    """
    Count occurrences of each letter a-z in the text.
    
    Case-insensitive (treats 'A' and 'a' as the same).
    Ignores non-alphabetic characters entirely.
    
    Args:
        text (str): The text to analyze
        
    Returns:
        dict: Dictionary mapping letters (a-z) to their counts
    """
    # Initialize dictionary with all letters a-z set to 0
    frequency = {}
    for i in range(26):
        letter = chr(ord('a') + i)
        frequency[letter] = 0
    
    # Count letters (case-insensitive, ignore non-letters)
    for char in text:
        if 'a' <= char <= 'z':
            frequency[char] += 1
        elif 'A' <= char <= 'Z':
            # Convert to lowercase for consistency
            lower_char = chr(ord('a') + (ord(char) - ord('A')))
            frequency[lower_char] += 1
    
    return frequency


def display_frequency(freq):
    """
    Display letter frequency dictionary in a readable format.
    
    Args:
        freq (dict): Dictionary of letter counts
    """
    print("\nLetter Frequency:")
    for letter in sorted(freq.keys()):
        if freq[letter] > 0:
            print(f"  {letter}: {freq[letter]}")


def main():
    """
    Main program with terminal menu for Caesar cipher operations.
    """
    print("Caesar Cipher Program")
    print("=" * 40)
    
    while True:
        print("\nOptions:")
        print("  1. Encrypt a message")
        print("  2. Decrypt a message")
        print("  3. Quit")
        
        choice = input("Enter your choice (1-3): ")
        
        if choice == '3':
            print("Goodbye!")
            break
        
        if choice == '1':
            # Encryption mode
            message = input("Enter the message to encrypt: ")
            shift = int(input("Enter shift value: "))
            
            # Encrypt
            ciphertext = caesar_cipher(message, shift)
            print(f"\nOriginal: {message}")
            print(f"Encrypted: {ciphertext}")
            
            # Show frequency analysis
            print("\n--- Frequency Analysis ---")
            freq = letter_frequency(ciphertext)
            display_frequency(freq)
            
            # Show decryption
            decrypted = caesar_decipher(ciphertext, shift)
            print(f"\nDecrypted (verification): {decrypted}")
            
        elif choice == '2':
            # Decryption mode
            ciphertext = input("Enter the message to decrypt: ")
            shift = int(input("Enter shift value: "))
            
            # Decrypt
            plaintext = caesar_decipher(ciphertext, shift)
            print(f"\nCiphertext: {ciphertext}")
            print(f"Decrypted: {plaintext}")
            
            # Show frequency analysis of ciphertext
            print("\n--- Frequency Analysis ---")
            freq = letter_frequency(ciphertext)
            display_frequency(freq)
            
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


# Run the program
if __name__ == "__main__":
    main()