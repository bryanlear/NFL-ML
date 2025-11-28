import pandas as pd
import os

# List of parquet files
parquet_files = [
    'raw_data/play_by_play_2021.parquet',
    'raw_data/play_by_play_2022.parquet',
    'raw_data/play_by_play_2023.parquet',
    'raw_data/play_by_play_2024.parquet',
    'raw_data/play_by_play_2025.parquet'
]

# Columns to drop
columns_to_drop = [
    'kicker_player_id',
    'kicker_player_name',
    'return_team'
]

# Add all columns that start with 'solo_tackle_'
for file in parquet_files:
    if os.path.exists(file):
        print(f"\nProcessing {file}...")
        
        # Read the parquet file
        df = pd.read_parquet(file)
        print(f"Original shape: {df.shape}")
        
        # Find all columns that start with 'solo_tackle_'
        solo_tackle_cols = [col for col in df.columns if col.startswith('solo_tackle_')]
        
        # Combine all columns to drop
        all_cols_to_drop = columns_to_drop + solo_tackle_cols
        
        # Filter to only columns that actually exist in the dataframe
        existing_cols_to_drop = [col for col in all_cols_to_drop if col in df.columns]
        
        if existing_cols_to_drop:
            print(f"Dropping columns: {existing_cols_to_drop}")
            df = df.drop(columns=existing_cols_to_drop)
            print(f"New shape: {df.shape}")
            
            # Save back to parquet
            df.to_parquet(file, index=False)
            print(f"✓ Saved {file}")
        else:
            print(f"No matching columns found to drop in {file}")
    else:
        print(f"File not found: {file}")

print("\n✓ All files processed!")
