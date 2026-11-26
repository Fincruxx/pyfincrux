import unittest
from unittest.mock import patch

from fincrux import Fincrux
from fincrux.__version__ import __version__


class _FakeResponse:
    """Minimal stand-in for a requests.Response that only needs .json()."""

    def __init__(self, payload):
        self._payload = payload

    def json(self):
        return self._payload


class FincruxRequestTests(unittest.TestCase):
    def setUp(self):
        self.client = Fincrux(api_key="test-key")

    @patch("fincrux.api.requests.request")
    def test_all_companies_builds_url_and_unwraps_data(self, request):
        request.return_value = _FakeResponse(
            {"success": "true", "data": [{"symbol": "TCS"}]}
        )

        result = self.client.all_companies()

        self.assertEqual(result, [{"symbol": "TCS"}])
        args, kwargs = request.call_args
        self.assertEqual(
            args,
            (
                "GET",
                "https://api.fincrux.org/api/all_companies?api_key=test-key",
            ),
        )
        self.assertEqual(kwargs["headers"]["Accept"], "application/json")
        self.assertEqual(kwargs["headers"]["X-Fincrux-Version"], __version__)
        self.assertIsNone(kwargs["params"])

    @patch("fincrux.api.requests.request")
    def test_search_company_formats_query_into_path(self, request):
        request.return_value = _FakeResponse(
            {"search_results": [{"symbol": "INFY"}]}
        )

        result = self.client.search_company("infosys")

        self.assertEqual(result, [{"symbol": "INFY"}])
        self.assertEqual(
            request.call_args[0][1],
            "https://api.fincrux.org/api/search/infosys?api_key=test-key",
        )

    @patch("fincrux.api.requests.request")
    def test_get_company_financials_normalises_statement_type(self, request):
        payload = {"success": "true", "data": {"revenue": 100}}
        request.return_value = _FakeResponse(payload)

        result = self.client.get_company_financials(
            "RELIANCE", statement_type="Consolidated"
        )

        self.assertEqual(result, payload)
        self.assertEqual(
            request.call_args.kwargs["params"],
            {"statement_type": "consolidated"},
        )

    def test_get_company_financials_rejects_invalid_statement_type(self):
        with self.assertRaisesRegex(ValueError, "Invalid statement_type"):
            self.client.get_company_financials(
                "RELIANCE", statement_type="audited"
            )

    @patch("fincrux.api.requests.request")
    def test_history_omits_none_dates_and_unwraps_data(self, request):
        request.return_value = _FakeResponse(
            {"success": "true", "data": [{"close": 100.5}]}
        )

        result = self.client.get_company_historicals("RELIANCE")

        self.assertEqual(result, [{"close": 100.5}])
        self.assertEqual(request.call_args.kwargs["params"], {"interval": "day"})

    @patch("fincrux.api.requests.request")
    def test_history_raises_api_message_on_failure(self, request):
        request.return_value = _FakeResponse(
            {"success": "false", "message": "invalid symbol"}
        )

        with self.assertRaisesRegex(ValueError, "invalid symbol"):
            self.client.get_company_historicals("NOPE")

    @patch("fincrux.api.requests.request")
    def test_get_fii_activity_normalises_types_and_dates(self, request):
        request.return_value = _FakeResponse(
            {"success": "true", "data": {"cash": []}}
        )

        result = self.client.get_fii_activity(
            ["Cash", "index_futures"], from_date="2026-11-01"
        )

        self.assertEqual(result, {"cash": []})
        self.assertEqual(
            request.call_args.kwargs["params"],
            {
                "data_type": "cash,index_futures",
                "interval": "1D",
                "from": "2026-11-01",
                "force_update": "false",
            },
        )

    def test_get_fii_activity_rejects_unknown_type(self):
        with self.assertRaisesRegex(ValueError, "Invalid data_type: gold"):
            self.client.get_fii_activity("cash,gold")

    @patch("fincrux.api.requests.request")
    def test_get_dii_activity_returns_rows(self, request):
        rows = [{"date": "2026-11-25", "net": 123.4}]
        request.return_value = _FakeResponse({"success": "true", "data": rows})

        self.assertEqual(self.client.get_dii_activity(), rows)

    def test_missing_api_key_raises_before_request(self):
        with self.assertRaisesRegex(ValueError, "API key is not set"):
            Fincrux(api_key="").all_companies()


if __name__ == "__main__":
    unittest.main()
