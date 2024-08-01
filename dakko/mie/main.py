from typing import Any, Dict, List, Optional

import httpx

from .models import (
    BaseAsset,
    Exchange,
    MieRequest,
    MieRequestMultiple,
    MieRequestRaw,
    MieRequestRawMultiple,
    QuoteAsset,
)

# ----------------------- #


class MarketImpactEstimation:
    __api_host: str = "http://mie-api-alb-625552804.us-east-2.elb.amazonaws.com"
    __auth_token: Optional[str] = None

    # ....................... #

    def __init__(self, version: str = "v0") -> None:
        self.version = version

    # ....................... #

    def auth(self, token: str) -> None:
        self.__auth_token = token

    # ....................... #

    def _get_headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}

        if self.__auth_token:
            headers["Authorization"] = self.__auth_token

        return headers

    # ....................... #

    def _post(self, endpoint: str, data: Dict[str, Any]) -> Any:
        url = f"{self.__api_host}/{self.version}/{endpoint}"

        with httpx.Client() as client:  # check concurrent requests
            response = client.post(url, headers=self._get_headers(), json=data)
            response.raise_for_status()

            return response.json()

    # ....................... #

    def get_optimal_trade_size(
        self,
        exchange: Exchange | List[Exchange],
        base_asset: BaseAsset,
        quote_asset: QuoteAsset = QuoteAsset.usdt,
        trade_size: float = 10000,
        is_sell: bool = True,
        max_abs_slippage_bps: float = 1,
        ts: Optional[int] = None,
        isodate: Optional[str] = None,
    ) -> Dict[str, Any] | List[Dict[str, Any]]:
        """Get the optimal trade size for given exchange(s).

        Args:
            exchange (Exchange | List[Exchange]): Exchange(s) to estimate slippage for
            base_asset (BaseAsset): Base asset to trade
            quote_asset (QuoteAsset, optional): Quote asset to trade against. Defaults to QuoteAsset.usdt.
            trade_size (float, optional): Initial size of the trade. Defaults to 10000.
            is_sell (bool, optional): Whether to sell the base asset. Defaults to True.
            max_abs_slippage_bps (float, optional): Maximum allowed slippage in basis points. Defaults to 1.
            ts (Optional[int], optional): Timestamp for estimation. Defaults to None.
            isodate (Optional[str], optional): Datetime (ISO format). Defaults to None.

        Returns:
            res (Dict[str, Any] | List[Dict[str, Any]]): Optimal trade size for the given exchange(s)
        """

        if isinstance(exchange, list):
            request = MieRequestMultiple(
                exchange=exchange,
                base=base_asset,
                trade_size=trade_size,
                sell=is_sell,
                max_abs_slippage_bps=max_abs_slippage_bps,
                quote=quote_asset,
                ts=ts,
                isodate=isodate,
            )
            return self._post("optimal/multiple", request.model_dump())

        else:
            request = MieRequest(
                exchange=exchange,
                base=base_asset,
                trade_size=trade_size,
                sell=is_sell,
                max_abs_slippage_bps=max_abs_slippage_bps,
                quote=quote_asset,
                ts=ts,
                isodate=isodate,
            )
            return self._post("optimal/single", request.model_dump())

    # ....................... #

    def estimate_slippage_across_sizes(
        self,
        exchange: Exchange | List[Exchange],
        base_asset: BaseAsset,
        quote_asset: QuoteAsset = QuoteAsset.usdt,
        trade_size: float = 10000,
        is_sell: bool = True,
        steps: int = 10,
        ts: Optional[int] = None,
        isodate: Optional[str] = None,
    ) -> Dict[str, Any] | List[Dict[str, Any]]:
        """Estimate slippage across trade sizes for given exchange(s).

        Args:
            exchange (Exchange | List[Exchange]): Exchange(s) to estimate slippage for
            base_asset (BaseAsset): Base asset to trade
            quote_asset (QuoteAsset, optional): Quote asset to trade against. Defaults to QuoteAsset.usdt.
            trade_size (float, optional): Initial size of the trade. Defaults to 10000.
            is_sell (bool, optional): Whether to sell the base asset. Defaults to True.
            steps (int, optional): Number of steps to estimate slippage across sizes. Defaults to 10.
            ts (Optional[int], optional): Timestamp for estimation. Defaults to None.
            isodate (Optional[str], optional): Datetime (ISO format). Defaults to None.

        Returns:
            res (Dict[str, Any] | List[Dict[str, Any]]): Estimated slippage across trade sizes for the given exchange(s)
        """

        if isinstance(exchange, list):
            request = MieRequestRawMultiple(
                exchange=exchange,
                base=base_asset,
                trade_size=trade_size,
                sell=is_sell,
                steps=steps,
                quote=quote_asset,
                ts=ts,
                isodate=isodate,
            )
            return self._post("raw/multiple", request.model_dump())

        else:
            request = MieRequestRaw(
                exchange=exchange,
                base=base_asset,
                trade_size=trade_size,
                sell=is_sell,
                steps=steps,
                quote=quote_asset,
                ts=ts,
                isodate=isodate,
            )
            return self._post("raw/single", request.model_dump())
