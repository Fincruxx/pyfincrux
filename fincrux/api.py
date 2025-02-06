import logging

import requests

from .__version__ import __title__, __version__

log = logging.getLogger(__name__)


class Fincrux:
    _default_root_uri = "https://api.fincrux.devharshit.in"
    _default_login_uri = "https://fincrux.devharshit.in/api/auth/login"

    _routes = {
        "company.all": "/api/all_companies",
        "company.search": "/api/search/{query}",
        "company.financials": "/api/financials/{company_trading_symbol}",
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
        return self._get("company.all")['data']

    def search_company(self, query):
        """
        Searches for companies by name.

        Args:
            query (str): The name of the company to search for.

        Returns:
            list: A list of company data in JSON format.
        """
        return self._get("company.search", url_args={"query": query})['search_results']

    def get_company_financials(self, company_trading_symbol):
        """
        Fetches financials for the specified company from the Fincrux API.

        Args:
            company_trading_symbol (str): The ID of the company to get financial data for.

        Returns:
            dict: The financial data for the company in JSON format.
        """
        return self._get("company.financials", url_args={"company_trading_symbol": company_trading_symbol})

    def _user_agent(self):
        return (__title__ + "-python/").capitalize() + __version__

    def _get(self, route, url_args=None, params=None, is_json=False):
        """Alias for sending a GET request."""
        return self._request(route, "GET", url_args=url_args, params=params, is_json=is_json)

    def _post(self, route, url_args=None, params=None, is_json=False, query_params=None):
        """Alias for sending a POST request."""
        return self._request(route, "POST", url_args=url_args, params=params, is_json=is_json, query_params=query_params)

    def _put(self, route, url_args=None, params=None, is_json=False, query_params=None):
        """Alias for sending a PUT request."""
        return self._request(route, "PUT", url_args=url_args, params=params, is_json=is_json, query_params=query_params)

    def _delete(self, route, url_args=None, params=None, is_json=False):
        """Alias for sending a DELETE request."""
        return self._request(route, "DELETE", url_args=url_args, params=params, is_json=is_json)

    def _request(self, route, method, url_args=None, params=None, is_json=False, query_params=None):
        """Make an HTTP request."""
        if url_args:
            uri = self._routes[route].format(**url_args)
        else:
            uri = self._routes[route]

        if self.api_key:
            url = self.root + uri + "?api_key=" + self.api_key
            response = requests.request(
                method, url, headers={
                    "X-Kite-Version": __version__,
                    "User-Agent": self._user_agent()
                }, params=params)
            return response.json()
        else:
            raise ValueError("API key is not set")
