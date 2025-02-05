import requests

BASE_URL = "https://api.fincrux.devharshit.in"


class FincruxAPI:
    def __init__(self, api_key):
        """
        Initializes the FincruxAPI class with the provided API key.
        """
        self.api_key = api_key

    def get_company_financials(self, company_id):
        """
        Fetches financials for the specified company from the Fincrux API.

        Args:
            company_id (str): The ID of the company to get financial data for.

        Returns:
            dict: The financial data for the company in JSON format.
        """
        url = f"{BASE_URL}/api/financials/{company_id}?api_key={self.api_key}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
