# NFL Play-by-Play Data: Descriptive Statistics Analysis

## Summary

Generated: November 17, 2025

### Datasets Overview
- **Total Files**: 27 parquet files (1999-2025)
- **Total Samples**: 1,258,814 rows
- **Years Covered**: 1999 - 2025 (complete coverage)
- **Sample Distribution**: Fairly uniform across years (~3.6-4.0% per year, 2025 is partial at 2.2%)

---

#### 1. Column Consistency
- **Common Columns**: 372 columns present across ALL years
- **Total Unique Columns**: 372 (no year-specific columns!)

#### 2. Samples Per Year
```
Highest:   2021-2024 (49,434 - 49,922 rows per year)
Lowest:    2025 (27,957 rows - partial season)
Average:   ~46,625 rows per year
```

#### 3. Missingness

**Most Complete Columns (0-1% missing)**:
- Core Game Information: `game_id`, `nfl_api_play_id`, `season`, `week`, `posteam`, `defteam`
- Timing Information: `time`, `game_seconds_remaining`, `half_seconds_remaining`, `quarter_seconds_remaining`
- Yard Line Info: `yrdln` (0.74%), `down` (15-16% only for non-plays)
- Win Probability: `wp`, `def_wp`, `vegas_wp` (0.58%)

**High Missing Columns** (play-type specific):
- Player-specific columns: 93-100% missing (only filled for relevant plays)
- Passing-only columns (air_yards, air_epa, cpoe, etc.): ~60-75% missing
- Rushing-only columns (rushing_yards, run_gap, run_location): ~70-78% missing
- Environmental data (wind, temp): 33-62% missing (weather data quality varies by year)
- Fantasy data (fantasy, fantasy_player_id): 28-32% missing

---

All 372 common columns are available across the entire 1999-2025 dataset:

**Sample Categories**:
- Game & Season Info (10 cols)
- Play Information (30 cols)  
- Offensive Plays (60 cols)
- Defensive Plays (50 cols)
- Scoring Events (15 cols)
- EPA/WPA Metrics (12 cols)
- Win Probability (8 cols)
- Player Info (120+ cols)
- Drive Tracking (25 cols)
- Outcome Indicators (32 cols)
