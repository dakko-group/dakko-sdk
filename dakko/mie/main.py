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

    def __init__(self, version: str = "v0"):
        self.version = version

    # ....................... #

    def auth(self, token: str):
        self.__auth_token = token

    # ....................... #

    def _get_headers(self):
        headers = {"Content-Type": "application/json"}

        if self.__auth_token:
            headers["Authorization"] = self.__auth_token

        return headers

    # ....................... #

    def _post(self, endpoint: str, data: dict) -> dict:
        url = f"{self.__api_host}/{self.version}/{endpoint}"

        with httpx.Client() as client:
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
    ) -> Dict[str, Any] | List[Dict[str, Any]]:
        if isinstance(exchange, list):
            request = MieRequestMultiple(
                exchange=exchange,
                base=base_asset,
                trade_size=trade_size,
                sell=is_sell,
                max_abs_slippage_bps=max_abs_slippage_bps,
                quote=quote_asset,
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
    ) -> Dict[str, Any] | List[Dict[str, Any]]:
        if isinstance(exchange, list):
            request = MieRequestRawMultiple(
                exchange=exchange,
                base=base_asset,
                trade_size=trade_size,
                sell=is_sell,
                steps=steps,
                quote=quote_asset,
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
            )
            return self._post("raw/single", request.model_dump())
