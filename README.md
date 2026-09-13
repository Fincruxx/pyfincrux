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
