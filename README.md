# FTX Auto Lend

FTX Auto Lend is a Python tool to automatically update the margin lending offer to include the payouts from the lending coins in the account. This effectively compounds the earnings.

## Warning

Do creating a lending sub-account as the tool:
* Lends the entire available amount for the coin in the account
* Requires a set of read-write API key and secret for it to work

# Using it

## Installation

```bash
% git clone https://github.com/shadowandy/ftx-auto-lend.git
% cd ftx-auto-lend
% pip3 install -r requirements.txt
```

## Get Existing Lending Info

This will check the existing info for the coin(s). The required information are `--api_key`, `--api_secret`, `--subaccount_name` and `--coin`.

```bash
% python3 ftx-auto-lend.py info --api_key 123fasc --api_secret fsac123 --subaccount_name Lending --coin BTC,ETH
```
```bash
% python3 ftx-auto-lend.py info --api_key 123fasc --api_secret fsac123 --subaccount_name Lending --coin BNB,USD
Subaccount: Lending
Coin: BNB
     Locked  : 2.49181547
     Offered : 2.49181547
     Lendable: 2.49181547
     Rate    : 3.42e-06
Coin: USD
     Locked  : 3527.64021287
     Offered : 3527.64021287
     Lendable: 3527.71270588
     Rate    : 3.42e-06
```

## Update Lending Offer

This will update the lending offer for the coin(s). The required information are `--api_key`, `--api_secret`, `--subaccount_name` and `--coin`.

```bash
% python3 ftx-auto-lend.py compound --api_key 123fasc --api_secret fsac123 --subaccount_name Lending --coin BTC,ETH
```
```bash
% python3 ftx-auto-lend.py compound --api_key 123fasc --api_secret fsac123 --subaccount_name Lending --coin BNB,USD
Coin: BNB
     Amount (old): 2.49181547
     Amount (new): 2.49181547
     Rate        : 3.42e-06
     No need to update lending amount.
Coin: USD
     Amount (old): 3527.64021287
     Amount (new): 3527.71270588
     Rate        : 3.42e-06
```
