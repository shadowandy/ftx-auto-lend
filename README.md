# FTX Auto Lend

FTX credits interests from the lending coins hourly back into the account. The newly credited interests are not automatically offered for lending.

FTX Auto Lend is a Python tool to automatically update the margin lending offer to include the payouts from the lending coins in the account. This effectively compounds the earnings.

Do join FTX using my [referral](https://ftx.com/#a=ftxauto).

## Warning

Please create a lending Subaccount for the tool as it:
* Lends the entire available amount for the coin in the account
* Requires a set of read-write API key and secret for it to work

# Using FTX Auto Lend

## Installation

```bash
% git clone https://github.com/shadowandy/ftx-auto-lend.git
% cd ftx-auto-lend
% pip3 install -r requirements.txt
```

## Setting up your FTX Subaccount

1. Create a subaccount (e.g., Lending)
2. Create an API key (for this new subaccount)
3. Move the coins to lend to this new subaccount
4. Lend the coins out using FTX
   * Specify the max amount
   * Specify the APY (as this tool will not change it)

## Get Existing Lending Info

This will check the existing info for the coin(s) using the `info` option. The required information are `--api_key`, `--api_secret`, `--subaccount_name` and `--coin`.

The details of the run are logged in `app.log`.

```bash
% python3 ftx-auto-lend.py info --api_key cc2988da027647d28319 --api_secret fdc343ac65db41b48f18 --subaccount_name Lending --coin BTC,ETH
```
### Example
```bash
% python3 ftx-auto-lend.py info --api_key cc2988da027647d28319 --api_secret fdc343ac65db41b48f18 --subaccount_name Lending --coin BNB,USD
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

This will update the lending offer for the coin(s) using the `compound` option. The required information are `--api_key`, `--api_secret`, `--subaccount_name` and `--coin`.

The details of the run are logged in `app.log`.

```bash
% python3 ftx-auto-lend.py compound --api_key cc2988da027647d28319 --api_secret fdc343ac65db41b48f18 --subaccount_name Lending --coin BTC,ETH
```
### Example
```bash
% python3 ftx-auto-lend.py compound --api_key cc2988da027647d28319 --api_secret fdc343ac65db41b48f18 --subaccount_name Lending --coin BNB,USD

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
