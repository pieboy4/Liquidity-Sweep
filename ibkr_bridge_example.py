"""
IBKR bridge example for Liquidity Sweep Trader V3.

This is a starter template only. Use IBKR paper trading first.
Requires:
    pip install ib-insync flask flask-cors

Run:
    1. Open IBKR Trader Workstation or IB Gateway.
    2. Enable API in TWS/Gateway settings.
    3. Confirm paper trading port, usually 7497.
    4. python ibkr_bridge_example.py

Then the dashboard can later call http://127.0.0.1:5050/status or /quote/NQ.
"""
from flask import Flask, jsonify
from flask_cors import CORS
from ib_insync import IB, Forex, Index

app = Flask(__name__)
CORS(app)
ib = IB()

HOST = "127.0.0.1"
PORT = 7497  # paper TWS default. Live TWS often uses 7496.
CLIENT_ID = 17

@app.route("/status")
def status():
    if not ib.isConnected():
        try:
            ib.connect(HOST, PORT, clientId=CLIENT_ID, timeout=5)
        except Exception as exc:
            return jsonify({"connected": False, "error": str(exc)})
    return jsonify({"connected": ib.isConnected(), "mode": "paper-first"})

@app.route("/quote/<symbol>")
def quote(symbol: str):
    if not ib.isConnected():
        ib.connect(HOST, PORT, clientId=CLIENT_ID, timeout=5)

    symbol = symbol.upper()
    if symbol == "EURUSD":
        contract = Forex("EURUSD")
    elif symbol in {"SPX", "NDX"}:
        contract = Index(symbol, "CBOE")
    else:
        return jsonify({"error": "Supported demo symbols: EURUSD, SPX, NDX"}), 400

    ticker = ib.reqMktData(contract, "", False, False)
    ib.sleep(2)
    return jsonify({
        "symbol": symbol,
        "bid": ticker.bid,
        "ask": ticker.ask,
        "last": ticker.last,
        "close": ticker.close
    })

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5050, debug=True)
