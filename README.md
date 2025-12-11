# Cryptography AES Project

> **مشروع تشفير AES** — تنفيذ خوارزمية AES بوضع CBC مع تجارب الأداء وتأثير الانهيار (Avalanche Effect).

---

## 📋 Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Project Structure](#project-structure)
4. [Prerequisites](#prerequisites)
5. [Installation](#installation)
6. [Usage](#usage)
7. [Output Files](#output-files)
8. [Algorithm Details](#algorithm-details)
9. [Experiments](#experiments)
10. [Sample Results](#sample-results)
11. [Troubleshooting](#troubleshooting)
12. [References](#references)
13. [License](#license)

---

## Introduction

This project implements **AES (Advanced Encryption Standard)** encryption/decryption using:
- **Mode**: CBC (Cipher Block Chaining)
- **Padding**: PKCS#7
- **Key Sizes**: 128, 192, 256 bits

The project includes two experimental studies:
1. **Performance Analysis**: Measure encryption/decryption time across different file sizes and key lengths.
2. **Avalanche Effect**: Analyze how a single bit change in plaintext or key affects the ciphertext.

---

## Features

✅ AES-CBC encryption/decryption with PKCS#7 padding  
✅ Support for 128, 192, 256-bit keys  
✅ Secure random key and IV generation  
✅ File encryption/decryption helpers  
✅ Performance benchmarking (timing experiments)  
✅ Avalanche effect analysis (bit-flip experiments)  
✅ CSV output for data analysis  
✅ Automatic plot generation (PNG)  
✅ Fully commented code for easy understanding  

---

## Project Structure

```
Cryptography_AES_Project/
├── aes_impl.py                 # Core AES implementation
├── experiments_performance.py  # Performance timing experiments
├── experiments_avalanche.py    # Avalanche effect experiments
├── results_preview.py          # CSV preview and plot generation
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── data/
│   ├── plaintext/              # Generated test files
│   │   ├── pt_1KB.bin
│   │   ├── pt_10KB.bin
│   │   ├── pt_100KB.bin
│   │   └── pt_1MB.bin
│   └── results/
│       ├── results_performance.csv
│       ├── results_avalanche.csv
│       └── plots/
│           ├── performance.png
│           └── avalanche.png
└── venv/                       # Virtual environment (optional)
```

---

## Prerequisites

- **Python**: 3.10 or higher (tested on 3.11)
- **OS**: Windows 10/11 (also works on Linux/macOS)
- **Libraries**:
  - `pycryptodome` — AES implementation
  - `pandas` — CSV handling
  - `matplotlib` — Plot generation

---

## Installation

### Step 1: Clone or Download
```pwsh
cd d:\
# If cloning from git:
# git clone <repo-url> Cryptography_AES_Project
cd Cryptography_AES_Project
```

### Step 2: Create Virtual Environment
```pwsh
python -m venv venv
```

### Step 3: Activate Virtual Environment

**Windows (PowerShell):**
```pwsh
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
venv\Scripts\activate.bat
```

**Linux/macOS:**
```bash
source venv/bin/activate
```

### Step 4: Install Dependencies
```pwsh
pip install -r requirements.txt
```

Or manually:
```pwsh
pip install pycryptodome pandas matplotlib
```

---

## Usage

### 1. Test AES Implementation
```pwsh
.\venv\Scripts\python.exe aes_impl.py
```
**Expected output:**
```
Original: b'Hello AES project!'
Decrypted: b'Hello AES project!'
Match: True
```

### 2. Run Performance Experiments
```pwsh
.\venv\Scripts\python.exe experiments_performance.py
```
**Output:** Creates plaintext files and `data/results/results_performance.csv`

### 3. Run Avalanche Experiments
```pwsh
.\venv\Scripts\python.exe experiments_avalanche.py
```
**Output:** Creates `data/results/results_avalanche.csv`

### 4. Generate Plots
```pwsh
.\venv\Scripts\python.exe results_preview.py
```
**Output:** Creates PNG plots in `data/results/plots/`

Add `--show` flag to display plots interactively:
```pwsh
.\venv\Scripts\python.exe results_preview.py --show
```

---

## Output Files

| File | Description |
|------|-------------|
| `data/plaintext/pt_*.bin` | Random binary test files (1KB, 10KB, 100KB, 1MB) |
| `data/results/results_performance.csv` | Timing data for encrypt/decrypt |
| `data/results/results_avalanche.csv` | Avalanche effect measurements |
| `data/results/plots/performance.png` | Performance graph |
| `data/results/plots/avalanche.png` | Avalanche histogram |

---

## Algorithm Details

### AES (Advanced Encryption Standard)
- **Block Size**: 128 bits (16 bytes)
- **Key Sizes**: 128, 192, or 256 bits
- **Rounds**: 10 (AES-128), 12 (AES-192), 14 (AES-256)

### CBC Mode (Cipher Block Chaining)
- Each plaintext block is XORed with the previous ciphertext block before encryption.
- Requires an **Initialization Vector (IV)** for the first block.
- IV must be random and unique for each encryption.

### PKCS#7 Padding
- Pads plaintext to a multiple of the block size.
- Padding value = number of bytes added (e.g., if 5 bytes needed, pad with `05 05 05 05 05`).

### File Format
Encrypted files store: `[IV (16 bytes)] + [Ciphertext]`

---

## Experiments

### Performance Experiment
- **Goal**: Measure encryption/decryption time.
- **Variables**:
  - File sizes: 1KB, 10KB, 100KB, 1MB
  - Key sizes: 128, 192, 256 bits
- **Runs**: 10 iterations per configuration (averaged)
- **Output**: CSV with columns: `file_name, file_size_bytes, key_size_bits, avg_enc_time_ms, avg_dec_time_ms, runs`

### Avalanche Experiment
- **Goal**: Measure ciphertext change when input changes by 1 bit.
- **Tests**:
  1. **Plaintext flip**: Change 1 bit in plaintext, same key/IV
  2. **Key flip**: Change 1 bit in key, same plaintext/IV
- **Metric**: Hamming distance as percentage of total bits
- **Trials**: 50 per key size
- **Expected**: ~50% change (ideal avalanche effect)

---

## Sample Results

### Performance CSV Preview
| file_name | file_size_bytes | key_size_bits | avg_enc_time_ms | avg_dec_time_ms |
|-----------|-----------------|---------------|-----------------|-----------------|
| pt_1KB.bin | 1024 | 128 | 0.0512 | 0.0347 |
| pt_1MB.bin | 1048576 | 256 | 3.2145 | 2.8901 |

### Avalanche CSV Preview
| trial | type | key_size_bits | avalanche_percent |
|-------|------|---------------|-------------------|
| 1 | plaintext | 128 | 48.75 |
| 1 | key | 128 | 51.25 |

---

## Troubleshooting

### "Import Crypto.Cipher could not be resolved"
- Ensure you activated the virtual environment.
- Run: `pip install pycryptodome`

### "python is not recognized"
- Add Python to your PATH, or use full path: `C:\Python311\python.exe`

### Plots not showing
- Use `--show` flag with `results_preview.py`
- Or open the PNG files directly from `data/results/plots/`

### Permission denied
- Run PowerShell as Administrator, or check folder permissions.

---

## References

1. **NIST FIPS 197** — Advanced Encryption Standard (AES)  
   https://csrc.nist.gov/publications/detail/fips/197/final

2. **PyCryptodome Documentation**  
   https://pycryptodome.readthedocs.io/

3. **CBC Mode** — Wikipedia  
   https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#CBC

4. **Avalanche Effect** — Wikipedia  
   https://en.wikipedia.org/wiki/Avalanche_effect

5. **PKCS#7 Padding** — RFC 5652  
   https://datatracker.ietf.org/doc/html/rfc5652#section-6.3

---

## License

This project is for **educational purposes** as part of a cryptography course project.

---

## Author

Cryptography Course Project — December 2025

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-12-11 | Initial release with AES-CBC, performance & avalanche experiments |
