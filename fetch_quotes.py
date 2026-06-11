"""Fetch delayed stock quotes + 1-month history and write docs/quotes.json.

Runs inside GitHub Actions (server-side, so no CORS restrictions).
Data source: Yahoo Finance via yfinance. Quotes are typically ~15 min
delayed for most exchanges. Edit TICKERS to taste — Yahoo symbols:
US tickers plain (AAPL), Euronext Amsterdam with .AS (ASML.AS),
indices with ^ (^AEX, ^GSPC).
"""

import datetime
import json
import pathlib
import time

import yfinance as yf

TICKERS = [
    "AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "META", "TSLA",
    "ASML.AS", "ADYEN.AS", "^AEX", "^GSPC", "^NDX",
]

OUT = pathlib.Path(__file__).parent / "docs" / "quotes.json"


def fetch_one(symbol: str):
    t = yf.Ticker(symbol)
    fi = t.fast_info
    last = fi.last_price
    prev = fi.previous_close
    if last is None or prev in (None, 0):
        return None
    hist = t.history(period="1mo", interval="1d")["Close"].dropna()
    return {
        "symbol": symbol,
        "name": getattr(fi, "shortName", None) or symbol,
        "last": round(float(last), 4),
        "chg_pct": round((float(last) - float(prev)) / float(prev) * 100, 2),
        "currency": getattr(fi, "currency", "") or "",
        "hist": [round(float(v), 4) for v in hist.tolist()][-30:],
    }


def main():
    quotes = []
    for sym in TICKERS:
        for attempt in range(2):
            try:
                q = fetch_one(sym)
                if q:
                    quotes.append(q)
                break
            except Exception as exc:  # noqa: BLE001 — per-symbol resilience
                print(f"{sym}: attempt {attempt + 1} failed: {exc}")
                time.sleep(2)
        time.sleep(0.4)  # be polite

    if not quotes:
        raise SystemExit("No quotes fetched — leaving previous quotes.json untouched.")

    payload = {
        "updated": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "source": "Yahoo Finance via yfinance (delayed ~15 min)",
        "quotes": quotes,
    }
    OUT.write_text(json.dumps(payload, separators=(",", ":")) + "\n")
    print(f"Wrote {len(quotes)}/{len(TICKERS)} quotes to {OUT}")


if __name__ == "__main__":
    main()
