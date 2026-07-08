# FillBench Data

Open, reproducible benchmark data for crypto trading tools and exchange APIs.

**Live site and full context: [fillbench.com](https://fillbench.com)**

This repository is the public data mirror for [FillBench](https://fillbench.com). The website is the real-time source of truth (refreshed every 2 hours, with charts, methodology, and analysis); this repo publishes the same raw data in a stable, downloadable, machine-readable form so it can be cited, diffed, and reused.

## What is in here

### B1: Exchange REST API latency

Steady-state REST API latency (p50 / p95 / p99 / mean and TLS connect time) for major crypto exchanges, measured from a fixed US East server so results stay comparable over time.

| File | What it is |
|---|---|
| [`data/latency/YYYY-MM-DD.json`](data/latency/) | One full run per UTC day: per-venue latency stats plus US-reachability probes. |
| [`data/latency/history.json`](data/latency/history.json) | Rolling daily time series (p50 + p95 per venue) for trend analysis. One record per UTC day. |

The matching human view, with a p95-over-time chart and per-venue ranking, lives at **[fillbench.com/exchange-api-latency](https://fillbench.com/exchange-api-latency)**.

## Field reference

See [DATA_DICTIONARY.md](DATA_DICTIONARY.md) for what every field means.

## Method (summary)

Each measured venue gets one persistent keep-alive HTTPS connection. We warm it up, then time back-to-back GET requests to a small public market-data endpoint (no API keys, no auth, no orders). The one-time TLS handshake is timed separately and reported as `connect_ms`, not mixed into request latency. Any non-200 or error is excluded from the stats and counted separately.

Every run executes from the same fixed US East server. That fixed vantage point is the point: it keeps the comparison between exchanges stable from run to run instead of drifting with whatever cloud region happened to host the test. Your own latency depends on where your bot runs; read these as a fair relative ranking from one consistent US vantage point. Full methodology: [fillbench.com/methodology](https://fillbench.com/methodology).

## Update cadence

The benchmark reruns every 2 hours. This mirror is refreshed from those runs. For the freshest single run, the site always serves it at [fillbench.com/data/latency-latest.json](https://fillbench.com/data/latency-latest.json).

## License

Data is released under [Creative Commons Attribution 4.0 (CC BY 4.0)](LICENSE). You are free to use, share, and build on it, including commercially, as long as you give credit.

**Attribution:** "Latency data by FillBench (https://fillbench.com), CC BY 4.0."

## Citing this data

> FillBench. "Crypto Exchange REST API Latency Benchmark." https://fillbench.com/exchange-api-latency

Questions or a venue you want added? Open an issue, or see [fillbench.com/contact](https://fillbench.com/contact).
