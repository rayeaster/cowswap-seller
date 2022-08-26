import brownie
from brownie import *
from brownie.test import given, strategy
import pytest

from scripts.send_order import get_cowswap_order_quote

"""
  Fuzz
    Fuzz any random token address
    To compare cowswap quote with pricer quote

    ## This will take almost an hour. Consider using foundry :P
"""
## TOKENS 
USDC = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
WBTC = "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599"
USDT = "0xdAC17F958D2ee523a2206206994597C13D831ec7"
SPELL = "0x090185f2135308bad17527004364ebcc2d37e5f6"
ALCX = "0xdbdb4d16eda451d0503b854cf79d55697f90c8df"
LFT = "0xB620Be8a1949AA9532e6a3510132864EF9Bc3F82"

## Mostly Aura
AURA = "0xC0c293ce456fF0ED870ADd98a0828Dd4d2903DBF"
AURA_BAL = "0x616e8BfA43F920657B3497DBf40D6b1A02D4608d"

BADGER = "0x3472A5A71965499acd81997a54BBA8D852C6E53d"

SD = "0x30d20208d987713f46dfd34ef128bb16c404d10f" ## Pretty much completely new token https://etherscan.io/token/0x30d20208d987713f46dfd34ef128bb16c404d10f#balances

DFX = "0x888888435FDe8e7d4c54cAb67f206e4199454c60" ## Fairly Liquid: https://etherscan.io/token/0x888888435FDe8e7d4c54cAb67f206e4199454c60#balances

FDT = "0xEd1480d12bE41d92F36f5f7bDd88212E381A3677" ## Illiquid as of today, in vault but no pool I could find https://etherscan.io/token/0xEd1480d12bE41d92F36f5f7bDd88212E381A3677#balances

LDO = "0x5A98FcBEA516Cf06857215779Fd812CA3beF1B32"
COW = "0xDEf1CA1fb7FBcDC777520aa7f396b4E015F497aB" ## Has pair with GNO and with WETH
GNO = "0x6810e776880C02933D47DB1b9fc05908e5386b96"

## Mostly Votium
CVX = "0x4e3FBD56CD56c3e72c1403e103b45Db9da5B9D2B"
WETH = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
SNX = "0xC011a73ee8576Fb46F5E1c5751cA3B9Fe0af2a6F"
TRIBE = "0xc7283b66Eb1EB5FB86327f08e1B5816b0720212B"
FLX = "0x6243d8cea23066d098a15582d81a598b4e8391f4"
INV = "0x41d5d79431a913c4ae7d69a668ecdfe5ff9dfb68"
FXS = "0x3432B6A60D23Ca0dFCa7761B7ab56459D9C964D0"

## More Random Votium stuff
TUSD = "0x0000000000085d4780B73119b644AE5ecd22b376"
STG = "0xAf5191B0De278C7286d6C7CC6ab6BB8A73bA2Cd6"
LYRA = "0x01BA67AAC7f75f647D94220Cc98FB30FCc5105Bf"
JPEG = "0xE80C0cd204D654CEbe8dd64A4857cAb6Be8345a3"
GRO = "0x3Ec8798B81485A254928B70CDA1cf0A2BB0B74D7"
EURS = "0xdB25f211AB05b1c97D595516F45794528a807ad8"

## New Aura Pools
DIGG = "0x798D1bE841a82a273720CE31c822C61a67a601C3"
GRAVI_AURA = "0xBA485b556399123261a5F9c95d413B4f93107407"

FUZZ_TOKEN_LIST = [
  (CVX, 18), ## CVX
  ("0x6B175474E89094C44Da98b954EedeAC495271d0F", 18), ## DAI
  (SPELL, 18), ## SPELL
  (ALCX, 18), ## ALCX
  ("0x7D1AfA7B718fb893dB30A3aBc0Cfc608AaCfeBB0", 18), ## MATIC
  (FXS, 18), ## FXS
  (LDO, 18), ## LDO
  (TRIBE, 18), ## TRIBE
  ("0x8207c1FfC5B6804F6024322CcF34F29c3541Ae26", 18), ## OGN
  ("0xa3BeD4E1c75D00fa6f4E5E6922DB7261B5E9AcD2", 18), ## MTA
  ("0x31429d1856aD1377A8A0079410B297e1a9e214c2", 18), ## ANGLE 
  ("0xCdF7028ceAB81fA0C6971208e83fa7872994beE5", 18), ## T
  (LFT, 18), ## LFT
  (FLX, 18), ## FLX
  (GRO, 18), ## GRO
  (STG, 18), ## STG
  ("0x674C6Ad92Fd080e4004b2312b45f796a192D27a0", 18), ## USDN
  ("0xFEEf77d3f69374f66429C91d732A244f074bdf74", 18), ## cvxFXS
  (INV, 18), ## INV
  (WETH, 18),
  (USDC, 6),
  (USDT, 6),
  (WBTC, 8),
  (AURA, 18),
  (AURA_BAL, 18),
  (BADGER, 18),
  ##(SD, 18), ## Not Supported -> Cannot fix at this time
  (DFX, 18),
  ##(FDT, 18), ## Not Supported -> Cannot fix at this time
  (COW, 18),
  (GNO, 18),
  (SNX, 18),

  ## More Coins
  (TUSD, 18),
  (LYRA, 18),
  (JPEG, 18),

  ## From new Balancer Pools
  (DIGG, 9),
  (GRAVI_AURA, 18)
]


### Sell token for Weth
@given(sell_token_num=strategy("uint256"), buy_token_num=strategy("uint256"))
def test_fuzz_quote_comparison(sell_token_num, buy_token_num, pm):
  
  sellTokenDecimal = FUZZ_TOKEN_LIST[sell_token_num % len(FUZZ_TOKEN_LIST)]
  sell_token = interface.ERC20(sellTokenDecimal[0])
  buyTokenDecimal = FUZZ_TOKEN_LIST[buy_token_num % len(FUZZ_TOKEN_LIST)]
  buy_token = interface.ERC20(buyTokenDecimal[0])
  
  if buy_token.address == sell_token.address:
     return True
     
  count = 10000
  if sell_token.address == interface.ERC20(WBTC).address or sell_token.address == interface.ERC20(DIGG).address:
     count = 1
  if sell_token.address == interface.ERC20(WETH).address:
     count = 10
  if sell_token.address == interface.ERC20(FLX).address or sell_token.address == interface.ERC20(INV).address or sell_token.address == interface.ERC20(GNO).address or sell_token.address == interface.ERC20(ALCX).address or sell_token.address == interface.ERC20(AURA_BAL).address:
     count = 100
  if sell_token.address == interface.ERC20(JPEG).address or sell_token.address == interface.ERC20(SPELL).address or sell_token.address == interface.ERC20(LFT).address:
     count = 1000000
     
  sell_amount = count * (10**sellTokenDecimal[1])

  #### FIXTURES ###
  
  univ3simulator = pm('rayeaster/on-chain-pricer@0.3').UniV3SwapSimulator.deploy({"from": accounts[0]})
  balancerV2Simulator = pm('rayeaster/on-chain-pricer@0.3').BalancerSwapSimulator.deploy({"from": accounts[0]})
  lenient_contract = pm('rayeaster/on-chain-pricer@0.3').OnChainPricingMainnetLenient.deploy(univ3simulator.address, balancerV2Simulator.address, {"from": accounts[0]})
  lenient_contract.setSlippage(499, {"from": accounts.at(lenient_contract.TECH_OPS(), force=True)})
    
  #### compare quote between cowswap and pricer
  #### coswap quote return (fee_amount, buy_amount_after_fee, sell_amount_after_fee)
  #### pricer quote return (SwapType, amountOut, pools, poolFees)
  print('sell ' + str(sell_amount) + ' ' + sell_token.address + ' FOR ' +  buy_token.address)
  quoteCowswap = get_cowswap_order_quote(sell_token, buy_token, sell_amount)
  assert quoteCowswap[0] + quoteCowswap[2] == sell_amount
  quotePricer = lenient_contract.findOptimalSwap(sell_token, buy_token, sell_amount)
  assert quoteCowswap[1] >= quotePricer[1]
    