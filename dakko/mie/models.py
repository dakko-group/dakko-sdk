from typing import List

from pydantic import Field

from dakko.base import BaseModelEnum, ExtendedEnum

# ----------------------- #


class Exchange(ExtendedEnum):
    krkn = "kraken"
    bnce = "binance"
    bfnx = "bitfinex"
    bbsp = "bybit"
    cbse = "coinbase"
    huob = "huobi"
    okex = "okx"
    mexc = "mexc"


# ....................... #


class BaseAsset(ExtendedEnum):
    sol = "sol"
    eth = "eth"
    btc = "btc"
    dot = "dot"
    ada = "ada"
    xrp = "xrp"
    bch = "bch"
    link = "link"
    matic = "matic"
    ltc = "ltc"
    avax = "avax"


# ....................... #


class QuoteAsset(ExtendedEnum):
    usdt = "usdt"
    usd = "usd"
    usdc = "usdc"


# ----------------------- #


class MieRequest(BaseModelEnum):

    exchange: Exchange = Field(description="Exchange to estimate slippage for")
    base: BaseAsset = Field(description="Base asset to trade")
    trade_size: float = Field(description="Initial size of the trade", ge=1000)
    sell: bool = Field(description="Whether to sell the base asset")
    max_abs_slippage_bps: float = Field(
        description="Maximum allowed slippage in basis points",
        default=1,
    )
    quote: QuoteAsset = Field(
        description="Quote asset to trade against", default=QuoteAsset.usdt
    )


# ....................... #


class MieRequestRaw(BaseModelEnum):

    exchange: Exchange = Field(description="Exchange to estimate slippage for")
    base: BaseAsset = Field(description="Base asset to trade")
    trade_size: float = Field(description="Initial size of the trade", ge=1000)
    sell: bool = Field(description="Whether to sell the base asset")
    steps: int = Field(
        description="Number of steps to estimate slippage across sizes",
        default=100,
        ge=5,
        le=200,
    )
    quote: QuoteAsset = Field(
        description="Quote asset to trade against", default=QuoteAsset.usdt
    )


# ....................... #


class MieRequestMultiple(BaseModelEnum):

    exchange: List[Exchange] = Field(description="Exchanges to estimate slippage for")
    base: BaseAsset = Field(description="Base asset to trade")
    trade_size: float = Field(description="Initial size of the trade", ge=1000)
    sell: bool = Field(description="Whether to sell the base asset")
    max_abs_slippage_bps: float = Field(
        description="Maximum allowed slippage in basis points",
        default=1,
    )
    quote: QuoteAsset = Field(
        description="Quote asset to trade against", default=QuoteAsset.usdt
    )


# ....................... #


class MieRequestRawMultiple(BaseModelEnum):

    exchange: List[Exchange] = Field(description="Exchanges to estimate slippage for")
    base: BaseAsset = Field(description="Base asset to trade")
    trade_size: float = Field(description="Initial size of the trade", ge=1000)
    sell: bool = Field(description="Whether to sell the base asset")
    steps: int = Field(
        description="Number of steps to estimate slippage across sizes",
        default=100,
        ge=5,
        le=200,
    )
    quote: QuoteAsset = Field(
        description="Quote asset to trade against", default=QuoteAsset.usdt
    )


# ....................... #


class MieResponse(BaseModelEnum):

    exchange: Exchange = Field(description="Exchange for which slippage was estimated")
    base: BaseAsset = Field(description="Base asset to trade")
    quote: QuoteAsset = Field(description="Quote asset to trade against")
    optimal_size: float = Field(description="Optimal trade size")
    current_price: float = Field(description="Current price of the base asset")
    estimated_slippage: float = Field(description="Estimated slippage in basis points")


# ....................... #


class MieResponseRawEntry(BaseModelEnum):
    size: float = Field(description="Trade size")
    estimated_slippage: float = Field(description="Estimated slippage in basis points")


# ....................... #


class MieResponseRaw(BaseModelEnum):

    exchange: Exchange = Field(description="Exchange for which slippage was estimated")
    base: BaseAsset = Field(description="Base asset to trade")
    quote: QuoteAsset = Field(description="Quote asset to trade against")
    current_price: float = Field(description="Current price of the base asset")
    raw: List[MieResponseRawEntry] = Field(
        description="Estimated slippage across trade sizes"
    )
