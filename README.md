# Liquidity Sweep Trader V4

Replay-first day-trading learning dashboard connected to IBKR Paper Trading through TWS.

## What V4 does

- Connects to TWS Paper Trading through a local Flask bridge.
- Pulls prices for the first three markets only:
  - NASDAQ: NDX index, with QQQ fallback
  - S&P 500: SPX index, with SPY fallback
  - EUR/USD: IBKR FX contract
- Shows a polished dashboard with market radar, replay centre, trade ticket and journal.
- Does not place trades.
- Designed for paper testing and tiny-risk learning.

## Files

- `index.html` — dashboard app
- `ibkr_bridge_v4.py` — local Python bridge to TWS
- `README.md` — setup guide

## Step 1 — Open TWS

Use Trader Workstation, not IBKR Desktop.

Login to Paper Trading.

Then go to:

File → Global Configuration → API → Settings

Tick:

Enable ActiveX and Socket Clients

Confirm port:

7497

## Step 2 — Install Python packages

Open PowerShell in the folder containing this project and run:

```powershell
py -3.11 -m pip install ib-insync flask flask-cors
```

## Step 3 — Start the bridge

```powershell
py -3.11 ibkr_bridge_v4.py
```

Leave this PowerShell window open.

## Step 4 — Test connection

Open another PowerShell window and run:

```powershell
curl http://127.0.0.1:5050/status -UseBasicParsing
```

Expected:

```json
{"connected": true, "message": "Connected to TWS API"}
```

## Step 5 — Open the dashboard

Double-click:

`index.html`

Then click:

- Check IBKR
- Fetch Prices
- Play Replay

## Notes

If NASDAQ or S&P 500 returns no data, you probably do not have index market-data permissions. The bridge then tries QQQ and SPY as fallback instruments.

This is not a live-order system. It is a learning dashboard and scanner base.
