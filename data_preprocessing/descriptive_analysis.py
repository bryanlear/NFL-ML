"""
Descriptive Statistics Analysis for NFL Play-by-Play Data
Analyzes all parquet files to identify:
- Number of samples (rows) per file
- Missing values (missingness)
- Column consistency across years
- Feature availability for engineering
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Setup paths
PROJECT_ROOT = Path(__file__).parent.parent
RAW_DATA_DIR = PROJECT_ROOT / 'raw_data'
OUTPUT_DIR = Path(__file__).parent / 'analysis_output'
OUTPUT_DIR.mkdir(exist_ok=True)

# Scientific color palette (viridis)
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("viridis")

def load_all_parquet_files():
    """Load all parquet files and return dictionary with metadata."""
    parquet_files = sorted(RAW_DATA_DIR.glob('play_by_play_*.parquet'))
    data_dict = {}
    
    print(f"Found {len(parquet_files)} parquet files")
    print("-" * 80)
    
    for file_path in parquet_files:
        year = file_path.stem.split('_')[-1]
        try:
            df = pd.read_parquet(file_path)
            data_dict[year] = df
            print(f"✓ {file_path.name}: {len(df):,} rows × {len(df.columns)} columns")
        except Exception as e:
            print(f"✗ Error loading {file_path.name}: {e}")
    
    print("-" * 80)
    return data_dict

def analyze_column_consistency(data_dict):
    """Analyze which columns are present across all years."""
    all_columns = {}
    for year, df in sorted(data_dict.items()):
        all_columns[year] = set(df.columns)
    
    # Find common columns across all years
    common_columns = set.intersection(*all_columns.values())
    
    # Find columns unique to specific years
    all_unique = set()
    for cols in all_columns.values():
        all_unique.update(cols)
    
    unique_by_year = {}
    for year, cols in all_columns.items():
        unique = cols - common_columns
        if unique:
            unique_by_year[year] = unique
    
    return {
        'common_columns': sorted(common_columns),
        'all_columns': all_columns,
        'unique_by_year': unique_by_year,
        'total_unique_columns': len(all_unique)
    }

def analyze_missingness(data_dict):
    """Analyze missing values across all files."""
    missingness_dict = {}
    
    for year, df in sorted(data_dict.items()):
        missing_counts = df.isnull().sum()
        missing_pct = (missing_counts / len(df) * 100).round(2)
        missingness_dict[year] = {
            'counts': missing_counts,
            'percentages': missing_pct,
            'has_missing': (missing_counts > 0).any()
        }
    
    return missingness_dict

def generate_summary_report(data_dict, column_analysis, missingness_analysis):
    """Generate comprehensive text report."""
    report = []
    report.append("=" * 100)
    report.append("NFL PLAY-BY-PLAY DATA: DESCRIPTIVE STATISTICS ANALYSIS")
    report.append("=" * 100)
    report.append("")
    
    # Section 1: Dataset Overview
    report.append("1. DATASET OVERVIEW")
    report.append("-" * 100)
    
    total_samples = sum(len(df) for df in data_dict.values())
    report.append(f"Total Files: {len(data_dict)}")
    report.append(f"Years Covered: {min(data_dict.keys())} - {max(data_dict.keys())}")
    report.append(f"Total Samples (rows): {total_samples:,}")
    report.append("")
    
    # Section 2: Samples per Year
    report.append("2. SAMPLES PER YEAR")
    report.append("-" * 100)
    for year in sorted(data_dict.keys()):
        n_rows = len(data_dict[year])
        pct = (n_rows / total_samples * 100)
        report.append(f"  {year}: {n_rows:,} rows ({pct:.1f}%)")
    report.append("")
    
    # Section 3: Column Consistency
    report.append("3. COLUMN CONSISTENCY ANALYSIS")
    report.append("-" * 100)
    common_cols = column_analysis['common_columns']
    report.append(f"Columns Present in ALL Years: {len(common_cols)}")
    report.append(f"Total Unique Columns (across all years): {column_analysis['total_unique_columns']}")
    report.append("")
    
    report.append("Common Columns (present in all years):")
    for i, col in enumerate(common_cols, 1):
        report.append(f"  {i:2d}. {col}")
    report.append("")
    
    if column_analysis['unique_by_year']:
        report.append("Columns Unique to Specific Years:")
        for year in sorted(column_analysis['unique_by_year'].keys()):
            unique_cols = column_analysis['unique_by_year'][year]
            report.append(f"  Year {year}: {', '.join(sorted(unique_cols))}")
        report.append("")
    
    # Section 4: Missingness Analysis
    report.append("4. MISSINGNESS ANALYSIS")
    report.append("-" * 100)
    
    # Find columns with any missing values
    columns_with_missing = set()
    for year_missing in missingness_analysis.values():
        cols_missing = year_missing['counts'][year_missing['counts'] > 0].index.tolist()
        columns_with_missing.update(cols_missing)
    
    report.append(f"Columns with ANY missing values: {len(columns_with_missing)}")
    report.append("")
    
    if columns_with_missing:
        report.append("Columns with Missing Values (by year):")
        for year in sorted(data_dict.keys()):
            missing_pct = missingness_analysis[year]['percentages']
            cols_with_missing_year = missing_pct[missing_pct > 0].sort_values(ascending=False)
            if len(cols_with_missing_year) > 0:
                report.append(f"\n  Year {year}:")
                for col, pct in cols_with_missing_year.items():
                    report.append(f"    {col}: {pct:.2f}%")
    report.append("")
    
    # Section 5: Feature Engineering Candidates
    report.append("5. FEATURE ENGINEERING RECOMMENDATIONS")
    report.append("-" * 100)
    report.append(f"Recommended Features (common columns for all years): {len(common_cols)}")
    report.append("These columns can be reliably used for feature engineering across the entire dataset.")
    report.append("")
    report.append("NEXT STEPS:")
    report.append("1. Review common columns for relevance to ML models")
    report.append("2. Address missing values through imputation or exclusion strategies")
    report.append("3. Consider year-specific features if applicable")
    report.append("4. Perform exploratory data analysis (EDA) on candidate features")
    report.append("")
    report.append("=" * 100)
    
    return "\n".join(report)

def create_missingness_heatmap(data_dict, missingness_analysis):
    """Create heatmap of missingness percentages."""
    # Collect all unique columns
    all_cols = set()
    for df in data_dict.values():
        all_cols.update(df.columns)
    
    # Create matrix: years × columns
    years = sorted(data_dict.keys())
    all_cols = sorted(all_cols)
    
    missing_matrix = np.zeros((len(years), len(all_cols)))
    
    for i, year in enumerate(years):
        missing_pct = missingness_analysis[year]['percentages']
        for j, col in enumerate(all_cols):
            if col in missing_pct.index:
                missing_matrix[i, j] = missing_pct[col]
    
    # Create heatmap
    fig, ax = plt.subplots(figsize=(16, 8))
    im = ax.imshow(missing_matrix, aspect='auto', cmap='viridis', interpolation='nearest')
    
    ax.set_xticks(np.arange(len(all_cols)))
    ax.set_yticks(np.arange(len(years)))
    ax.set_xticklabels(all_cols, rotation=90, fontsize=8)
    ax.set_yticklabels(years, fontsize=10)
    ax.set_xlabel('Columns', fontsize=12, fontweight='bold')
    ax.set_ylabel('Year', fontsize=12, fontweight='bold')
    ax.set_title('Missing Values Heatmap (%) - NFL Play-by-Play Data', 
                  fontsize=14, fontweight='bold', pad=20)
    
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Missing %', fontsize=11)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'missingness_heatmap.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: missingness_heatmap.png")
    plt.close()

def create_samples_per_year_chart(data_dict):
    """Create bar chart of samples per year."""
    years = sorted(data_dict.keys(), key=int)
    counts = [len(data_dict[year]) for year in years]
    
    fig, ax = plt.subplots(figsize=(14, 6))
    bars = ax.bar(years, counts, color=plt.cm.viridis(np.linspace(0, 1, len(years))))
    
    ax.set_xlabel('Year', fontsize=12, fontweight='bold')
    ax.set_ylabel('Number of Samples (rows)', fontsize=12, fontweight='bold')
    ax.set_title('Play-by-Play Samples by Year', fontsize=14, fontweight='bold', pad=20)
    ax.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height):,}',
                ha='center', va='bottom', fontsize=9)
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'samples_per_year.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: samples_per_year.png")
    plt.close()

def create_column_consistency_chart(data_dict):
    """Create visualization of column presence across years."""
    column_analysis = analyze_column_consistency(data_dict)
    common_cols = set(column_analysis['common_columns'])
    
    years = sorted(data_dict.keys(), key=int)
    
    fig, ax = plt.subplots(figsize=(14, 6))
    
    total_cols = [len(data_dict[year].columns) for year in years]
    common_col_count = [len(common_cols)] * len(years)
    unique_cols = [total - common for total, common in zip(total_cols, common_col_count)]
    
    x = np.arange(len(years))
    width = 0.6
    
    # Stacked bar chart
    p1 = ax.bar(x, common_col_count, width, label='Common (all years)',
                color=plt.cm.viridis(0.2))
    p2 = ax.bar(x, unique_cols, width, bottom=common_col_count,
                label='Year-specific', color=plt.cm.viridis(0.8))
    
    ax.set_xlabel('Year', fontsize=12, fontweight='bold')
    ax.set_ylabel('Number of Columns', fontsize=12, fontweight='bold')
    ax.set_title('Column Availability by Year', fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(years)
    ax.legend(loc='upper left', fontsize=11)
    ax.grid(axis='y', alpha=0.3)
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'column_consistency.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: column_consistency.png")
    plt.close()

def main():
    """Main analysis pipeline."""
    print("\n" + "=" * 80)
    print("NFL PLAY-BY-PLAY DATA: DESCRIPTIVE STATISTICS ANALYSIS")
    print("=" * 80 + "\n")
    
    # Load data
    print("Step 1: Loading parquet files...")
    data_dict = load_all_parquet_files()
    print()
    
    # Analyze columns
    print("Step 2: Analyzing column consistency...")
    column_analysis = analyze_column_consistency(data_dict)
    print(f"✓ Common columns across all years: {len(column_analysis['common_columns'])}")
    print(f"✓ Total unique columns: {column_analysis['total_unique_columns']}")
    print()
    
    # Analyze missingness
    print("Step 3: Analyzing missing values...")
    missingness_analysis = analyze_missingness(data_dict)
    print("✓ Missingness analysis complete")
    print()
    
    # Generate report
    print("Step 4: Generating report...")
    report = generate_summary_report(data_dict, column_analysis, missingness_analysis)
    report_path = OUTPUT_DIR / 'ANALYSIS_REPORT.txt'
    with open(report_path, 'w') as f:
        f.write(report)
    print(f"✓ Saved: ANALYSIS_REPORT.txt")
    print()
    
    # Create visualizations
    print("Step 5: Creating visualizations...")
    create_samples_per_year_chart(data_dict)
    create_column_consistency_chart(data_dict)
    create_missingness_heatmap(data_dict, missingness_analysis)
    print()
    
    print("=" * 80)
    print("ANALYSIS COMPLETE!")
    print(f"Output directory: {OUTPUT_DIR}")
    print("=" * 80 + "\n")
    
    # Print report to console
    print(report)

if __name__ == '__main__':
    main()
