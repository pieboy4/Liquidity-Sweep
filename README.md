# Liquidity Sweep Trader V3

A static GitHub Pages dashboard for learning liquidity sweep trading with replay-first visualisation.

## What is included

- Replay Centre
- School Run Mode
- Trade212-style market radar
- Trade ticket calculator concept
- Local browser journal
- IBKR connection plan
- Beginner risk controls

## How to run locally

1. Download the ZIP.
2. Unzip it.
3. Open `index.html` in Chrome, Edge, Brave or Safari.

## How to publish on GitHub Pages

1. Create a new GitHub repository.
2. Upload `index.html` and this `README.md`.
3. Open repository Settings.
4. Go to Pages.
5. Choose Deploy from branch.
6. Select `main` and `/root`.
7. Save.
8. Open the URL GitHub provides.

## IBKR note

This version does not place trades. GitHub Pages cannot directly connect to IBKR because IBKR runs through Trader Workstation or IB Gateway on your own computer.

The correct path is:

Dashboard -> Local Python bridge -> IBKR TWS/Gateway -> Paper trading account -> Live account later.

Start with paper trading and manual confirmation only.
