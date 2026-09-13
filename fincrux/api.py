import logging
import platform

import requests

from .__version__ import __url__, __version__

log = logging.getLogger(__name__)


class Fincrux:
    _default_root_uri = "https://api.fincrux.org"
    _default_login_uri = "https://fincrux.org/api/auth/login"

    VALID_INTERVALS = {"1minute", "30minutes", "day", "week", "month"}
    VALID_MARKET_INTERVALS = {"1D", "1M"}
    VALID_FII_DATA_TYPES = {
        "index_futures",
        "stock_futures",
        "index_options",
        "stock_options",
        "cash",
    }

    _routes = {
        "company.all": "/api/all_companies",
        "company.search": "/api/search/{query}",
        "company.financials": "/api/financials/{company_trading_symbol}",
        "company.historicals": "/api/historicals/{company_trading_symbol}",
        "company.corporate_actions": "/api/corporate-actions/{company_trading_symbol}",
        "company.competitors": "/api/competitors/{company_trading_symbol}",
        "market.fii": "/api/market/fii",
        "market.dii": "/api/market/dii",
    }

    def __init__(self, api_key, root=None):
        """
        Initializes the Fincrux class with the provided API key.
        """
        self.root = root or self._default_root_uri
        self.api_key = api_key

    def all_companies(self):
        """
        Fetches a list of all companies from the Fincrux API.

        Returns:
            list: A list of company data in JSON format.
        """
        return self._get("company.all")["data"]

    def search_company(self, query: str):
        """
        Searches for companies by name.

        Args:
            query (str): The name of the company to search for.

        Returns:
            list: A list of company data in JSON format.
        """
        return self._get("company.search", url_args={"query": query})[
            "search_results"
        ]

    def get_company_financials(self, company_trading_symbol: str):
        """
        Fetches financials for the specified company from the Fincrux API.

        Args:
            company_trading_symbol (str): The trading symbol of the company.

        Returns:
            dict: The financial data for the company in JSON format.
        """
        return self._get(
            "company.financials",
            url_args={"company_trading_symbol": company_trading_symbol},
        )

    def get_company_historicals(
        self,
        company_trading_symbol: str,
        interval: str = "day",
        from_date: str = None,
        to_date: str = None,
    ):
        """
        Fetches historical data for the specified company from the Fincrux API.

        Args:
            company_trading_symbol (str): The trading symbol of the company.
            interval (str): Candle interval.
            from_date (str, optional): Start date in ``YYYY-MM-DD`` format.
            to_date (str, optional): End date in ``YYYY-MM-DD`` format.

        Returns:
            list: The historical data for the company in JSON format.
        """
        if interval not in self.VALID_INTERVALS:
            raise ValueError(
                f"Invalid interval. Choose from: {self.VALID_INTERVALS}"
            )
        response = self._get(
            "company.historicals",
            url_args={"company_trading_symbol": company_trading_symbol},
            params={
                "interval": interval,
                "from_date": from_date,
                "to_date": to_date,
            },
        )
        if response["success"] == "true":
            return response["data"]
        raise ValueError(str(response.get("message")))

    def get_corporate_actions(
        self,
        company_trading_symbol: str,
        force_update: bool = False,
    ):
        """
        Fetches corporate actions for the specified company.

        Args:
            company_trading_symbol (str): The trading symbol of the company.
            force_update (bool): Bypass cache and refresh latest data.

        Returns:
            dict | list: Corporate actions payload from the API.
        """
        response = self._get(
            "company.corporate_actions",
            url_args={"company_trading_symbol": company_trading_symbol},
            params={"force_update": str(force_update).lower()},
        )
        if response.get("success") == "true":
            return response.get("data", response)
        raise ValueError(str(response.get("message")))

    def get_competitors(
        self,
        company_trading_symbol: str,
        force_update: bool = False,
    ):
        """
        Fetches peer competitors for the specified company.

        Args:
            company_trading_symbol (str): The trading symbol of the company.
            force_update (bool): Bypass cache and refresh latest data.

        Returns:
            dict | list: Competitors payload from the API.
        """
        response = self._get(
            "company.competitors",
            url_args={"company_trading_symbol": company_trading_symbol},
            params={"force_update": str(force_update).lower()},
        )
        if response.get("success") == "true":
            return response.get("data", response)
        raise ValueError(str(response.get("message")))

    def get_fii_activity(
        self,
        data_type,
        interval: str = "1D",
        from_date: str = None,
        force_update: bool = False,
    ):
        """
        Fetches FII activity for NSE cash and F&O segments.

        Args:
            data_type (str | list[str]): One or more of
                ``index_futures``, ``stock_futures``, ``index_options``,
                ``stock_options``, ``cash``.
            interval (str): ``1D`` (daily) or ``1M`` (monthly).
            from_date (str, optional): Start date in ``YYYY-MM-DD`` format.
            force_update (bool): Bypass cache and refresh latest data.

        Returns:
            dict: Map of data_type key to FII activity rows.
        """
        if interval not in self.VALID_MARKET_INTERVALS:
            raise ValueError(
                "Invalid interval. Choose from: "
                f"{sorted(self.VALID_MARKET_INTERVALS)}"
            )

        if isinstance(data_type, (list, tuple, set)):
            types = [str(item).strip().lower() for item in data_type if item]
        else:
            types = [
                part.strip().lower()
                for part in str(data_type).split(",")
                if part.strip()
            ]

        if not types:
            raise ValueError("At least one data_type is required.")

        invalid = [item for item in types if item not in self.VALID_FII_DATA_TYPES]
        if invalid:
            raise ValueError(
                f"Invalid data_type: {', '.join(invalid)}. "
                f"Accepted values: {', '.join(sorted(self.VALID_FII_DATA_TYPES))}"
            )

        response = self._get(
            "market.fii",
            params={
                "data_type": ",".join(types),
                "interval": interval,
                "from": from_date,
                "force_update": str(force_update).lower(),
            },
        )
        if response.get("success") == "true":
            return response.get("data", {})
        raise ValueError(str(response.get("message")))

    def get_dii_activity(
        self,
        interval: str = "1D",
        from_date: str = None,
        force_update: bool = False,
    ):
        """
        Fetches DII cash-market activity.

        Args:
            interval (str): ``1D`` (daily) or ``1M`` (monthly).
            from_date (str, optional): Start date in ``YYYY-MM-DD`` format.
            force_update (bool): Bypass cache and refresh latest data.

        Returns:
            list: DII activity rows.
        """
        if interval not in self.VALID_MARKET_INTERVALS:
            raise ValueError(
                "Invalid interval. Choose from: "
                f"{sorted(self.VALID_MARKET_INTERVALS)}"
            )

        response = self._get(
            "market.dii",
            params={
                "interval": interval,
                "from": from_date,
                "force_update": str(force_update).lower(),
            },
        )
        if response.get("success") == "true":
            return response.get("data", [])
        raise ValueError(str(response.get("message")))

    def _user_agent(self):
        return (
            f"fincrux-python/{__version__} "
            f"(python/{platform.python_version()}; "
            f"{platform.system()}/{platform.release()}; "
            f"+{__url__})"
        )

    def _headers(self):
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": self._user_agent(),
            "X-Fincrux-Client": "python",
            "X-Fincrux-Version": __version__,
        }

    def _clean_params(self, params):
        if not params:
            return None
        return {key: value for key, value in params.items() if value is not None}

    def _get(self, route, url_args=None, params=None, is_json=False):
        """Alias for sending a GET request."""
        return self._request(
            route, "GET", url_args=url_args, params=params, is_json=is_json
        )

    def _post(self, route, url_args=None, params=None, is_json=False, query_params=None):
        """Alias for sending a POST request."""
        return self._request(
            route,
            "POST",
            url_args=url_args,
            params=params,
            is_json=is_json,
            query_params=query_params,
        )

    def _put(self, route, url_args=None, params=None, is_json=False, query_params=None):
        """Alias for sending a PUT request."""
        return self._request(
            route,
            "PUT",
            url_args=url_args,
            params=params,
            is_json=is_json,
            query_params=query_params,
        )

    def _delete(self, route, url_args=None, params=None, is_json=False):
        """Alias for sending a DELETE request."""
        return self._request(
            route, "DELETE", url_args=url_args, params=params, is_json=is_json
        )

    def _request(
        self,
        route,
        method,
        url_args=None,
        params=None,
        is_json=False,
        query_params=None,
    ):
        """Make an HTTP request."""
        if url_args:
            uri = self._routes[route].format(**url_args)
        else:
            uri = self._routes[route]

        if not self.api_key:
            raise ValueError("API key is not set")

        url = f"{self.root}{uri}?api_key={self.api_key}"
        response = requests.request(
            method,
            url,
            headers=self._headers(),
            params=self._clean_params(params),
        )
        return response.json()
