import argparse  # CLI parsing
from pathlib import Path  # Path handling

import matplotlib.pyplot as plt  # Plotting
import pandas as pd  # CSV loading

RESULTS_DIR = Path("data/results")  # Results folder
PLOTS_DIR = RESULTS_DIR / "plots"  # Plots subfolder
PLOTS_DIR.mkdir(parents=True, exist_ok=True)  # Ensure plots folder exists


def preview_csv(path: Path, label: str, head_rows: int = 5) -> pd.DataFrame | None:
    if not path.exists():
        print(f"{label}: missing at {path}")  # Inform if missing
        return None  # Nothing to preview

    df = pd.read_csv(path)  # Load CSV
    print(f"{label}: {len(df)} rows from {path}")  # Row count
    print(df.head(head_rows))  # Preview head
    return df  # Return DataFrame


def plot_performance(df: pd.DataFrame | None, save_path: Path, show: bool) -> None:
    if df is None or df.empty:
        print("Performance data missing or empty; skipping plot.")  # Guard empty
        return  # Skip plotting

    perf = df.copy()  # Work on a copy
    perf["avg_enc_time_ms"] = pd.to_numeric(perf["avg_enc_time_ms"], errors="coerce")  # Ensure numeric
    perf["avg_dec_time_ms"] = pd.to_numeric(perf["avg_dec_time_ms"], errors="coerce")  # Ensure numeric
    perf["file_size_bytes"] = pd.to_numeric(perf["file_size_bytes"], errors="coerce")  # Ensure numeric
    perf = perf.dropna(subset=["avg_enc_time_ms", "avg_dec_time_ms", "file_size_bytes"]).sort_values("file_size_bytes")  # Clean rows
    perf["size_kb"] = perf["file_size_bytes"] / 1024.0  # Convert size to KB

    fig, axes = plt.subplots(1, 2, figsize=(10, 4), sharex=True)  # Two subplots

    for key_size, group in perf.groupby("key_size_bits"):
        axes[0].plot(group["size_kb"], group["avg_enc_time_ms"], marker="o", label=f"AES-{key_size}")  # Encrypt line
        axes[1].plot(group["size_kb"], group["avg_dec_time_ms"], marker="o", label=f"AES-{key_size}")  # Decrypt line

    axes[0].set_title("Encrypt time")  # Title left
    axes[0].set_ylabel("ms")  # Y label left
    axes[1].set_title("Decrypt time")  # Title right
    for ax in axes:
        ax.set_xlabel("File size (KB)")  # X label
        ax.grid(True, alpha=0.3)  # Grid
        ax.legend()  # Legend

    fig.suptitle("AES CBC performance")  # Overall title
    fig.tight_layout()  # Layout
    fig.savefig(save_path)  # Save PNG
    if show:
        plt.show()  # Optional display
    plt.close(fig)  # Free resources
    print(f"Saved performance plot to {save_path}")  # Log save


def plot_avalanche(df: pd.DataFrame | None, save_path: Path, show: bool) -> None:
    if df is None or df.empty:
        print("Avalanche data missing or empty; skipping plot.")  # Guard empty
        return  # Skip plotting

    aval = df.copy()  # Work on a copy
    aval["avalanche_percent"] = pd.to_numeric(aval["avalanche_percent"], errors="coerce")  # Ensure numeric
    aval = aval.dropna(subset=["avalanche_percent"]).sort_values("key_size_bits")  # Clean rows

    fig, ax = plt.subplots(figsize=(6, 4))  # Single subplot
    for label, group in aval.groupby("type"):
        ax.hist(group["avalanche_percent"], bins=20, alpha=0.6, label=f"{label} flip")  # Histogram per type

    ax.set_title("Avalanche effect distribution")  # Title
    ax.set_xlabel("Changed bits (%)")  # X label
    ax.set_ylabel("Count")  # Y label
    ax.grid(True, alpha=0.3)  # Grid
    ax.legend()  # Legend

    fig.tight_layout()  # Layout
    fig.savefig(save_path)  # Save PNG
    if show:
        plt.show()  # Optional display
    plt.close(fig)  # Free resources
    print(f"Saved avalanche plot to {save_path}")  # Log save


def main() -> None:
    parser = argparse.ArgumentParser(description="Preview CSV outputs and render quick plots.")  # CLI parser
    parser.add_argument("--show", action="store_true", help="Display plots interactively in addition to saving.")  # Flag
    args = parser.parse_args()  # Parse args

    perf_csv = RESULTS_DIR / "results_performance.csv"  # Performance CSV path
    aval_csv = RESULTS_DIR / "results_avalanche.csv"  # Avalanche CSV path

    perf_df = preview_csv(perf_csv, label="Performance")  # Load performance
    aval_df = preview_csv(aval_csv, label="Avalanche")  # Load avalanche

    plot_performance(perf_df, PLOTS_DIR / "performance.png", show=args.show)  # Save performance plot
    plot_avalanche(aval_df, PLOTS_DIR / "avalanche.png", show=args.show)  # Save avalanche plot


if __name__ == "__main__":
    main()  # Entry point
