from typing import List, Optional

from pydantic import Field

from dakko.base import Base, ExtendedEnum

# ----------------------- #


class Exchange(str, ExtendedEnum):
    krkn = "kraken"
    bnce = "binance"
    bfnx = "bitfinex"
    bbsp = "bybit"
    cbse = "coinbase"
    huob = "huobi"
    okex = "okx"
    mexc = "mexc"


# ....................... #


class BaseAsset(str, ExtendedEnum):
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


class QuoteAsset(str, ExtendedEnum):
    usdt = "usdt"
    usd = "usd"
    usdc = "usdc"


# ----------------------- #


class MieRequest(Base):

    exchange: Exchange = Field(..., description="Exchange to estimate slippage for")
    base: BaseAsset = Field(..., description="Base asset to trade")
    trade_size: float = Field(..., description="Initial size of the trade", ge=1000)
    sell: bool = Field(..., description="Whether to sell the base asset")
    max_abs_slippage_bps: float = Field(
        1,
        description="Maximum allowed slippage in basis points",
    )
    quote: QuoteAsset = Field(
        QuoteAsset.usdt,
        description="Quote asset to trade against",
    )
    ts: Optional[int] = Field(None, description="Timestamp for estimation")
    isodate: Optional[str] = Field(None, description="Datetime (ISO format)")


# ....................... #


class MieRequestRaw(Base):

    exchange: Exchange = Field(..., description="Exchange to estimate slippage for")
    base: BaseAsset = Field(..., description="Base asset to trade")
    trade_size: float = Field(..., description="Initial size of the trade", ge=1000)
    sell: bool = Field(..., description="Whether to sell the base asset")
    steps: int = Field(
        100,
        description="Number of steps to estimate slippage across sizes",
        ge=5,
        le=200,
    )
    quote: QuoteAsset = Field(
        QuoteAsset.usdt,
        description="Quote asset to trade against",
    )
    ts: Optional[int] = Field(None, description="Timestamp for estimation")
    isodate: Optional[str] = Field(None, description="Datetime (ISO format)")


# ....................... #


class MieRequestMultiple(Base):

    exchange: List[Exchange] = Field(
        ...,
        description="Exchanges to estimate slippage for",
    )
    base: BaseAsset = Field(..., description="Base asset to trade")
    trade_size: float = Field(..., description="Initial size of the trade", ge=1000)
    sell: bool = Field(..., description="Whether to sell the base asset")
    max_abs_slippage_bps: float = Field(
        1,
        description="Maximum allowed slippage in basis points",
    )
    quote: QuoteAsset = Field(
        QuoteAsset.usdt,
        description="Quote asset to trade against",
    )
    ts: Optional[int] = Field(None, description="Timestamp for estimation")
    isodate: Optional[str] = Field(None, description="Datetime (ISO format)")


# ....................... #


class MieRequestRawMultiple(Base):

    exchange: List[Exchange] = Field(
        ..., description="Exchanges to estimate slippage for"
    )
    base: BaseAsset = Field(..., description="Base asset to trade")
    trade_size: float = Field(..., description="Initial size of the trade", ge=1000)
    sell: bool = Field(..., description="Whether to sell the base asset")
    steps: int = Field(
        100,
        description="Number of steps to estimate slippage across sizes",
        ge=5,
        le=200,
    )
    quote: QuoteAsset = Field(
        QuoteAsset.usdt,
        description="Quote asset to trade against",
    )
    ts: Optional[int] = Field(None, description="Timestamp for estimation")
    isodate: Optional[str] = Field(None, description="Datetime (ISO format)")


# ....................... #


class MieResponse(Base):

    exchange: Exchange = Field(
        ...,
        description="Exchange for which slippage was estimated",
    )
    base: BaseAsset = Field(..., description="Base asset to trade")
    quote: QuoteAsset = Field(..., description="Quote asset to trade against")
    optimal_size: float = Field(..., description="Optimal trade size")
    current_price: float = Field(..., description="Current price of the base asset")
    estimated_slippage: float = Field(
        ...,
        description="Estimated slippage in basis points",
    )
    ts: Optional[int | float] = Field(None, description="Timestamp")
    isodate: Optional[str] = Field(None, description="Datetime (ISO format)")


# ....................... #


class MieResponseRawEntry(Base):
    size: float = Field(..., description="Trade size")
    estimated_slippage: float = Field(
        ...,
        description="Estimated slippage in basis points",
    )


# ....................... #


class MieResponseRaw(Base):

    exchange: Exchange = Field(
        ...,
        description="Exchange for which slippage was estimated",
    )
    base: BaseAsset = Field(..., description="Base asset to trade")
    quote: QuoteAsset = Field(..., description="Quote asset to trade against")
    current_price: float = Field(..., description="Current price of the base asset")
    raw: List[MieResponseRawEntry] = Field(
        ...,
        description="Estimated slippage across trade sizes",
    )
    ts: Optional[int | float] = Field(None, description="Timestamp")
    isodate: Optional[str] = Field(None, description="Datetime (ISO format)")
