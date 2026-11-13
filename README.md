# Fincrux Python Package

Official Python client for the Fincrux API.

## Installation

```bash
pip install fincrux
```

## Quick start

```python
from fincrux import Fincrux

client = Fincrux(api_key="YOUR_API_KEY")

# Company data
financials = client.get_company_financials("RELIANCE")
financials_consolidated = client.get_company_financials(
    "RELIANCE", statement_type="consolidated"
)
filings = client.get_company_filings("RELIANCE")
news = client.get_company_news("RELIANCE", page_number=1, page_size=20)
historicals = client.get_company_historicals("RELIANCE", interval="day")
actions = client.get_corporate_actions("RELIANCE")
peers = client.get_competitors("RELIANCE")

# Market institutional flows
fii = client.get_fii_activity(data_type="cash", interval="1D")
fii_fo = client.get_fii_activity(
    data_type=["index_futures", "stock_futures"],
    interval="1D",
)
dii = client.get_dii_activity(interval="1D")
```

## Company methods

### `get_company_financials`

| Arg | Required | Notes |
| --- | --- | --- |
| `company_trading_symbol` | yes | NSE trading symbol |
| `statement_type` | no | `standalone` (default) or `consolidated` |

### `get_company_filings`

Returns recent announcements and annual reports, including the original filing link, publication timestamp, and a title-derived `is_revised` flag.

| Arg | Required | Notes |
| --- | --- | --- |
| `company_trading_symbol` | yes | NSE trading symbol |
| `force_update` | no | `False` by default |

### `get_company_news`

| Arg | Required | Notes |
| --- | --- | --- |
| `company_trading_symbol` | yes | NSE trading symbol |
| `page_number` | no | `1` by default (1-100) |
| `page_size` | no | `20` by default (1-100) |

## Market methods

### `get_fii_activity`

| Arg | Required | Notes |
| --- | --- | --- |
| `data_type` | yes | `cash`, `index_futures`, `stock_futures`, `index_options`, `stock_options` (string or list) |
| `interval` | no | `1D` (default) or `1M` |
| `from_date` | no | `YYYY-MM-DD` |
| `force_update` | no | `False` by default |

### `get_dii_activity`

| Arg | Required | Notes |
| --- | --- | --- |
| `interval` | no | `1D` (default) or `1M` |
| `from_date` | no | `YYYY-MM-DD` |
| `force_update` | no | `False` by default |
