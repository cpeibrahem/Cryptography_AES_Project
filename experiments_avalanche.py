import os  # Random plaintext/key data
import csv  # CSV writing
import random  # Random bit selection
from pathlib import Path  # Path handling

from aes_impl import (
    generate_aes_key,  # Key generator
    generate_iv,  # IV generator
    aes_encrypt_cbc,  # Encrypt helper
    BLOCK_SIZE,  # AES block size
)

RESULTS_DIR = Path("data/results")  # Results directory
RESULTS_DIR.mkdir(parents=True, exist_ok=True)  # Ensure it exists

# Flip one random bit in the given bytes
def flip_one_bit(data: bytes) -> bytes:
    if len(data) == 0:
        raise ValueError("Data must not be empty")  # Guard empty input

    data_list = bytearray(data)  # Mutable copy

    byte_index = random.randint(0, len(data_list) - 1)  # Choose byte
    bit_index = random.randint(0, 7)  # Choose bit

    mask = 1 << bit_index  # Bit mask
    data_list[byte_index] ^= mask  # Flip bit

    return bytes(data_list)  # Return bytes

# Count differing bits between two equal-length byte strings
def hamming_distance(b1: bytes, b2: bytes) -> int:
    if len(b1) != len(b2):
        raise ValueError("Inputs must have the same length for Hamming distance")  # Length check

    distance = 0  # Accumulator
    for x, y in zip(b1, b2):
        diff = x ^ y  # XOR to find differing bits
        distance += diff.bit_count()  # Count bits set
    return distance  # Total differing bits

# Convert Hamming distance to percentage of bits flipped
def avalanche_percentage(b1: bytes, b2: bytes) -> float:
    if len(b1) != len(b2):
        raise ValueError("Inputs must have the same length for avalanche calculation")  # Length check

    total_bits = len(b1) * 8  # Total bits compared
    hd = hamming_distance(b1, b2)  # Hamming distance
    return (hd / total_bits) * 100.0  # Percentage flipped

# Experiment: flip plaintext bit with fixed key/IV
def experiment_plaintext_avalanche(num_trials: int = 50, key_size_bits: int = 128):
    key = generate_aes_key(key_size_bits)  # Fixed key
    iv = generate_iv()  # Fixed IV

    results = []  # Collect rows

    for i in range(num_trials):
        plaintext = os.urandom(BLOCK_SIZE * 4)  # Random plaintext (4 blocks)
        plaintext_flipped = flip_one_bit(plaintext)  # One-bit flip

        c1 = aes_encrypt_cbc(plaintext, key, iv)  # Ciphertext baseline
        c2 = aes_encrypt_cbc(plaintext_flipped, key, iv)  # Ciphertext flipped

        perc = avalanche_percentage(c1, c2)  # Avalanche percent

        results.append({
            "trial": i + 1,  # Trial number
            "type": "plaintext",  # Flip type
            "key_size_bits": key_size_bits,  # AES size
            "avalanche_percent": perc,  # Result
        })

    return results  # All plaintext-flip rows

# Experiment: flip key bit with fixed plaintext
def experiment_key_avalanche(num_trials: int = 50, key_size_bits: int = 128):
    plaintext = os.urandom(BLOCK_SIZE * 4)  # Fixed plaintext

    results = []  # Collect rows

    for i in range(num_trials):
        key = generate_aes_key(key_size_bits)  # Random key
        key_flipped = flip_one_bit(key)  # One-bit-flipped key

        iv = generate_iv()  # Fresh IV per trial

        c1 = aes_encrypt_cbc(plaintext, key, iv)  # Ciphertext baseline
        c2 = aes_encrypt_cbc(plaintext, key_flipped, iv)  # Ciphertext flipped

        perc = avalanche_percentage(c1, c2)  # Avalanche percent

        results.append({
            "trial": i + 1,  # Trial number
            "type": "key",  # Flip type
            "key_size_bits": key_size_bits,  # AES size
            "avalanche_percent": perc,  # Result
        })

    return results  # All key-flip rows

# Run all avalanche experiments across key sizes and write CSV
def run_avalanche_experiments():
    num_trials = 50  # Trials per experiment
    key_sizes = [128, 192, 256]  # AES key sizes

    all_results = []  # Accumulate rows

    for ks in key_sizes:
        print(f"Running plaintext avalanche for AES-{ks}")  # Log
        all_results.extend(experiment_plaintext_avalanche(num_trials=num_trials, key_size_bits=ks))  # Plaintext flips

        print(f"Running key avalanche for AES-{ks}")  # Log
        all_results.extend(experiment_key_avalanche(num_trials=num_trials, key_size_bits=ks))  # Key flips

    csv_path = RESULTS_DIR / "results_avalanche.csv"  # Output CSV path
    with csv_path.open("w", newline="") as f:
        writer = csv.writer(f)  # CSV writer
        writer.writerow(["trial", "type", "key_size_bits", "avalanche_percent"])  # Header

        for row in all_results:
            writer.writerow([
                row["trial"],  # Trial number
                row["type"],  # Flip type
                row["key_size_bits"],  # AES size
                f"{row['avalanche_percent']:.4f}",  # Avalanche %
            ])

    print(f"Avalanche results saved to: {csv_path}")  # Done message

if __name__ == "__main__":
    run_avalanche_experiments()  # Entry point
