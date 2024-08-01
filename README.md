# Dakko Python SDK

Dakko Python SDK is a Python library for interacting with the Dakko Services.

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
mie.auth(token="***your token***")
```

### Market Impact Estimation

The Market Impact Estimation (MIE) service provides tools for estimating the market impact of a trade with a given size, exchange(s), direction and instrument. For example:

```python
opt_trade = mie.get_optimal_trade_size(
    exchange=["kraken", "binance"], # a single exchange or a list of exchanges
    base_asset="eth",
    trade_size=100000,
)
```

The MIE service also supports baseline backtesting capabilities with 30 days back window. To run the model in backtesting mode you need to specify `ts` or `isodate` parameter (if `isodate` is provided, `ts` will be ignored). In this case for `ts` we require UNIX timestamp format in seconds (integer), for `isodate` we require ISO 8601 format (string). For example:

```python
# example with ts
opt_trade = mie.get_optimal_trade_size(
    exchange=["kraken", "mexc", "coinbase"],
    base_asset="sol",
    quote_asset="usdt"
    trade_size=222111,
    ts=1721440800 # corresponds to 2024-08-01T23:15:36Z
)

# example with isodate
opt_trade = mie.get_optimal_trade_size(
    exchange=["mexc", "coinbase"],
    base_asset="btc",
    quote_asset="usdt"
    trade_size=123456,
    isodate="2024-08-01T23:15:36Z"
    ts=123 # will be ignored
)
```

The MIE service also supports slippage estimation across different trade sizes. For example:

```python
raw_distr = mie.estimate_slippage_across_sizes(
    exchange="binance", # a single exchange or a list of exchanges
    base_asset="sol",
    trade_size=100000,
    steps=5,
)
```

Backtesting mode is also supported for slippage estimation. You need to use the same parameters to enable execution in backtesting for 30 days window. To get method description you always can use `help` function. For example:

```python
print(help(mie.estimate_slippage_across_sizes))
```
