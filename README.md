# NFL-ML

<div align="center">
  <img src="images/nfl_ml.png" alt="NFL" width="300">
</div>

---

## Dataset example

- **Source**: NFL play-by-play 2024 season
- **Total Plays**: 49,492
- **Total Games**: 285
- **Columns**: 333
- **Format**: Parquet

## Variables

### Offensive Metrics
- **CP (Completion Probability)**: 0-1 scale
- **CPOE (Completion % Over Expected)**: -100 to +100
- **EPA (Expected Points Added)**: Play value metric
- **XYAC**: Expected yards after catch metrics

### Defensive Metrics
- Tackles and assist tackles
- Sacks and half-sacks
- Pass defense
- Interceptions and fumble recoveries

### Game Context
- Drive information and transitions
- Penalties and challenges
- Environmental conditions (weather, surface, roof)
- Betting lines and spreads

## Data Quality

- **100% Complete**: Game IDs, team info, play types
- **High Completeness (>90%)**: Player names, scoring events
- **Moderate (50-90%)**: Advanced metrics, player IDs
- **Lower (<10%)**: Defensive details, penalty info

---