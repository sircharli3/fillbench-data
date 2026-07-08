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
| `connect_ms` | One-time DNS + TCP + TLS handshake time, measured once, reported separately from request latency. |
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
