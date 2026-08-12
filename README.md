# FillBench Data

Open, reproducible benchmark data for crypto trading: exchange REST API latency, real cost-to-trade (fee + spread + slippage), and x402 blockchain settlement latency.

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

### B2: Real cost to trade

Total one-way taker cost, in basis points, to market-buy a fixed dollar size on each US exchange: published taker fee + measured half-spread + measured order-book slippage. Measured at two sizes ($10k and $100k). Published for two assets, so you can see how cost changes between a deeply liquid coin and a mid-cap.

| File | What it is |
|---|---|
| [`data/fees/YYYY-MM-DD.json`](data/fees/) | One full BTC run per UTC day: per-venue fee, spread, and slippage at each size. |
| [`data/fees/history.json`](data/fees/history.json) | Rolling daily BTC time series (total cost bps per venue). |
| [`data/fees-sol/YYYY-MM-DD.json`](data/fees-sol/) | Same, for SOL (the mid-cap case where spread and slippage differ far more by venue). |
| [`data/fees-sol/history.json`](data/fees-sol/history.json) | Rolling daily SOL time series. |

Human views: **[fillbench.com/exchange-fees](https://fillbench.com/exchange-fees)** (BTC) and **[fillbench.com/exchange-fees-sol](https://fillbench.com/exchange-fees-sol)** (SOL).

### B6: x402 settlement latency (blockchain payment rails)

Measured time for a stablecoin micropayment to reach **true finality** on each x402-supported chain, timed from submit to on-chain finality from a fixed host. This is the settlement leg an x402 pay-per-call incurs. A chain's marketing "block time" is not the same as when a payment is final and irreversible, so we publish the measured number, not the spec. This is the on-chain settlement an x402 payment triggers (a real USDC transfer timed to finality), not the full HTTP-402 + facilitator handshake; settlement is the part that differs by chain. Every payment is a real on-chain transaction, verifiable on a block explorer.

| File | What it is |
|---|---|
| [`data/x402/x402-<chain>-settlement.json`](data/x402/) | Sequential settlement: real USDC payments on `<chain>` mainnet, each timed submit to true finality (min / p50 / p95 / max / mean). |
| [`data/x402/x402-<chain>-burst.json`](data/x402/) | Burst / throughput: a burst of concurrent USDC payments, with per-payment finality, success rate, how many one wallet lands per block or ledger, and fee under load. |

Published: **Algorand** (settlement + burst), **Solana** (burst), **Stellar** (settlement + burst) and **Base** (settlement + burst), each measured to that chain's true finality so the comparison stays apples-to-apples. **Cardano (ADA)** and **Hedera (HBAR)** are next. Note on Base: it is an optimistic rollup whose ~0.3s sequencer confirm is soft and reversible, so the settlement number is its true Ethereum L1 finality (~15-20 min), not the 0.3s. Note on the burst data: throughput is capped by a single free public RPC endpoint (HTTP 429 under load), not the chain, so treat `throughput_tps` as a single-free-endpoint figure; the per-payment `settle_ms` (finality) and fixed fee are the chain's own numbers. Human views with full comparison and on-chain proof: settlement **[fillbench.com/x402-payment-rails](https://fillbench.com/x402-payment-rails)**, throughput **[fillbench.com/x402-throughput](https://fillbench.com/x402-throughput)**.

## Field reference

See [DATA_DICTIONARY.md](DATA_DICTIONARY.md) for what every field means.

## Method (summary)

Each measured venue gets one persistent keep-alive HTTPS connection. We warm it up, then time back-to-back GET requests to a small public market-data endpoint (no API keys, no auth, no orders). The one-time TLS handshake is timed separately and reported as `connect_ms`, not mixed into request latency. Any non-200 or error is excluded from the stats and counted separately.

Every run executes from the same fixed US East server. That fixed vantage point is the point: it keeps the comparison between exchanges stable from run to run instead of drifting with whatever cloud region happened to host the test. Your own latency depends on where your bot runs; read these as a fair relative ranking from one consistent US vantage point. Full methodology: [fillbench.com/methodology](https://fillbench.com/methodology).

## Update cadence

The benchmarks rerun every 2 hours on the live site. This public mirror is refreshed from those runs once a day. For the freshest single run, the site always serves the latest at [`/data/latency-latest.json`](https://fillbench.com/data/latency-latest.json), [`/data/fees-latest.json`](https://fillbench.com/data/fees-latest.json), and [`/data/fees-sol-latest.json`](https://fillbench.com/data/fees-sol-latest.json).

## License

Data is released under [Creative Commons Attribution 4.0 (CC BY 4.0)](LICENSE). You are free to use, share, and build on it, including commercially, as long as you give credit.

**Attribution:** "Benchmark data by FillBench (https://fillbench.com), CC BY 4.0."

## Citing this data

> FillBench. "Crypto Exchange REST API Latency Benchmark." https://fillbench.com/exchange-api-latency
>
> FillBench. "Real Cost to Trade on US Crypto Exchanges." https://fillbench.com/exchange-fees
>
> FillBench. "x402 Settlement Latency by Chain." https://fillbench.com/x402-payment-rails

Questions or a venue you want added? Open an issue, or see [fillbench.com/contact](https://fillbench.com/contact).
