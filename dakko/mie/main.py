from typing import Any, Dict, List, Optional, Sequence, get_args

import httpx
import pandas as pd  # noqa: F401

from dakko.base.typing import Wildcard

from .models import (
    BaseAsset,
    Exchange,
    MieRequestMultiple,
    MieRequestRawMultiple,
    QuoteAsset,
)

# ----------------------- #


class MarketImpactEstimation:
    __api_host: str = "http://mie-api-alb-625552804.us-east-2.elb.amazonaws.com"
    __auth_token: Optional[str] = None

    # ....................... #

    def __init__(self, version: str = "v0") -> None:
        assert version in [
            "v0",
            "v1",
        ], "Invalid version. Supported versions are v0 and v1"

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
            response = client.post(
                url, headers=self._get_headers(), json=data, timeout=30
            )
            response.raise_for_status()

            return response.json()

    # ....................... #

    def __get_optimal_trade_size_deprecated(
        self,
        exchanges: List[Exchange] | Wildcard,
        trade_size: float,
        is_sell: bool,
        base_asset: BaseAsset,
        quote_asset: QuoteAsset = QuoteAsset.usdt,
        max_abs_slippage_bps: float = 1,
        ts: Optional[int] = None,
        isodate: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Get the optimal trade size for given exchange(s).

        Args:
            exchange (List[Exchange] | Wildcard): Exchange(s) to estimate slippage for
            trade_size (float): Initial size of the trade
            is_sell (bool): Whether to sell the base asset
            base_asset (BaseAsset): Base asset to trade
            quote_asset (QuoteAsset, optional): Quote asset to trade against. Defaults to "usdt"
            max_abs_slippage_bps (float, optional): Maximum allowed slippage in basis points. Defaults to 1
            ts (int, optional): Timestamp for estimation. Defaults to None
            isodate (str, optional): Datetime (ISO format). Defaults to None

        Returns:
            res (List[Dict[str, Any]]): Optimal trade size for the given exchange(s)
        """

        if exchanges in get_args(Wildcard):
            exchanges = Exchange.list()

        request = MieRequestMultiple(
            exchange=exchanges,
            base=base_asset,
            trade_size=trade_size,
            sell=is_sell,
            max_abs_slippage_bps=max_abs_slippage_bps,
            quote=quote_asset,
            ts=ts,
            isodate=isodate,
        )
        return self._post("optimal/multiple", request.model_dump())

    # ....................... #

    def estimate_slippage_across_sizes(
        self,
        exchanges: List[Exchange] | Wildcard,
        trade_size: float,
        is_sell: bool,
        base_asset: BaseAsset,
        quote_asset: QuoteAsset = QuoteAsset.usdt,
        steps: int = 10,
        ts: Optional[int] = None,
        isodate: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Estimate slippage across trade sizes for given exchange(s).

        Args:
            exchange (List[Exchange] | Wildcard): Exchange(s) to estimate slippage for
            trade_size (float): Initial size of the trade
            is_sell (bool): Whether to sell the base asset
            base_asset (BaseAsset): Base asset to trade
            quote_asset (QuoteAsset, optional): Quote asset to trade against. Defaults to "usdt"
            steps (int, optional): Number of steps to estimate slippage across sizes. Defaults to 10
            ts (int, optional): Timestamp for estimation. Defaults to None
            isodate (str, optional): Datetime (ISO format). Defaults to None

        Returns:
            res (List[Dict[str, Any]]): Estimated slippage across trade sizes for the given exchange(s)
        """

        assert self.version == "v0", "This method is only available in v0"

        if exchanges in get_args(Wildcard):
            exchanges = Exchange.list()

        request = MieRequestRawMultiple(
            exchange=exchanges,
            base=base_asset,
            trade_size=trade_size,
            sell=is_sell,
            steps=steps,
            quote=quote_asset,
            ts=ts,
            isodate=isodate,
        )
        return self._post("raw/multiple", request.model_dump())

    # ....................... #

    @staticmethod
    def __closest_size(df: pd.DataFrame, threshold_abs: float = 1):
        def find_closest_size_with_max_size(group, threshold_abs):
            group["slippage_diff"] = (
                abs(group["estimated_slippage"]) - abs(threshold_abs)
            ).abs()
            min_slippage_diff = group["slippage_diff"].min()
            filtered_group = group[group["slippage_diff"] == min_slippage_diff]

            return filtered_group.loc[filtered_group["size"].idxmax()]

        # ....................... #

        all_columns = df.columns.tolist()
        closest_sizes = df.groupby("exchange")[all_columns].apply(
            lambda group: find_closest_size_with_max_size(group, threshold_abs)
        )
        closest_sizes.drop(columns=["slippage_diff"], inplace=True)
        closest_sizes.reset_index(drop=True, inplace=True)

        return closest_sizes

    # ....................... #

    def get_optimal_trade_size(
        self,
        exchanges: Sequence[Exchange] | Wildcard,
        trade_size: float,
        is_sell: bool,
        base_asset: BaseAsset,
        quote_asset: QuoteAsset = QuoteAsset.usdt,
        max_abs_slippage_bps: float = 1,
        ts: Optional[int] = None,
        isodate: Optional[str] = None,
    ):
        """Get the optimal trade size for given exchange(s).

        Args:
            exchange (List[Exchange] | Wildcard): Exchange(s) to estimate slippage for
            trade_size (float): Initial size of the trade
            is_sell (bool): Whether to sell the base asset
            base_asset (BaseAsset): Base asset to trade
            quote_asset (QuoteAsset, optional): Quote asset to trade against. Defaults to "usdt"
            abs_slippage_bps (float, optional): Maximum allowed slippage in basis points. Defaults to 1
            ts (int, optional): Timestamp for estimation. Defaults to None
            isodate (str, optional): Datetime (ISO format). Defaults to None

        Returns:
            res (pd.DataFrame): Optimal trade size for the given exchange(s)
        """

        if exchanges in get_args(Wildcard):
            exchanges = Exchange.list()

        request = MieRequestRawMultiple(
            exchange=exchanges,
            base=base_asset,
            trade_size=trade_size,
            sell=is_sell,
            steps=200,
            quote=quote_asset,
            ts=ts,
            isodate=isodate,
        )
        res = self._post("raw/multiple", request.model_dump())

        empty_df = pd.DataFrame()

        for data in res:
            df_raw = pd.DataFrame(data.pop("raw"))

            for k, v in data.items():
                df_raw[k] = v

            empty_df = pd.concat([empty_df, df_raw])

        res = self.__closest_size(empty_df, max_abs_slippage_bps)
        best_price = (
            res["current_price"].max() if is_sell else res["current_price"].min()
        )
        res["cross_ex_slippage"] = abs(
            (res["current_price"] - best_price) / best_price * 10_000
        )
        res["size_quote"] = res["size"]
        res["size_base"] = res["size_quote"] / res["current_price"]

        res = res.sort_values("cross_ex_slippage", ascending=True).reset_index(
            drop=True
        )

        res = res[
            [
                "ts",
                "isodate",
                "exchange",
                "base",
                "quote",
                "current_price",
                "estimated_slippage",
                "cross_ex_slippage",
                "size_quote",
                "size_base",
            ]
        ].copy()

        return res

    # ....................... #

    def estimate_trade_allocation(
        self,
        exchanges: Sequence[Exchange] | Wildcard,
        trade_size: float,
        is_sell: bool,
        base_asset: BaseAsset,
        quote_asset: QuoteAsset = QuoteAsset.usdt,
        max_abs_slippage_bps: float = 1,
        ts: Optional[int] = None,
        isodate: Optional[str] = None,
    ):

        res: pd.DataFrame = self.get_optimal_trade_size(
            exchanges=exchanges,
            trade_size=trade_size,
            is_sell=is_sell,
            base_asset=base_asset,
            quote_asset=quote_asset,
            max_abs_slippage_bps=max_abs_slippage_bps,
            ts=ts,
            isodate=isodate,
        )

        coverage = 0

        for i in range(res.shape[0]):
            row = res.loc[i]
            size = row["size_quote"]

            if trade_size - coverage > size:
                coverage += size

            else:

                res.loc[i, "size_quote"] = trade_size - coverage
                res.loc[i, "size_base"] = (trade_size - coverage) / res.loc[
                    i, "current_price"
                ]
                coverage = trade_size
                res = res.loc[:i]
                break

        res = res[
            [
                "ts",
                "isodate",
                "exchange",
                "base",
                "quote",
                "current_price",
                "estimated_slippage",
                "cross_ex_slippage",
                "size_quote",
                "size_base",
            ]
        ].copy()

        return res
