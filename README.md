# FTX Auto Lend

FTX Auto Lend is a Python tool to automatically update the margin lending offer to include the payouts from the lending coins in the account. This effectively compounds the earnings.

## Warning

Do creating a lending sub-account as the tool:
* Lends the entire available amount for the coin in the account
* Requires a set of read-write API key and secret for it to work

# Using it

## Installation

```bash
pip3 install -r requirements.txt
```

## Get Existing Lending Info

This will check the existing info for the coin(s). The required information are `--api_key`, `--api_secret`, `--subaccount_name` and `--coin`.

```bash
python3 ftx-auto-lend.py info --api_key <api_key> --api_secret <api_secret> --subaccount_name <subaccount name> --coin BTC,ETH
```

## Update Lending Offer

This will update the lending offer for the coin(s). The required information are `--api_key`, `--api_secret`, `--subaccount_name` and `--coin`.

```bash
python3 ftx-auto-lend.py compound --api_key <api_key> --api_secret <api_secret> --subaccount_name <subaccount name> --coin BTC,ETH
```
