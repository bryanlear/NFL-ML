# NFL Play-by-Play 2024 Dataset Analysis Report

**Generated:** November 17, 2025  
**Data Source:** `raw_data/play_by_play_2024.parquet`  
**Dataset Size:** 49,492 rows × 333 columns

---

 The dataset contains 49,492 individual plays from 285 unique games across the 2024 NFL season. Each play record includes detailed information about offensive and defensive actions, player involvement, penalties, turnovers, and advanced statistical metrics such as Expected Points Added (EPA) and completion probability over expected (CPOE).

---

## Table of Contents

1. [Dataset Overview](#dataset-overview)
2. [Core Game Information](#core-game-information)
3. [Teams & Coaching](#teams--coaching)
4. [Scoring & Betting](#scoring--betting)
5. [Field & Environmental Conditions](#field--environmental-conditions)
6. [Drive Information](#drive-information)
7. [Play Classification & Sequencing](#play-classification--sequencing)
8. [Passing Plays](#passing-plays)
9. [Rushing Plays](#rushing-plays)
10. [Defensive Plays](#defensive-plays)
11. [Turnovers & Special Plays](#turnovers--special-plays)
12. [Penalties](#penalties)
13. [Advanced Analytics](#advanced-analytics)
14. [Data Quality Notes](#data-quality-notes)

---

## Dataset Overview

### Basic Statistics
- **Total Plays:** 49,492
- **Total Games:** 285
- **Average Plays per Game:** ~173.6
- **Columns:** 333
- **Time Period:** 2024 NFL Season

### Data Completeness
The dataset has strong completeness for core fields:
- Core play fields (game_id, play_id): 100% populated
- Player identification fields: 74-76% populated (varies by play type)
- Advanced metrics (EPA, CP): 35-74% populated

---

## Core Game Information

| Field | Type | Description | Completeness |
|-------|------|-------------|--------------|
| `game_id` | string | Unique game identifier | 100% |
| `play_id` | float | Unique play identifier within game | 100% |
| `old_game_id` | string | Legacy game ID format for compatibility | 100% |
| `nfl_api_id` | string | NFL's internal API game identifier (UUID format) | 100% |
| `season` | int32 | Season year (all values: 2024) | 100% |
| `start_time` | string | Game start time (format: MM/DD/YY, HH:MM:SS) | 100% |
| `time_of_day` | string | ISO 8601 timestamp for each play | 97.1% |
| `end_clock_time` | string | ISO 8601 timestamp when play ended | 84.2% |
| `stadium` | string | Game location name | 100% |
| `stadium_id` | string | 3-letter team code + 00 format | 100% |
| `game_stadium` | string | Alternative stadium name | 100% |

**Key Insights:**
- 271 unique start times indicate regular scheduling patterns
- Stadium coverage is complete for all plays
- Time-of-day data available for 97.1% of plays

---

## Teams & Coaching

| Field | Type | Description | Completeness |
|-------|------|-------------|--------------|
| `home_team` | string | Home team abbreviation (3-letter code) | 100% |
| `away_team` | string | Away team abbreviation (3-letter code) | 100% |
| `home_coach` | string | Head coach name of home team | 100% |
| `away_coach` | string | Head coach name of away team | 100% |
| `location` | string | Game location type: Home or Neutral | 100% |
| `div_game` | int32 | Binary flag (0/1): Is divisional matchup | 100% |

**Key Insights:**
- All 32 NFL teams represented in coaching data
- Divisional games clearly marked for conference analysis
- Single neutral site game identified

---

## Scoring & Betting

| Field | Type | Min | Max | Mean | Description |
|-------|------|-----|-----|------|-------------|
| `away_score` | int32 | 0 | 51 | - | Away team score at play time |
| `home_score` | int32 | 0 | 54 | - | Home team score at play time |
| `result` | int32 | -48 | 51 | - | Score differential (home - away) |
| `total` | int32 | 6 | 96 | - | Combined score (home + away) |
| `spread_line` | float64 | -16.5 | 19.5 | 1.57 | Betting spread (home team perspective) |
| `total_line` | float64 | 32.5 | 56.5 | 44.50 | Over/under betting line |

**Key Insights:**
- Highest scoring game: 96 combined points
- Lowest scoring game: 6 combined points
- Average total: 44.5 points (close to betting lines)
- Spread range indicates competitive and non-competitive games
- 42-43 unique score values per team throughout season

---

## Field & Environmental Conditions

### Stadium & Surface Information

| Field | Type | Distribution | Description |
|-------|------|--------------|-------------|
| `roof` | string | Outdoors (majority), Dome, Closed | Stadium roof type |
| `surface` | string | 7 types | Field surface composition |
| `weather` | string | 260 unique descriptions | Detailed weather conditions |
| `temp` | float64 | 14°F - 93°F | Temperature (63.6% populated) |
| `wind` | float64 | 0 - 20 mph | Wind speed (63.6% populated) |

**Roof Type Breakdown:**
- **Outdoors:** Primary (most games)
- **Dome:** Climate-controlled environments
- **Closed:** Retractable/convertible roofs

**Surface Types:**
1. Grass
2. FieldTurf
3. Astroturf
4. A-Turf
5. Matrix Turf
6. Sport Turf
7. Empty/Unknown

**Weather Coverage:**
- 260 unique weather descriptions captured
- Temperature data available for 63.6% of plays (indoor games often missing)
- Wind data available for 63.6% of plays
- Examples: "Clouds and sun with wind Temp: 61° F, Humidity: 55%, Wind: W 20 mph"

**Key Insights:**
- Temperature ranges from 14°F (cold weather games) to 93°F (dome/warm weather)
- Wind speeds up to 20 mph documented
- Surface type important for injury and traction analysis

---

## Drive Information

### Drive Tracking Overview

Drives track offensive possessions from start to end. Key metrics include:

| Field | Type | Min | Max | Mean | Description |
|-------|------|-----|-----|------|-------------|
| `fixed_drive` | float64 | 1 | 31 | 11.24 | Drive number sequence |
| `drive_play_count` | float64 | 0 | 21 | 7.63 | Total plays in drive |
| `drive_first_downs` | float64 | 0 | 9 | 2.59 | First downs achieved |
| `drive_inside20` | float64 | 0/1 | - | 0.44 | Drive reached opponent 20-yard line |
| `drive_ended_with_score` | float64 | 0/1 | - | 0.52 | Drive resulted in points |
| `drive_yards_penalized` | float64 | -45 | 61 | -0.26 | Net penalty yards |
| `drive_quarter_start` | float64 | 1 | 5 | 2.52 | Quarter where drive began |
| `drive_quarter_end` | float64 | 1 | 5 | 2.65 | Quarter where drive ended |

**Completeness:** 98.9% of plays have drive data

### Drive Transitions

**Start Transitions** (how teams gained possession):
- KICKOFF
- PUNT
- FUMBLE
- INTERCEPTION
- MISSED_FG
- BLOCKED_FG
- BLOCKED_PUNT
- MUFFED_KICKOFF
- MUFFED_PUNT
- ONSIDE_KICK
- BLOCKED_FG,_DOWNS
- BLOCKED_PUNT,_DOWNS

**End Transitions** (how drives concluded):
- TOUCHDOWN
- FIELD_GOAL
- PUNT
- FUMBLE
- INTERCEPTION
- DOWNS (turnover on downs)
- MISSED_FG
- BLOCKED_FG
- BLOCKED_PUNT
- SAFETY
- FUMBLE,_SAFETY
- END_HALF
- END_GAME

### Drive Timing

| Field | Description | Example Values |
|-------|-------------|-----------------|
| `drive_real_start_time` | ISO 8601 timestamp of drive start | 2024-09-08T17:03:02.957Z |
| `drive_time_of_possession` | Clock time consumed (MM:SS format) | 7:13 |
| `drive_game_clock_start` | Game clock at drive start | 15:00 |
| `drive_game_clock_end` | Game clock at drive end | 07:47 |
| `drive_play_id_started` | First play ID of drive | 38 - 5,144 |
| `drive_play_id_ended` | Last play ID of drive | 39 - 5,220 |

### Drive Field Position

| Field | Format | Description |
|-------|--------|-------------|
| `drive_start_yard_line` | "TEAM ##" | e.g., "ARI 30" |
| `drive_end_yard_line` | "TEAM ##" | e.g., "BUF 5" |

**Key Insights:**
- Average 7.63 plays per drive
- 52% of drives result in scoring (TD or FG)
- 44% of drives reach opponent's 20-yard line (scoring position)
- Average 2.59 first downs per drive
- Drives span 1-5 quarters (overtime drives tracked)

---

## Play Classification & Sequencing

### Play Type Classification

| Field | Type | Distribution | Description |
|-------|------|--------------|-------------|
| `play_type_nfl` | string | 17 types | NFL's official play type classification |
| `play_type` | string | Simplified | Broader play category |
| `play_deleted` | float64 | All 0 | No deleted plays in dataset |
| `aborted_play` | float64 | All 0 | No aborted plays in dataset |

**Play Type (NFL) Values:**
- GAME_START
- KICK_OFF
- RUSH
- PASS
- FIELD_GOAL (all FG attempts)
- PUNT
- EXTRA_POINT
- TWO_MINUTE_WARNING
- TIMEOUT
- CHALLENGE
- REFEREE_TIMEOUT
- END_GAME
- END_HALF
- FUMBLE
- INTERCEPTION

### Play Sequencing

| Field | Type | Min | Max | Mean | Description |
|-------|------|-----|-----|------|-------------|
| `order_sequence` | float64 | 1 | 5,246 | 2,193.62 | Chronological play order |
| `series` | float64 | 1 | 71 | 28.66 | Drive series within game |
| `play_id` | float64 | Varies | - | - | Play identifier |

### Play Categorization

| Field | Type | Values | Description |
|-------|------|--------|-------------|
| `pass` | float64 | 0/1 | Is pass play (45% of plays) |
| `rush` | float64 | 0/1 | Is rush play (29% of plays) |
| `special` | float64 | 0/1 | Special teams (15% of plays) |
| `play` | float64 | 0/1 | Is regular play (76% of plays) |
| `special_teams_play` | float64 | 0/1 | ST flag - 13% of plays |
| `st_play_type` | string | Empty | ST subtype (not populated) |

### Series Information

| Field | Type | Description |
|-------|------|-------------|
| `series_success` | float64 | Did series gain first down (59% success) |
| `series_result` | string | Outcome of series |

**Series Results:**
- First down (continued drive)
- Touchdown
- Field goal
- Missed field goal
- Punt
- Safety
- Turnover
- Turnover on downs
- Opp touchdown (defensive score)
- QB kneel
- End of half

**Key Insights:**
- 59% series success rate (first down gain)
- 45% pass plays, 29% rush plays, 15% special teams
- 76% are regular plays (vs. admin plays)
- Max 71 series in a single game

---

## Passing Plays

### Passer Information

| Field | Type | Unique Values | Completeness | Description |
|-------|------|---------------|--------------|-------------|
| `passer` | string | 112 | 45.3% | QB name (only pass plays) |
| `passer_id` | string | 113 | 45.3% | QB NFL ID |
| `passer_jersey_number` | float64 | 25 | 45.3% | QB jersey (1-84 range) |

### Receiver Information

| Field | Type | Unique Values | Completeness | Description |
|-------|------|---------------|--------------|-------------|
| `receiver` | string | 485 | 38.2% | Target player name |
| `receiver_id` | string | 497 | 38.2% | Target player NFL ID |
| `receiver_jersey_number` | float64 | 66 | 38.4% | Receiver jersey number |

### Pass Characteristics

| Field | Type | Values | Description |
|-------|------|--------|-------------|
| `pass_length` | string | short / deep / screen | Distance category of pass |
| `pass_location` | string | left / middle / right | Horizontal throw location |
| `air_yards` | float64 | -15 to 65+ | Yards traveled by ball in air |
| `yards_after_catch` | float64 | -15 to 80+ | Yards gained after reception |
| `yards_gained` | float64 | Variable | Total yards on play |
| `yards_net_of_penalty` | float64 | Variable | Yards after penalties applied |

### Completion Metrics

| Field | Type | Min | Max | Mean | Description |
|-------|------|-----|-----|------|-------------|
| `cp` | float64 | 0.15 | 0.92 | 0.67 | Completion Probability |
| `cpoe` | float64 | -92.34 | 80.11 | 0.98 | Completion % Over Expected |
| `qb_epa` | float64 | -12.69 | 8.54 | 0.02 | Expected Points Added by QB (98.8% populated) |

**Completion Probability (CP):**
- Ranges 0-1, represents likelihood of completion
- Based on pass depth, location, and situation

**CPOE (Completion % Over Expected):**
- Measures QB performance vs. model expectations
- Positive values = QB outperforming model
- Negative values = QB underperforming model
- Range: -92.34 (significant underperformance) to +80.11 (significant outperformance)

**Key Insights:**
- 112 unique QBs threw passes
- Average CP of 0.67 indicates moderate to good catchability
- CPOE averaging 0.98 suggests realistic model calibration
- QB EPA ranges from -12.69 (poor play) to +8.54 (excellent play)

---

## Rushing Plays

### Rusher Information

| Field | Type | Unique Values | Completeness | Description |
|-------|------|---------------|--------------|-------------|
| `rusher` | string | 334 | 29.8% | RB/runner name |
| `rusher_id` | string | 343 | 29.8% | Runner NFL ID |
| `rusher_jersey_number` | float64 | 70 | 31.3% | Jersey number (0-89 range) |

**Key Insights:**
- 334 unique rushers tracked
- Wide range of jersey numbers (0-89)
- 29.8% of plays are rushing attempts
- 31.3% completeness for jersey numbers suggests some QBs also run

---

## Defensive Plays

### Tackle Information

Tackles tracked in hierarchy: primary tackle, then up to 4 assists.

| Field | Type | Unique Values | Completeness | Description |
|-------|------|---------------|--------------|-------------|
| `tackle_player_id` | string | 783 | 18.6% | Primary tackler ID |
| `tackle_player_name` | string | 755 | 18.6% | Primary tackler name |
| `tackle_team` | string | 32 | 18.6% | Defending team |
| `tackle_with_assist` | float64 | 0/1 | 96.9% | Was tackle assisted? |

**Assist Tackle Levels (1-4):**
- `assist_tackle_1_*`: 5.2% of plays (2,572)
- `assist_tackle_2_*`: 0.2% of plays (89)
- `assist_tackle_3_*`: 0.006% of plays (3)
- `assist_tackle_4_*`: 0.006% of plays (3)

Each level includes:
- `*_player_id`: Player NFL ID
- `*_player_name`: Player name
- `*_team`: Team abbreviation

### Pass Defense

| Field | Type | Unique Values | Completeness | Description |
|-------|------|---------------|--------------|-------------|
| `pass_defense_1_player_id` | string | 582 | 4.6% | Primary pass defender |
| `pass_defense_1_player_name` | string | 560 | 4.6% | Pass defender name |
| `pass_defense_2_player_id` | string | 80 | 0.2% | Secondary pass defender (rare) |
| `pass_defense_2_player_name` | string | 80 | 0.2% | Secondary pass defender |

### Sacks

| Field | Type | Unique Values | Completeness | Description |
|-------|------|---------------|--------------|-------------|
| `sack_player_id` | string | 410 | 2.5% | Sack maker ID (1,238 plays) |
| `sack_player_name` | string | 402 | 2.5% | Sack maker name |
| `half_sack_1_player_id` | string | 122 | 0.3% | First half-sack player (144 plays) |
| `half_sack_1_player_name` | string | 121 | 0.3% | First half-sack name |
| `half_sack_2_player_id` | string | 121 | 0.3% | Second half-sack player (144 plays) |
| `half_sack_2_player_name` | string | 122 | 0.3% | Second half-sack name |

**Key Insights:**
- 1,238 sack plays (2.5% of total)
- 410 unique sack makers
- 144 shared sacks (2 defenders credited with 0.5 sack each)

### Safeties

| Field | Type | Unique Values | Completeness | Description |
|-------|------|---------------|--------------|-------------|
| `safety_player_id` | string | 11 | 0.02% | Safety scorer ID |
| `safety_player_name` | string | 11 | 0.02% | Safety scorer name |

**Safety Scorers (11 total plays):**
- Z.Allen
- A.Wright
- B.Young
- D.Jones
- D.Phillips
- H.Landry
- K.Lassiter
- N.Gallimore
- S.Hubbard
- A.Epenesa
- Z.Harrison

### Returns

| Field | Type | Min | Max | Mean | Description |
|-------|------|-----|-----|------|-------------|
| `return_team` | string | 32 teams | 10.9% | Team returning kick/punt |
| `return_yards` | float64 | -5 | 103 | 0.84 | Return yardage |

**Key Insights:**
- 10.9% of plays involve returns (5,397 plays)
- Maximum return: 103 yards (likely kickoff return for TD)
- Minimum return: -5 yards (negative yardage possible)

### Defensive Two-Point Plays

| Field | Type | Values | Description |
|-------|------|--------|-------------|
| `defensive_two_point_attempt` | float64 | 0/1 | Is 2-pt conversion defense |
| `defensive_two_point_conv` | float64 | 0/1 | Did defense score 2 points |
| `defensive_extra_point_attempt` | float64 | 0/1 | Is extra point defense attempt |
| `defensive_extra_point_conv` | float64 | 0/1 | Did defense score on XP |

**Key Insights:**
- Defensive 2-point conversions are rare
- Defensive extra points: 0 in dataset (all zeros)

---

## Turnovers & Special Plays

### Interceptions & Fumbles

| Field | Type | Description |
|-------|------|-------------|
| `interception` | float64 | Was pass intercepted (binary) |
| `fumble` | float64 | Was fumble recorded (binary) |
| `touchdown` | float64 | Was touchdown scored (binary) |

### Fumble Details

**Primary Fumbler** (1.3% of plays, 663 fumbles):
- `fumbled_1_team`: Team that fumbled
- `fumbled_1_player_id`: Fumbler ID
- `fumbled_1_player_name`: Fumbler name

**Secondary Fumbler** (extremely rare, 4 total):
- `fumbled_2_*`: Same fields for second fumbler

**Notable Fumbles:**
- Most fumbles by single team in season: 663 tracked
- Distribution across 271 unique fumbling players

### Fumble Recovery Details

**Primary Recovery** (1.2% of plays, 608 recoveries):
- `fumble_recovery_1_team`: Team that recovered
- `fumble_recovery_1_yards`: Recovery yardage (-7 to +102)
- `fumble_recovery_1_player_id`: Recover ID
- `fumble_recovery_1_player_name`: Recovery name

**Secondary Recovery** (extremely rare, 3 total):
- `fumble_recovery_2_*`: Same fields for second recovery

**Key Insights:**
- 608 fumble recoveries in season
- Recovery yards range -7 to +102
- Average recovery gain: 2.12 yards
- Multiple recoveries on same play extremely rare (3 plays)

---

## Penalties

### Penalty Occurrence

| Field | Type | Completeness | Description |
|-------|------|--------------|-------------|
| `penalty` | float64 | 100% | Was penalty called (0/1) |
| `penalty_yards` | float64 | 7.4% | Yards of penalty |
| `penalty_type` | string | 7.3% | Type of penalty called |

**Penalty Statistics:**
- 3,642 plays with penalties (7.4% of total)
- 3,335 have identified penalty players (6.7%)

### Penalty Details

| Field | Type | Unique Values | Description |
|-------|------|---------------|-------------|
| `penalty_team` | string | 32 teams | Team committing penalty |
| `penalty_player_id` | string | 1,243 | Player ID of offender |
| `penalty_player_name` | string | 1,174 | Player name of offender |

### Penalty Yards

| Min | Max | Mean |
|-----|-----|------|
| 0 | 48 | 8.09 |

**Common Penalty Yardages:**
- 5 yards: Minor infractions
- 10 yards: Standard penalties
- 15 yards: Significant infractions

### Penalty Types

50 unique penalty types recorded, including:

**Common Penalties:**
- Unnecessary Roughness
- Defensive Pass Interference
- Face Mask
- Illegal Block
- Holding
- Offensive Pass Interference
- Off-sides
- Encroachment
- False Start
- Roughing the Passer
- Illegal Motion
- Illegal Shift
- Ineligible Downfield
- Intentional Grounding
- Unnecessary Roughness on Kicker
- Delay of Game
- Neutral Zone Infraction
- Illegal Use of Hands
- Hands to Face / Facemask
- Clipping
- Unsportsmanlike Conduct
- Taunting

**Key Insights:**
- 7.4% of plays result in penalty
- 1,243 unique offending players
- 50 different penalty types
- Average penalty: 8.09 yards

---

## Advanced Analytics

### Expected Points Added (EPA)

| Field | Type | Min | Max | Mean | Completeness |
|-------|------|-----|-----|------|--------------|
| `qb_epa` | float64 | -12.69 | 8.54 | 0.02 | 98.8% |
| `epa` | float64 | Variable | Variable | Variable | 98.8% |

**EPA Concept:**
- Measures change in expected points from play start to end
- Positive EPA = offensive gain in expected points
- Negative EPA = offensive loss in expected points
- Range spans from significant losses to significant gains

### Expected Yards After Catch (XYAC)

Available for ~33.4% of plays (16,511):

| Field | Type | Min | Max | Mean |
|-------|------|-----|-----|------|
| `xyac_epa` | float64 | -1.56 | 9.59 | 0.73 |
| `xyac_mean_yardage` | float64 | 0.50 | 23.95 | 5.54 |
| `xyac_median_yardage` | float64 | 0 | 36 | 3.72 |
| `xyac_success` | float64 | 0.027 | 1.0 | 0.77 |
| `xyac_fd` | float64 | 0.004 | 1.0 | 0.57 |

**XYAC Metrics:**
- `xyac_epa`: EPA generated after catch
- `xyac_mean_yardage`: Expected average yards after catch
- `xyac_median_yardage`: Expected median yards after catch
- `xyac_success`: Probability of gaining first down via YAC
- `xyac_fd`: First down probability from YAC

**Key Insights:**
- Average expected YAC: 5.54 yards (mean), 3.72 yards (median)
- 77% success rate on YAC plays (gaining positive yards)
- 57% first down conversion probability via YAC

### Expected Pass Rate (xPass)

| Field | Type | Min | Max | Mean | Completeness |
|-------|------|-----|-----|------|--------------|
| `xpass` | float64 | 0.018 | 0.998 | 0.63 | 76.1% |
| `pass_oe` | float64 | -99.44 | 97.79 | -1.75 | 73.9% |

**xPass Metrics:**
- `xpass`: Probability of pass play call (0-1 scale)
- `pass_oe`: Pass play % over expected (-100 to +100)
  - Positive = more passing than expected
  - Negative = less passing than expected

**Key Insights:**
- Average pass probability: 0.63 (63% chance to pass)
- Average teams pass 1.75% less than expected (conservative)

### Game-State Indicators

| Field | Type | Description |
|-------|------|-------------|
| `home_opening_kickoff` | float64 | Did home team receive opening kickoff (51% true) |
| `first_down` | float64 | Did play result in first down (23% success, 96.9% complete) |
| `success` | float64 | Play success metric (45% success, 98.8% complete) |
| `out_of_bounds` | float64 | Was play out of bounds (8% of plays) |

---

## Replays & Challenges

| Field | Type | Values | Completeness | Description |
|-------|------|--------|--------------|-------------|
| `replay_or_challenge` | float64 | 0/1 | 100% | Was play reviewed/challenged |
| `replay_or_challenge_result` | string | reversed, upheld | 0.7% | Challenge outcome |

**Key Insights:**
- 346 plays reviewed/challenged (0.7% of total)
- ~50/50 split between reversals and upheld calls

---

## Player Identification

### Generic Player Fields

These fields capture the primary player involved in a play (can be offensive or defensive depending on context):

| Field | Type | Unique Values | Completeness | Description |
|-------|------|---------------|--------------|-------------|
| `name` | string | 356 | 75.1% | Primary player name |
| `id` | string | 367 | 75.1% | Primary player NFL ID |
| `jersey_number` | float64 | 71 | 74.2% | Primary player jersey |

**Note:** These fields capture the "key player" for each play type.

### Fantasy Player Identification

| Field | Type | Unique Values | Completeness | Description |
|-------|------|---------------|--------------|-------------|
| `fantasy_player_name` | string | 575 | 67.3% | Fantasy league player name |
| `fantasy_player_id` | string | 593 | 67.3% | Fantasy player ID |
| `fantasy` | string | 588 | 70.4% | Alternative fantasy name |
| `fantasy_id` | string | 606 | 70.4% | Alternative fantasy ID |

**Key Insights:**
- 575 unique fantasy player names
- Slight variance between fantasy_player_* and fantasy_* fields
- 67-70% coverage indicates fantasy data available for scoring plays

---

## Data Quality Notes

### Completeness Summary

**100% Complete Fields:**
- Core identifiers (game_id, play_id, season)
- Team information
- Scoring data
- Play type classifications
- Drive information (98.9%)

**High Completeness (>90%):**
- Player names/IDs: 74-76%
- Scoring events: 96.9%
- Basic play attributes: 96-100%

**Moderate Completeness (50-90%):**
- Advanced metrics (EPA, CP, CPOE): 35-98.8%
- Passing plays: 38-45%
- Rushing plays: 29-31%

**Low Completeness (<10%):**
- Defensive plays (tackles, sacks): 2.5-18.6%
- Penalties: 7.4%
- Safeties: 0.02%

### Data Quality Issues

1. **Empty Columns:**
   - `st_play_type`: Completely empty (0 values)
   - `end_yard_line`: Empty (0 values)
   - `tackle_with_assist_2_*`: Empty (0 values)
   - `play_clock`: All zeros (no data)

2. **Sparse Data:**
   - Defensive statistics relatively sparse (depends on play type)
   - Environmental data (temp, wind) missing for domed stadiums
   - Secondary recovery data extremely rare (3 instances)

3. **Data Consistency:**
   - All 49,492 rows appear to be valid plays
   - No deleted or aborted plays
   - Replay/challenge data properly coded

### Field Surface Notes

Empty string values in `surface` field appear to represent missing data, not specific surface type. Likely corresponds to:
- Virtual games (none)
- Data collection gaps (rare)

---

## Statistical Summary

### Overall Dataset Metrics

| Metric | Value |
|--------|-------|
| Total Plays | 49,492 |
| Unique Games | 285 |
| Avg Plays/Game | 173.6 |
| Pass Plays | 22,427 (45.3%) |
| Rush Plays | 14,732 (29.8%) |
| Special Teams | 7,448 (15.0%) |
| Offensive Plays | 36,159 (73.1%) |
| Defensive/Admin Plays | 13,333 (26.9%) |
| Drive Count | ~4,700 |
| Average Drive Length | 7.63 plays |
| Drive Success Rate | 59% (first down) |
| Penalty Rate | 7.4% |

### Scoring Distribution

| Metric | Value |
|--------|-------|
| Total Games | 285 |
| Highest Score | 96 combined |
| Lowest Score | 6 combined |
| Avg Score | 44.5 combined |
| Touchdowns Scored | 2,445+ |
| Field Goals Scored | 1,100+ |
| Safeties | 11 |
| Safety Scorers | 11 unique players |

### Player Coverage

| Category | Unique Players |
|----------|-----------------|
| Quarterbacks | 112 |
| Rushers | 334 |
| Receivers | 485 |
| Tacklers | 783 |
| Pass Defenders | 582 |
| Sack Makers | 410 |
| Penalty Offenders | 1,243 |
| Overall Players | 1,500+ |

---

## Recommendations for Analysis

### Suggested Use Cases

1. **Advanced Statistical Analysis:**
   - EPA-based analysis for play value
   - CPOE for QB evaluation
   - Expected points modeling

2. **Team Performance:**
   - Drive efficiency metrics
   - Penalty analysis by team
   - Turnover analysis

3. **Player Performance:**
   - Individual player EPA/yards generated
   - Sack/tackle leader boards
   - Penalty leaders/least penalized

4. **Game Theory:**
   - Play calling analysis (xPass, gap between expected/actual)
   - Situational football metrics
   - Drive efficiency in different situations

5. **Environmental Impact:**
   - Weather effect on passing accuracy (where temp/wind data available)
   - Surface type impact on turnovers
   - Roof type correlation with scoring

### Data Cleaning Recommendations

1. Remove or flag plays from `st_play_type` (all empty)
2. Handle missing temperature/wind data (domed stadiums)
3. Consider surface type consistency (empty values)
4. Flag games with minimal environmental data

---

## Conclusion

The 2024 NFL play-by-play dataset is comprehensive and well-structured, containing 49,492 plays across 285 games. It provides rich detail on both offensive and defensive plays, with extensive advanced metrics (EPA, CPOE, xPass) and player identification. 

The dataset is particularly strong for:
- Offensive play analysis (passing yards, receivers, play efficiency)
- Game-level analysis (drives, scoring, team statistics)
- Advanced metrics and modeling

The dataset is more sparse for:
- Detailed defensive statistics
- Injury/player safety metrics
- Rare events (safeties, multiple fumble recoveries)

With proper handling of missing data and understanding of field completeness percentages, this dataset enables sophisticated NFL analytics across multiple dimensions including team strategy, player performance, and game outcomes.

---

**End of Report**

Generated: November 17, 2025  
Data Source: raw_data/play_by_play_2024.parquet  
Total Dataset Size: 49,492 rows × 333 columns
