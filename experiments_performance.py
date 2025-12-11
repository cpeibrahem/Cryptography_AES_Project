import os  # Random bytes for plaintext
import time  # Timing measurements
import csv  # CSV writing
from pathlib import Path  # Path handling

from aes_impl import (
    generate_aes_key,  # Key generator
    generate_iv,  # IV generator
    aes_encrypt_cbc,  # Encrypt helper
    aes_decrypt_cbc,  # Decrypt helper
    BLOCK_SIZE,  # AES block size
)

PLAINTEXT_DIR = Path("data/plaintext")  # Fixture directory
RESULTS_DIR = Path("data/results")  # Results directory

PLAINTEXT_DIR.mkdir(parents=True, exist_ok=True)  # Ensure plaintext folder exists
RESULTS_DIR.mkdir(parents=True, exist_ok=True)  # Ensure results folder exists

# Generate random plaintext fixtures if missing
def generate_plaintext_files():
    sizes = {
        "pt_1KB.bin": 1 * 1024,  # 1 KB
        "pt_10KB.bin": 10 * 1024,  # 10 KB
        "pt_100KB.bin": 100 * 1024,  # 100 KB
        "pt_1MB.bin": 1024 * 1024,  # 1 MB
    }

    for filename, size in sizes.items():
        path = PLAINTEXT_DIR / filename  # Target file path
        if not path.exists():
            print(f"Generating {path} ({size} bytes)")  # Log generation
            data = os.urandom(size)  # Random data
            path.write_bytes(data)  # Write file
        else:
            print(f"{path} already exists, skipping.")  # Skip existing

# Time AES encrypt/decrypt for one plaintext and key size
def time_encrypt_decrypt(plaintext: bytes, key_size_bits: int, runs: int = 10):
    key = generate_aes_key(key_size_bits)  # Fresh key
    iv = generate_iv()  # Fresh IV

    enc_times = []  # Collect encrypt times
    for _ in range(runs):
        start = time.perf_counter()  # Start timer
        ciphertext = aes_encrypt_cbc(plaintext, key, iv)  # Encrypt
        end = time.perf_counter()  # Stop timer
        enc_times.append((end - start) * 1000.0)  # ms duration

    dec_times = []  # Collect decrypt times
    for _ in range(runs):
        ciphertext = aes_encrypt_cbc(plaintext, key, iv)  # Fresh ciphertext
        start = time.perf_counter()  # Start timer
        _ = aes_decrypt_cbc(ciphertext, key, iv)  # Decrypt
        end = time.perf_counter()  # Stop timer
        dec_times.append((end - start) * 1000.0)  # ms duration

    avg_enc = sum(enc_times) / len(enc_times)  # Mean encrypt time
    avg_dec = sum(dec_times) / len(dec_times)  # Mean decrypt time

    return avg_enc, avg_dec  # Return averages

# Main performance loop across files and key sizes; writes CSV
def run_performance_experiments():
    generate_plaintext_files()  # Ensure fixtures

    key_sizes = [128, 192, 256]  # AES key sizes
    plaintext_files = sorted(PLAINTEXT_DIR.glob("pt_*.bin"))  # All fixtures

    csv_path = RESULTS_DIR / "results_performance.csv"  # Output CSV path
    with csv_path.open("w", newline="") as f:
        writer = csv.writer(f)  # CSV writer
        writer.writerow([
            "file_name",  # Fixture name
            "file_size_bytes",  # Size in bytes
            "key_size_bits",  # AES key size
            "avg_enc_time_ms",  # Mean encrypt time
            "avg_dec_time_ms",  # Mean decrypt time
            "runs",  # Number of runs
        ])

        for pt_file in plaintext_files:
            data = pt_file.read_bytes()  # Load plaintext
            file_size = len(data)  # Size of plaintext
            for key_size in key_sizes:
                print(f"Testing {pt_file.name} with AES-{key_size}")  # Log test
                avg_enc, avg_dec = time_encrypt_decrypt(data, key_size, runs=10)  # Measure

                writer.writerow([
                    pt_file.name,  # Name
                    file_size,  # Size
                    key_size,  # Key size
                    f"{avg_enc:.4f}",  # Encrypt ms
                    f"{avg_dec:.4f}",  # Decrypt ms
                    10,  # Runs
                ])

    print(f"Performance results saved to: {csv_path}")  # Done message

if __name__ == "__main__":
    run_performance_experiments()  # Entry point
