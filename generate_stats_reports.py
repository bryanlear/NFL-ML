from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).parent
REPORTS_DIR = BASE_DIR / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

PARQUET_FILES = {
    "play_by_play_2021": BASE_DIR / "raw_data" / "play_by_play_2021.parquet",
    "play_by_play_2022": BASE_DIR / "raw_data" / "play_by_play_2022.parquet",
    "play_by_play_2023": BASE_DIR / "raw_data" / "play_by_play_2023.parquet",
    "play_by_play_2024": BASE_DIR / "raw_data" / "play_by_play_2024.parquet",
    "play_by_play_2025": BASE_DIR / "raw_data" / "play_by_play_2025.parquet",
}


def build_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Return a descriptive summary augmented with dtype and null metrics."""
    summary = df.describe(include="all", datetime_is_numeric=True).transpose()
    summary.insert(0, "dtype", df.dtypes.astype(str))
    missing_count = df.isna().sum()
    summary.insert(1, "missing_count", missing_count)
    summary.insert(2, "missing_pct", (missing_count / len(df) * 100).round(2))
    return summary


def main() -> None:
    for label, file_path in PARQUET_FILES.items():
        if not file_path.exists():
            print(f"⚠️ Skipping {label}: file not found at {file_path}")
            continue

        print(f"Processing {label} ...")
        df = pd.read_parquet(file_path)
        summary = build_summary(df)

        summary_path = REPORTS_DIR / f"{label}_stats.csv"
        summary.to_csv(summary_path)
        print(f"✓ Saved stats report to {summary_path}")


if __name__ == "__main__":
    main()
