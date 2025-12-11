from pathlib import Path  # Filesystem paths
from Crypto.Cipher import AES  # AES cipher implementation
from Crypto.Random import get_random_bytes  # Cryptographically secure RNG

BLOCK_SIZE = 16  # AES block size in bytes

def pkcs7_pad(data: bytes, block_size: int = BLOCK_SIZE) -> bytes:
    pad_len = block_size - (len(data) % block_size)  # How many bytes to add
    return data + bytes([pad_len] * pad_len)  # Append padding bytes

def pkcs7_unpad(padded_data: bytes, block_size: int = BLOCK_SIZE) -> bytes:
    if len(padded_data) == 0 or len(padded_data) % block_size != 0:
        raise ValueError("Invalid padded data length")  # Reject bad lengths

    pad_len = padded_data[-1]  # Last byte is pad length
    if pad_len < 1 or pad_len > block_size:
        raise ValueError("Invalid padding length byte")  # Reject out-of-range pad

    if padded_data[-pad_len:] != bytes([pad_len] * pad_len):
        raise ValueError("Invalid PKCS#7 padding bytes")  # Reject wrong pad pattern

    return padded_data[:-pad_len]  # Strip padding

def generate_aes_key(key_size_bits: int) -> bytes:
    """Generate an AES key for the given size in bits (128, 192, 256)."""
    if key_size_bits not in (128, 192, 256):
        raise ValueError("Key size must be 128, 192, or 256 bits.")  # Enforce valid sizes
    return get_random_bytes(key_size_bits // 8)  # Random key of requested size

def generate_iv() -> bytes:
    return get_random_bytes(BLOCK_SIZE)  # Fresh IV per encryption

def aes_encrypt_cbc(plaintext: bytes, key: bytes, iv: bytes) -> bytes:
    padded = pkcs7_pad(plaintext, BLOCK_SIZE)  # Pad plaintext to block size
    cipher = AES.new(key, AES.MODE_CBC, iv)  # CBC-mode cipher
    ciphertext = cipher.encrypt(padded)  # Encrypt padded plaintext
    return ciphertext

def aes_decrypt_cbc(ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_CBC, iv)  # CBC-mode cipher
    padded = cipher.decrypt(ciphertext)  # Decrypt to padded plaintext
    plaintext = pkcs7_unpad(padded, BLOCK_SIZE)  # Remove padding
    return plaintext

def encrypt_file_cbc(input_path: str, output_path: str, key_size_bits: int = 128):
    input_file = Path(input_path)  # Input file path
    data = input_file.read_bytes()  # Read entire file

    key = generate_aes_key(key_size_bits)  # Fresh key
    iv = generate_iv()  # Fresh IV

    ciphertext = aes_encrypt_cbc(data, key, iv)  # Encrypt file contents

    out_file = Path(output_path)  # Output file path
    out_file.write_bytes(iv + ciphertext)  # Store IV || ciphertext

    return key, iv  # Return key/IV for later decrypt

def decrypt_file_cbc(input_path: str, output_path: str, key: bytes):
    input_file = Path(input_path)  # Encrypted file path
    raw = input_file.read_bytes()  # Read IV || ciphertext

    iv = raw[:BLOCK_SIZE]  # Extract IV
    ciphertext = raw[BLOCK_SIZE:]  # Extract ciphertext

    plaintext = aes_decrypt_cbc(ciphertext, key, iv)  # Decrypt

    out_file = Path(output_path)  # Output path
    out_file.write_bytes(plaintext)  # Write plaintext

if __name__ == "__main__":
    msg = b"Hello AES project!"  # Test message
    key = generate_aes_key(128)  # Sample key
    iv = generate_iv()  # Sample IV

    c = aes_encrypt_cbc(msg, key, iv)  # Encrypt
    p = aes_decrypt_cbc(c, key, iv)  # Decrypt

    print("Original:", msg)  # Show original
    print("Decrypted:", p)  # Show decrypted
    print("Match:", msg == p)  # Verify round-trip
