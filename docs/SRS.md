# SOFTWARE REQUIREMENTS SPECIFICATION (SRS)

**Project Designation:** AncientSloth CLI Logger V1
**System Type:** Quantitative Ledger & Swing Trading Framework
**Environment:** Python CLI (Local/Offline)
**Status:** LOCKED / BASELINE ESTABLISHED

---

## 1. System Objective

To construct a highly modular, asynchronous command-line logging and analytics framework tailored exclusively for systematic retail swing trading. The architecture must enforce absolute operational discipline, strictly isolate execution logic from mathematical calculation, and persist all execution and behavioral data to a centralized flat-file CSV ledger.

---

## 2. System Architecture & Directory Blueprint

The framework utilizes a unidirectional data flow and strict module isolation.

```text
$CLI_LOGGER_HOME/
├── core/
│   ├── __init__.py
│   ├── config.py             # Parses constraints.json, resolves CLI_LOGGER_HOME
│   ├── constraints.json      # Boolean discipline toggles (e.g., "no_news_trading")
│   ├── risk_engine.py        # Enforces 0.005 limit, sizing math, directional logic
│   └── storage_engine.py     # File locking, sanitization, CSV append/update I/O
├── analytics/
│   ├── __init__.py
│   ├── edge_calculator.py    # All-Time & T-100 win rate queries
│   ├── regime_finder.py      # MA/ATR computation mapping to boolean states
│   ├── discipline_audit.py   # Compliance score calculator based on BREACH flags
│   ├── optimization.py       # High-expectancy parameter mapping
│   └── trade_duration.py     # Computes median/mean hold times to TP/SL per setup_id
├── data/
│   ├── trading_log.csv       # Master append-only ledger
│   └── daily_analytics.csv   # Async background analytical output
├── docs/
|   └── SRS.md                # Documentation
├── execute_trade.py          # Main sync thread (Ingestion)
└── update_trade.py           # Sync thread (Trade closure and excursion/friction logging)

```

---

## 3. Functional Requirements (FR)

* **FR-01: Hybrid Data Ingestion:** `execute_trade.py` must support sequential interactive prompts (via `Rich`/`Questionary` libraries) with real-time regex validation (`^\d+(\.\d+)?$`), and single-line command arguments (via `argparse`) for rapid execution.
* **FR-02: Active State Management:** `update_trade.py` must dynamically query `trading_log.csv` for rows where `status == 'OPEN'`, rendering them in a terminal table. It must ingest closing parameters (`exit_timestamp`, `exit_trigger`, `MAE`, `MFE`, `trade_friction_log`) via UUID4 or index selection.
* **FR-03: Asynchronous Analytics Subprocess:** Upon successful completion of Thread 0 (Input/Append), the system must spawn Thread 1 (via `asyncio`). This background thread recalculates metrics across the `analytics/` pipeline and updates `data/daily_analytics.csv` without blocking terminal operation.
* **FR-04: Dual-Horizon Probability Query:** Prior to execution confirmation, the system must query historical data to output the All-Time and T-100 (most recent 100 occurrences) win rates for the inputted `setup_id`.
* **FR-05: Computational Regime Tagging:** `regime_finder.py` must programmatically ingest price-action logic to output a string-based regime tag (e.g., `BULL_VOLATILE`). Manual subjective tagging is strictly prohibited.
* **FR-06: Temporal Setup Analytics:** `trade_duration.py` must partition historical data by `setup_id` and compute the time delta (`exit_timestamp - entry_timestamp`). It must isolate and return the mathematical mean and median durations for winning trades (`exit_trigger == 'TP'`) and losing trades (`exit_trigger == 'SL'`).

---

## 4. Non-Functional Requirements (NFR)

* **NFR-01: Strict Offline Isolation:** Version 1.0 contains zero API dependencies. It must function flawlessly in an air-gapped or disconnected environment.
* **NFR-02: Global Environment Pathing:** All internal directory references must resolve via the `$CLI_LOGGER_HOME` environment variable, ensuring operability regardless of the active terminal directory.
* **NFR-03: Temporal Indexing:** Batch execution windows must auto-generate a `YYYYMMDD_Session` format for `session_id`.
* **NFR-04: Data Sanitization (Free-Text):** The `storage_engine.py` must sanitize the `trade_friction_log` by stripping internal carriage returns and wrapping the payload in double quotes to prevent CSV delimiter corruption.
* **NFR-05: File State Locking:** The system must implement cross-platform file locking (e.g., `portalocker`) during read/write operations to prevent race conditions between the CLI ingestion thread and the background analytics thread.

---

## 5. Data Schema (`trading_log.csv`)

| Column Header | Data Type | Origin / Validation Rule |
| --- | --- | --- |
| `trade_id` | `UUID4` | System generated. Primary Key. |
| `session_id` | `str` | System generated. `YYYYMMDD_Session`. |
| `asset_traded` | `str` | User input (`execute_trade.py`). Regex verified. |
| `direction` | `str` | User input. Enum: `LONG`, `SHORT`. |
| `setup_id` | `str` | User input. Alphanumeric identifier. |
| `regime_tag` | `str` | System generated (`regime_finder.py`). |
| `status` | `str` | Enum: `OPEN`, `CLOSED`, `DISCIPLINE_BREACH`, `CLOSED_WITH_BREACH`. |
| `entry_timestamp` | `datetime` | System generated. ISO 8601. |
| `exit_timestamp` | `datetime` | User input (`update_trade.py`). ISO 8601. Nullable. |
| `account_balance` | `float` | User input. Must be $> 0.0$. |
| `risk_parameter` | `float` | Hardcoded constant $\le 0.005$. |
| `entry_price` | `float` | User input. Must be $> 0.0$. |
| `SL_price` | `float` | User input. Subject to directional bounds. |
| `TP_price` | `float` | User input. Subject to directional bounds. |
| `position_size` | `float` | System generated (`risk_engine.py`). |
| `risk_reward` | `float` | System generated. $\vert{}TP - Entry\vert{} / \vert{}Entry - SL\vert{}$. |
| `MAE` | `float` | User input (`update_trade.py`). Nullable. |
| `MFE` | `float` | User input (`update_trade.py`). Nullable. |
| `exit_trigger` | `str` | User input (`update_trade.py`). Enum: `SL`, `TP`, `MANUAL`. Nullable. |
| `trade_friction_log` | `str` | User input (`update_trade.py`). Sanitized string. Nullable. |

---

## 6. Business Logic & Constraints (CR)

* **CR-01: The Biological Risk Law:**
* Maximum allowable risk is `0.005` (0.5% of account balance). This variable cannot be dynamically altered by user input during the normal trade flow.


* **CR-02: Modular Discipline Dictionary:**
* Operational parameters (e.g., restricted trading windows) are defined in `core/constraints.json`. These rules act as binary filters before execution validation.


* **CR-03: Fatal Logic Protocol (Hard Exit):**
* Directional mismatch guarantees immediate script termination (`sys.exit(1)`).
* LONG condition: `SL_price < entry_price` AND `TP_price > entry_price`.
* SHORT condition: `SL_price > entry_price` AND `TP_price < entry_price`.


* **CR-04: Discipline Breach Protocol (Override):**
* If user input violates a non-fatal constraint (e.g., manually forcing risk $> 0.005$ or trading during a restricted JSON window), the system intercepts and blocks execution.
* The user may issue a bypass command.
* Upon bypass, execution proceeds, but the trade is permanently written with `status = 'DISCIPLINE_BREACH'` (or `CLOSED_WITH_BREACH` upon exit).
* `analytics/discipline_audit.py` consumes this flag to permanently degrade the system compliance score.



---
