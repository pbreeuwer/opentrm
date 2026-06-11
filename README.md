# OPENTRM — free live market terminal

A Bloomberg-style terminal built entirely on free, public, key-less data:

- **Crypto** — true real-time via Binance public WebSocket (watchlist, candlestick chart, order book, movers)
- **FX** — official ECB reference rates via Frankfurter
- **Stocks** — ~15-min-delayed quotes (Yahoo Finance), fetched every ~10 minutes by a free GitHub Actions job in this repo and served to the page as `docs/quotes.json`

The whole site lives in `docs/` and is served by GitHub Pages. No server, no API keys, no cost.

## Customizing

- **Stock tickers:** edit the `TICKERS` list at the top of `fetch_quotes.py`. Yahoo symbol format: US tickers plain (`AAPL`), Euronext Amsterdam with `.AS` (`ASML.AS`), indices with `^` (`^AEX`).
- **Refresh rate:** edit the `cron` line in `.github/workflows/quotes.yml` (GitHub minimum: every 5 minutes).
- **Crypto watchlist:** edit the `WL` array near the top of the script in `docs/index.html`.

## Things to know

- Stock data is delayed ~15 minutes by the source, plus the cron interval. Real-time equity feeds are licensed by exchanges and are never legally free. The crypto panels are genuinely real-time.
- GitHub pauses scheduled workflows after ~60 days without repo activity — re-enable from the Actions tab if the stocks panel goes stale.
- `fetch_quotes.py` uses Yahoo's unofficial endpoints via `yfinance`; if the job starts failing, it usually self-heals since yfinance installs fresh on every run.

Nothing in this project is investment advice.
