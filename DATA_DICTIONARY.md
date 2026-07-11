# Data dictionary

All latency values are in **milliseconds (ms)**. Lower is better.

## Top-level fields (per daily run file, `YYYY-MM-DD.json`)

| Field | Meaning |
|---|---|
| `benchmark` | Benchmark id. `B1-exchange-rest-latency` for these files. |
| `script_version` | Version of the measurement script that produced the run. |
| `timestamp_utc` | ISO 8601 UTC time the run started. |
| `region` | Where the run executed. `us-east` is the fixed production server. A few early runs are labeled `github-actions-runner` (a different vantage point) and should not be trend-compared with `us-east` runs. |
| `method` | One-line description of how latency was measured. |
| `samples_per_venue` | Number of timed requests per venue. |
| `results` | Array of per-venue measurements (see below). |
| `us_blocked` | Venues probed for reachability only because they block US datacenters. Not timed, not ranked. |

## Per-venue fields (`results[]`)

| Field | Meaning |
|---|---|
| `venue` | Machine id of the exchange (e.g. `coinbase`). |
| `label` | Display name (e.g. `Coinbase`). |
| `host` | Hostname of the measured endpoint. |
| `path` | Public market-data path requested. |
| `us` | `yes` / `no`: whether the venue serves US retail customers (verified periodically; regulatory status shifts). |
| `samples_requested` | Timed requests attempted. |
| `samples_ok` | Timed requests that returned HTTP 200 with a body. |
| `errors` | Requests excluded from stats (non-200, timeout, or connection error). |
| `connect_ms` | One-time DNS + TCP + TLS handshake time (median of several handshake samples), reported separately from request latency. |
| `connect_ms_min` | Fastest of the handshake samples, for reference. |
| `connect_samples` | How many handshake samples the connect figures are based on. |
| `error_detail` | First error encountered, if any. |
| `stats_ms` | Latency percentiles over successful samples: `min`, `p50`, `p95`, `p99`, `max`, `mean`. |

## Reachability-only probes (`us_blocked[]`)

| Field | Meaning |
|---|---|
| `venue` / `label` / `host` | The probed venue. |
| `http_status` | Live HTTP status from a US datacenter (e.g. `451` or `403` for a geoblock), or `null` if the connection failed. |

## History time series (`history.json`)

| Field | Meaning |
|---|---|
| `benchmark` | Benchmark id. |
| `description` | Plain-language summary of the series. |
| `unit` | `milliseconds`. |
| `generated_utc` | When this history file was last rebuilt. |
| `history` | Array of daily records, one per UTC day. |

Each `history[]` record: `date`, `timestamp_utc`, `region`, and `venues` (a map of `venue -> { p50, p95, label, us }`).

---

# B2: Real cost to trade (`data/fees/` and `data/fees-sol/`)

All cost values are in **basis points (bps)**. 1 bps = 0.01%, so on a $10,000 order 1 bps = $1. Lower is better.

## Top-level fields (per daily run file, `YYYY-MM-DD.json`)

| Field | Meaning |
|---|---|
| `benchmark` | Benchmark id. `B2-cost-to-trade`. |
| `asset` | The asset traded in this file: `BTC` (in `data/fees/`) or `SOL` (in `data/fees-sol/`). |
| `script_version` | Version of the measurement script that produced the run. |
| `timestamp_utc` | ISO 8601 UTC time the run started. |
| `region` | Where the run executed. `us-east` is the fixed production server. |
| `method` | One-line description of how cost was measured. |
| `sizes_usd` | The order sizes (in USD) modeled, e.g. `[10000, 100000]`. |
| `results` | Array of per-venue measurements (see below). |

## Per-venue fields (`results[]`)

| Field | Meaning |
|---|---|
| `venue` / `label` / `host` | Machine id, display name, and measured endpoint host. |
| `best_bid` / `best_ask` / `mid` | Top-of-book bid, ask, and midpoint at measurement time. |
| `half_spread_bps` | Half the bid-ask spread in bps: the cost of crossing from mid to the ask. |
| `taker_fee_bps` | Published base-tier taker fee in bps for this venue. |
| `fee_as_of` | Date the taker fee was last verified. |
| `fee_source` | URL of the venue's public fee schedule. |
| `error_detail` | First error encountered, if any (else `null`). |
| `sizes` | Map of order size (USD) -> `{ slippage_bps, total_cost_bps }`. |

For each size: `slippage_bps` is the measured order-book slippage to fill that market buy, and `total_cost_bps` = `taker_fee_bps` + `half_spread_bps` + `slippage_bps` (the all-in one-way cost).

## History time series (`history.json`)

Top-level: `benchmark`, `asset`, `description`, `unit` (`basis_points`), `primary_size_usd`, `generated_utc`, and `history` (one record per UTC day). Each `history[]` record has `date`, `timestamp_utc`, `region`, and `venues` (a map of `venue -> { total_cost_bps, half_spread_bps, label }` at the primary size).
