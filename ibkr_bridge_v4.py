"""
Liquidity Sweep Trader V4 - IBKR/TWS bridge
Option A: NASDAQ, S&P 500, EUR/USD

Run:
  py -3.11 -m pip install ib-insync flask flask-cors
  py -3.11 ibkr_bridge_v4.py

TWS Paper Trading:
  API port: 7497
  Enable ActiveX and Socket Clients: ON

Endpoints:
  http://127.0.0.1:5050/status
  http://127.0.0.1:5050/api/prices
"""

import asyncio
import math
import random
import time
from datetime import datetime, timezone

from flask import Flask, jsonify
from flask_cors import CORS
from ib_insync import IB, Forex, Index, Stock

HOST = "127.0.0.1"
PORT = 7497          # Paper trading default. Live is usually 7496.
CLIENT_ID = 17

app = Flask(__name__)
CORS(app)
ib = IB()


def ensure_event_loop():
    """ib_insync needs an asyncio event loop. Flask threads may not have one."""
    try:
        asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)


def connect_ib():
    ensure_event_loop()
    if not ib.isConnected():
        ib.connect(HOST, PORT, clientId=CLIENT_ID, timeout=8)
        # 1 = live if subscribed. 3 = delayed if live subscription unavailable.
        # We ask for delayed because beginners often do not yet have paid market data.
        ib.reqMarketDataType(3)
    return ib


def safe_number(value):
    if value is None:
        return None
    try:
        if math.isnan(float(value)):
            return None
        return float(value)
    except Exception:
        return None


def contract_candidates(symbol):
    """Primary is the index/FX. Fallback uses ETF for US indices if index feed is unavailable."""
    if symbol == "NASDAQ":
        return [
            ("NDX index", Index("NDX", "NASDAQ", "USD")),
            ("QQQ ETF fallback", Stock("QQQ", "SMART", "USD")),
        ]
    if symbol == "SP500":
        return [
            ("SPX index", Index("SPX", "CBOE", "USD")),
            ("SPY ETF fallback", Stock("SPY", "SMART", "USD")),
        ]
    if symbol == "EURUSD":
        return [("EUR/USD FX", Forex("EURUSD"))]
    raise ValueError(f"Unknown symbol: {symbol}")


def get_price_for(symbol):
    connection = connect_ib()
    last_error = None
    for label, contract in contract_candidates(symbol):
        try:
            qualified = connection.qualifyContracts(contract)
            if not qualified:
                last_error = f"Could not qualify {label}"
                continue
            q_contract = qualified[0]
            ticker = connection.reqMktData(q_contract, "", False, False)
            connection.sleep(2.0)
            market_price = safe_number(ticker.marketPrice())
            bid = safe_number(ticker.bid)
            ask = safe_number(ticker.ask)
            last = safe_number(ticker.last)
            close = safe_number(ticker.close)
            connection.cancelMktData(q_contract)

            price = market_price or last or close
            if price is not None:
                return {
                    "symbol": symbol,
                    "source": label,
                    "price": round(price, 5),
                    "bid": None if bid is None else round(bid, 5),
                    "ask": None if ask is None else round(ask, 5),
                    "last": None if last is None else round(last, 5),
                    "close": None if close is None else round(close, 5),
                    "ok": True,
                }
            last_error = f"No market price returned for {label}. Check market data permissions/subscriptions."
        except Exception as exc:
            last_error = str(exc)
    return {"symbol": symbol, "ok": False, "price": None, "error": last_error}


@app.route("/")
def home():
    return jsonify({
        "service": "Liquidity Sweep Trader V4 IBKR Bridge",
        "status_endpoint": "/status",
        "prices_endpoint": "/api/prices",
    })


@app.route("/status")
def status():
    try:
        connect_ib()
        return jsonify({
            "connected": ib.isConnected(),
            "message": "Connected to TWS API" if ib.isConnected() else "Not connected",
            "host": HOST,
            "port": PORT,
            "clientId": CLIENT_ID,
            "account_mode": "paper_expected",
            "time_utc": datetime.now(timezone.utc).isoformat(),
        })
    except Exception as exc:
        return jsonify({
            "connected": False,
            "error": str(exc),
            "host": HOST,
            "port": PORT,
            "clientId": CLIENT_ID,
        })


@app.route("/api/prices")
def prices():
    results = {}
    for symbol in ["NASDAQ", "SP500", "EURUSD"]:
        results[symbol] = get_price_for(symbol)
    return jsonify({
        "connected": ib.isConnected(),
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "market_data_type": "delayed_if_no_live_subscription",
        "results": results,
    })


@app.route("/api/demo-replay")
def demo_replay():
    """Synthetic replay so the front end can teach the pattern even when markets are closed."""
    base = 21800 + random.randint(-50, 50)
    points = [
        ("Level forms", base),
        ("Sweep", base + 28),
        ("Reversal", base - 5),
        ("Entry", base - 18),
        ("Trade active", base - 52),
        ("Target", base - 92),
    ]
    return jsonify({
        "market": "NASDAQ",
        "direction": "SELL",
        "score": 84,
        "entry": base - 18,
        "stop": base + 35,
        "target": base - 92,
        "timeline": [{"step": i+1, "label": label, "price": price} for i, (label, price) in enumerate(points)]
    })


if __name__ == "__main__":
    print("Liquidity Sweep Trader V4 bridge starting...")
    print("Open dashboard index.html separately.")
    print("Status: http://127.0.0.1:5050/status")
    print("Prices: http://127.0.0.1:5050/api/prices")
    # threaded=False avoids ib_insync event-loop errors in request threads.
    app.run(host="127.0.0.1", port=5050, debug=False, threaded=False)
