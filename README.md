# Dakko Python SDK

Dakko Python SDK is a Python library for interacting with the Dakko Services.
Supported exchanges:

- Coinbase (only "Exchange Domestic");
- Kraken;
- MEXC;
- Bitfinex;
- Bybit;
- OKX;
- Binance;
- Huobi.

Supported base assets:

- SOL;
- ETH;
- BTC;
- DOT;
- ADA;
- XRP;
- BCH;
- LINK;
- MATIC;
- LTC;
- AVAX.

Supported quote assets:

- USDT;
- USD;
- USDC.

## Installation

Using pip:

```bash
pip install git+https://github.com/dakko-group/dakko-sdk.git
```

Using poetry:

```bash
poetry add git+https://github.com/dakko-group/dakko-sdk.git
```

## Upgrading

Using pip:

```bash
pip uninstall dakko-sdk
pip install git+https://github.com/dakko-group/dakko-sdk.git
```

Using poetry:

```bash
poetry update dakko-sdk
```

## Usage

### Authentication

To authenticate with the Dakko Services, you need to provide an API token.

```python

from dakko.mie import MarketImpactEstimation

mie = MarketImpactEstimation()
mie.auth(token="your_token")
```

### Market Impact Estimation

The Market Impact Estimation (MIE) service provides tools for estimating the market impact of a trade with a given size, exchange(s), direction and instrument:

```python
mie.get_optimal_trade_size(
    exchanges=["kraken", "binance"], # a list of exchanges or wildcard, i.e. "*" or "all"
    base_asset="eth",
    trade_size=1_000_000,
    is_sell=True,
    max_abs_slippage_bps=5,
)
```

In this case slippage threshold is a target value, so model will try to identify the best trade size for a given criteria. The MIE supports slippage estimation across different trade sizes. In this case using `steps` argument we build linear space with `start = 1000 USD` and `end = trade_size USD` points to build 2D distribution of slippage vs trade size:

```python
mie.estimate_slippage_across_sizes(
    exchanges="*", # wildcard is used
    base_asset="sol",
    trade_size=100_000,
    steps=5,
    is_sell=False,
    max_abs_slippage_bps=5,
)
```

To get estimation of a given trade size allocation across exchanges you can use the following method:

```python
mie.estimate_trade_allocation(
    exchanges="*", # wildcard
    base_asset="eth",
    quote_asset="usdt",
    trade_size=10_000_000,
    is_sell=True,
)
```

### Backtesting Mode

The MIE supports baseline backtesting capabilities with 30 days back window. To run the model in backtesting mode you need to specify `ts` or `isodate` parameter (if `isodate` is provided, `ts` will be ignored). In this case for `ts` we require UNIX timestamp format in seconds (integer), for `isodate` we require ISO 8601 format (string). For example:

```python
# example with ts
mie.get_optimal_trade_size(
    exchanges=["kraken", "mexc", "coinbase"],
    base_asset="sol",
    quote_asset="usdt",
    is_sell=True,
    trade_size=10_000_000,
    ts=1721440800 # corresponds to 2024-07-20T05:00:00Z
)

# example with isodate
mie.get_optimal_trade_size(
    exchanges=["mexc", "coinbase"],
    base_asset="btc",
    quote_asset="usdt",
    is_sell=True,
    trade_size=10_000_000,
    isodate="2024-07-20T05:00:00Z"
    ts=123 # will be ignored
)
```

The backtesting mode is also supported for slippage estimation across trade sizes. You need to use the same parameters to enable execution in backtesting for 30 days window:

```python
mie.estimate_slippage_across_sizes(
    exchanges=["coinbase"],
    base_asset="eth",
    quote_asset="usd",
    is_sell=True,
    trade_size=10_000_000,
    steps=10,
    ts=1721440800 # corresponds to 2024-07-20T05:00:00Z
)
```

We gonna add support for wider versioning and model metrics access (based on benchmarks over historical data) to enhance results and user experience.

### Help

To get method description you always can use `help` function. For example:

```python
help(mie.estimate_slippage_across_sizes)
```
