#!/usr/bin/env python3
"""Generate a LaTeX report with detailed statistics for every play-by-play dataset."""

from __future__ import annotations

import math
from datetime import datetime
from pathlib import Path
from typing import Iterable, Tuple

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = ROOT / "raw_data"
REPORT_DIR = ROOT / "reports"
REPORT_PATH = REPORT_DIR / "nfl_play_by_play_stats.tex"

REPORT_DIR.mkdir(parents=True, exist_ok=True)

# Pandas output options keep memory usage reasonable
pd.options.mode.copy_on_write = True


def _format_float(value: float, digits: int = 6) -> str:
    """Return a nicely formatted float string or an empty string for NaN."""
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return ""
    return f"{value:.{digits}f}"


def _format_percent(value: float) -> str:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return ""
    return f"{value:.2f}"


def _compute_numeric_stats(df: pd.DataFrame) -> pd.DataFrame:
    numeric_cols = df.select_dtypes(include=[np.number]).columns.to_list()
    if not numeric_cols:
        return pd.DataFrame()

    numeric_df = df[numeric_cols]
    stats = pd.DataFrame(index=numeric_cols)
    stats["non_null"] = numeric_df.count()
    stats["missing_pct"] = (1 - stats["non_null"] / len(df)) * 100
    stats["distinct"] = numeric_df.nunique(dropna=True)
    stats["mean"] = numeric_df.mean()
    stats["std"] = numeric_df.std()
    stats["min"] = numeric_df.min()
    stats["p25"] = numeric_df.quantile(0.25)
    stats["median"] = numeric_df.median()
    stats["p75"] = numeric_df.quantile(0.75)
    stats["max"] = numeric_df.max()

    stats.index.name = "column"
    stats = stats.reset_index()

    stats["non_null"] = stats["non_null"].astype(int)
    stats["distinct"] = stats["distinct"].astype(int)
    stats["missing_pct"] = stats["missing_pct"].apply(_format_percent)

    float_cols = ["mean", "std", "min", "p25", "median", "p75", "max"]
    for col in float_cols:
        stats[col] = stats[col].apply(_format_float)

    return stats


def _top_value(series: pd.Series) -> Tuple[str, int]:
    counts = series.value_counts(dropna=True)
    if counts.empty:
        return "", 0
    top = str(counts.index[0])
    freq = int(counts.iloc[0])
    return top, freq


def _compute_non_numeric_stats(df: pd.DataFrame) -> pd.DataFrame:
    non_numeric_cols = df.select_dtypes(exclude=[np.number]).columns.to_list()
    if not non_numeric_cols:
        return pd.DataFrame()

    records = []
    total_rows = len(df)
    for col in non_numeric_cols:
        series = df[col]
        non_null = int(series.notna().sum())
        missing_pct = (1 - non_null / total_rows) * 100
        unique = int(series.dropna().nunique())
        top, freq = _top_value(series)

        sample_min = ""
        sample_max = ""
        if pd.api.types.is_datetime64_any_dtype(series):
            if non_null:
                sample_min = str(series.min())
                sample_max = str(series.max())
        records.append(
            {
                "column": col,
                "non_null": non_null,
                "missing_pct": _format_percent(missing_pct),
                "unique": unique,
                "top": top,
                "top_freq": freq,
                "sample_min": sample_min,
                "sample_max": sample_max,
            }
        )

    stats = pd.DataFrame(records)
    stats.sort_values("column", inplace=True)
    return stats


def _build_column_format(df: pd.DataFrame, text_overrides: dict[str, str]) -> str | None:
    if df.empty:
        return None

    parts: list[str] = []
    for col in df.columns:
        if col in text_overrides:
            parts.append(text_overrides[col])
        else:
            parts.append("r")
    return "".join(parts)


def _df_to_latex(df: pd.DataFrame, caption: str, column_format: str | None = None) -> str:
    if df.empty:
        return "\\paragraph{} No columns in this category.\n"
    latex_table = df.to_latex(
        index=False,
        longtable=True,
        escape=True,
        column_format=column_format,
    )
    return (
        f"\\paragraph{{{caption}}}\n"
        "\\begingroup\\setlength{\\tabcolsep}{4pt}\\scriptsize\n"
        f"{latex_table}\n"
        "\\endgroup\n"
    )


def _build_document(sections: Iterable[str], summary_table: pd.DataFrame) -> str:
    today = datetime.now().strftime("%B %d, %Y")
    header = [
        "\\documentclass{article}",
        "\\usepackage{booktabs}",
        "\\usepackage{longtable}",
    "\\usepackage{array}",
        "\\usepackage{geometry}",
        "\\usepackage{pdflscape}",
        "\\geometry{margin=1in}",
        "",
        "\\begin{document}",
        "\\title{NFL Play-by-Play Statistical Analysis}",
        f"\\date{{Generated on {today}}}",
        "\\maketitle",
        "\\tableofcontents",
        "",
    ]

    summary_table = summary_table.copy()
    summary_table.sort_values("Year", inplace=True)
    summary_table["Rows"] = summary_table["Rows"].map(lambda x: f"{x:,}")
    summary_table["Columns"] = summary_table["Columns"].map(lambda x: f"{x}")

    header.append("\\section{Dataset Overview}")
    header.append(
        summary_table.to_latex(
            index=False,
            longtable=False,
            escape=True,
            caption="Per-year dataset overview",
        )
    )
    header.append("\\clearpage")

    document = header + list(sections) + ["\\end{document}"]
    return "\n".join(document)


def main() -> None:
    parquet_files = sorted(RAW_DATA_DIR.glob("play_by_play_*.parquet"))
    if not parquet_files:
        raise FileNotFoundError("No play_by_play_*.parquet files found in raw_data directory")

    sections: list[str] = []
    summary_records = []

    for dataset_path in parquet_files:
        df = pd.read_parquet(dataset_path)
        year = dataset_path.stem.split("_")[-1]
        rows, columns = df.shape

        numeric_stats = _compute_numeric_stats(df)
        non_numeric_stats = _compute_non_numeric_stats(df)

        numeric_format = _build_column_format(
            numeric_stats,
            {
                "column": "p{4.5cm}",
            },
        )
        non_numeric_format = _build_column_format(
            non_numeric_stats,
            {
                "column": "p{4.5cm}",
                "top": "p{4.5cm}",
                "sample_min": "p{4.5cm}",
                "sample_max": "p{4.5cm}",
            },
        )

        sections.append(f"\\section{{Season {year}}}")
        sections.append(f"\\noindent\\textbf{{Rows}}: {rows:,}\\newline")
        sections.append(f"\\noindent\\textbf{{Columns}}: {columns}\\newline")
        sections.append(
            f"\\noindent\\textbf{{Numeric Columns}}: {numeric_stats.shape[0]}\\newline"
        )
        sections.append(
            f"\\noindent\\textbf{{Non-numeric Columns}}: {non_numeric_stats.shape[0]}\\newline"
        )
        sections.append("\\begin{landscape}")
        sections.append(
            _df_to_latex(
                numeric_stats,
                "Numeric column summary",
                column_format=numeric_format,
            )
        )
        sections.append("\\clearpage")
        sections.append(
            _df_to_latex(
                non_numeric_stats,
                "Non-numeric column summary",
                column_format=non_numeric_format,
            )
        )
        sections.append("\\end{landscape}")
        sections.append("\\clearpage")

        summary_records.append(
            {
                "Year": year,
                "Rows": rows,
                "Columns": columns,
                "Numeric Columns": numeric_stats.shape[0],
                "Non-numeric Columns": non_numeric_stats.shape[0],
            }
        )

    summary_table = pd.DataFrame(summary_records)
    latex_doc = _build_document(sections, summary_table)

    REPORT_PATH.write_text(latex_doc, encoding="utf-8")


if __name__ == "__main__":
    main()
