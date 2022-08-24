# Fair Selling

A [BadgerDAO](https://app.badger.com/) sponsored repo of Open Source Contracts for:
- Integrating Smart Contracts with Cowswap

## Why bother

We understand that we cannot prove a optimal price because at any time a new source of liquidity may be available and the contract cannot adapt.

However we believe that given a set of constraints (available Dexes, handpicked), we can efficiently compute the best trade available to us

In exploring this issue we aim to:
- Find the most gas-efficient way to get the best executable price (currently 120 /150k per quote, from 1.6MLN)
- Finding the most reliable price we can, to determine if an offer is fair or unfair (Cowswap integration)
- Can we create a "trustless swap" that is provably not frontrun nor manipulated?
- How would such a "self-defending" contract act and how would it be able to defend itself, get the best quote, and be certain of it (with statistical certainty)

# Notable Contracts
## CowswapSeller

OnChain Integration with Cowswap, all the functions you want to:
- Verify an Order
- Retrieve the OrderUid from the orderData
- Validate an order through basic security checks (price is correct, sends to correct recipient)
- Integrated with an onChain Pricer (see below), to offer stronger execution guarantees