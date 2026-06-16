# Liquidity Sweep Trader V5

## What V5 is

V5 is a replay-first learning dashboard connected to IBKR/TWS market data.

It is designed for:

- learning day trading
- paper trading first
- read-only market data
- replay review
- school-run mode
- simple trade tickets

It does **not** place orders.

## Folder recommendation

Move this project to:

```text
C:\Trading\Liquidity-Sweep-Trader-V5
```

Do not run it from your Desktop long term.

## Required software

- Windows 11
- Python 3.11.9
- TWS installed
- TWS logged into Paper Trading
- TWS API enabled
- Read-Only API kept ON for now

## Install packages

```powershell
py -3.11 -m pip install ib-insync flask flask-cors
```

## Start TWS

1. Open TWS.
2. Log into Paper Trading.
3. Go to:

```text
File → Global Configuration → API → Settings
```

4. Check:

```text
Enable ActiveX and Socket Clients = ON
Socket port = 7497
Read-Only API = ON
```

## Start the IBKR bridge

Open PowerShell in the V5 folder:

```powershell
cd "C:\Trading\Liquidity-Sweep-Trader-V5"
py -3.11 ibkr_bridge_v5.py
```

Leave this PowerShell window open.

## Test the bridge

Open in your browser:

```text
http://127.0.0.1:5050/status
```

Expected:

```json
{"connected": true}
```

Then test:

```text
http://127.0.0.1:5050/api/snapshot
```

You should see NASDAQ, S&P 500 and EUR/USD price data plus setup scores.

## Start the dashboard

Open a second PowerShell window in the same V5 folder:

```powershell
py -m http.server 8000
```

Then open:

```text
http://127.0.0.1:8000
```

Do not double-click `index.html` once you are connecting to the bridge.

## Daily routine

### Morning

1. Open TWS Paper Trading.
2. Start `ibkr_bridge_v5.py`.
3. Start the dashboard server.
4. Press **Check IBKR**.
5. Press **Fetch Snapshot**.
6. Review the best setup and replay.

### Before school run

Press **Fetch Snapshot**.

### After school run

Press **Fetch Snapshot** again.

If a setup appeared, open Replay Centre and review the sequence.

## What the score means

- 0-49: No trade
- 50-71: Watch
- 72-100: Setup worth reviewing

The score is not a promise of profit. It is a teaching filter.

## Safety rules

Keep these until you have at least 100 logged paper trades:

- Read-Only API ON
- Paper Trading only
- £1 theoretical risk per trade
- No automated orders
- No live trading

## V5 limitations

V5 uses a simple recent-price model to approximate levels. It is a learning scanner, not yet a professional session-based execution engine.

Version 6 should add:

- proper historical 1-minute candles
- true Asia/London/New York session levels
- automatic saved signals while away
- candlestick replay
- CSV journal export
- paper order placement after manual confirmation
