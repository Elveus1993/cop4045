"""
Unit tests for Caesar Cipher functions
Problem 5 - CS Assignment
"""

import unittest
from p5_Elveus_Edna import caesar_cipher, caesar_decipher, letter_frequency


class TestCaesarCipher(unittest.TestCase):
    """Test cases for Caesar cipher functions."""
    
    def test_caesar_cipher_basic(self):
        """Test basic encryption with positive shift."""
        self.assertEqual(caesar_cipher("abc", 1), "bcd")
        self.assertEqual(caesar_cipher("xyz", 1), "yza")
        self.assertEqual(caesar_cipher("ABC", 1), "BCD")
        self.assertEqual(caesar_cipher("XYZ", 1), "YZA")
    
    def test_caesar_cipher_negative_shift(self):
        """Test encryption with negative shift."""
        self.assertEqual(caesar_cipher("bcd", -1), "abc")
        self.assertEqual(caesar_cipher("yza", -1), "xyz")
        self.assertEqual(caesar_cipher("BCD", -1), "ABC")
        self.assertEqual(caesar_cipher("YZA", -1), "XYZ")
    
    def test_caesar_cipher_zero_shift(self):
        """Test encryption with zero shift (no change)."""
        text = "Hello World"
        self.assertEqual(caesar_cipher(text, 0), text)
    
    def test_caesar_cipher_case_preservation(self):
        """Test that case is preserved during encryption."""
        self.assertEqual(caesar_cipher("AbC", 1), "BcD")
        self.assertEqual(caesar_cipher("ZyX", 1), "AzY")
    
    def test_caesar_cipher_non_letters(self):
        """Test that spaces and punctuation are preserved."""
        text = "Hello, World!"
        encrypted = caesar_cipher(text, 1)
        self.assertEqual(encrypted, "Ifmmp, Xpsme!")
        self.assertEqual(encrypted[5], ',')  # Comma preserved
        self.assertEqual(encrypted[6], ' ')  # Space preserved
        self.assertEqual(encrypted[-1], '!')  # Exclamation preserved
    
    def test_caesar_cipher_large_shift(self):
        """Test with large shift values (wrapping)."""
        self.assertEqual(caesar_cipher("abc", 26), "abc")
        self.assertEqual(caesar_cipher("abc", 27), "bcd")
        self.assertEqual(caesar_cipher("abc", -26), "abc")
        self.assertEqual(caesar_cipher("abc", -27), "zab")
    
    def test_caesar_decipher(self):
        """Test decryption function."""
        plaintext = "Hello World"
        shift = 5
        ciphertext = caesar_cipher(plaintext, shift)
        self.assertEqual(caesar_decipher(ciphertext, shift), plaintext)
    
    def test_caesar_decipher_negative_shift(self):
        """Test decryption with negative shift."""
        plaintext = "Hello World"
        shift = -5
        ciphertext = caesar_cipher(plaintext, shift)
        self.assertEqual(caesar_decipher(ciphertext, shift), plaintext)
    
    def test_letter_frequency_basic(self):
        """Test basic letter frequency counting."""
        freq = letter_frequency("abc")
        self.assertEqual(freq['a'], 1)
        self.assertEqual(freq['b'], 1)
        self.assertEqual(freq['c'], 1)
        self.assertEqual(freq['d'], 0)
    
    def test_letter_frequency_case_insensitive(self):
        """Test that frequency counting is case-insensitive."""
        freq = letter_frequency("AaBb")
        self.assertEqual(freq['a'], 2)
        self.assertEqual(freq['b'], 2)
        self.assertEqual(freq['c'], 0)
    
    def test_letter_frequency_ignore_non_letters(self):
        """Test that non-alphabetic characters are ignored."""
        freq = letter_frequency("a1b2c3!@#")
        self.assertEqual(freq['a'], 1)
        self.assertEqual(freq['b'], 1)
        self.assertEqual(freq['c'], 1)
        self.assertEqual(freq['d'], 0)
    
    def test_letter_frequency_mixed_text(self):
        """Test frequency counting on mixed text."""
        text = "Hello World"
        freq = letter_frequency(text)
        self.assertEqual(freq['h'], 1)  # 'h' in 'Hello'
        self.assertEqual(freq['e'], 1)
        self.assertEqual(freq['l'], 3)  # 'Hello' has 2, 'World' has 1
        self.assertEqual(freq['o'], 2)  # 'Hello' and 'World'
        self.assertEqual(freq['w'], 1)
        self.assertEqual(freq['r'], 1)
        self.assertEqual(freq['d'], 1)


if __name__ == "__main__":
    unittest.main()