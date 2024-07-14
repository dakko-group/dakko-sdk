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

```python

from dakko.mie import MarketImpactEstimation

mie = MarketImpactEstimation()
mie.auth(token="***your token***")

opt_trade = mie.get_optimal_trade_size(
    exchange=["kraken", "binance"], # a single exchange or a list of exchanges
    base_asset="eth",
    trade_size=100000,
)

raw_distr = mie.estimate_slippage_across_sizes(
    exchange="binance", # a single exchange or a list of exchanges
    base_asset="sol",
    trade_size=100000,
    steps=5,
)
```
