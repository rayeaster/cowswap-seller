import brownie
from brownie import *
import pytest

from scripts.send_order import get_cowswap_order

"""
    Verify order
    Place order
"""

def test_verify_and_add_order(seller, usdc, weth, manager):
  sell_amount = 1000000000000000000

  ## TODO Use the Hash Map here to verify it
  order_details = get_cowswap_order(seller, weth, usdc, sell_amount)

  data = order_details.order_data
  uid = order_details.order_uid

  ## Verify that the ID Matches
  assert uid == seller.getOrderID(data)

  ## Verify that the quote is better than what we could do
  assert seller.checkCowswapOrder(data, uid)

  ## Place the order
  ## Get settlement here and check
  seller.initiateCowswapOrder(data, uid, {"from": manager})

  settlement = interface.ICowSettlement(seller.SETTLEMENT())

  assert settlement.preSignature(uid) > 0

"""
    Cowswap RELAYER approval amount override issue found by watchpug audit 
    https://www.hacknote.co/17c261f7d8fWbdml/doc/182cf5567f8Gdn7B#182cf5567f8Gdn7B
"""
@pytest.mark.skip(reason="existing deployed version will override")
def test_approval_override(seller_v_0_3_deployed, usdc, weth, wbtc, seller_v_0_3_deployed_manager):
  sell_amount = 500 * 1000000000000000000
  settlement = interface.ICowSettlement(seller_v_0_3_deployed.SETTLEMENT())

  ## First order to setup inital approval to Cowswap relayer 
  order_details = get_cowswap_order(seller_v_0_3_deployed, weth, usdc, sell_amount)
  data = order_details.order_data
  uid = order_details.order_uid
  assert uid == seller_v_0_3_deployed.getOrderID(data)
  seller_v_0_3_deployed.initiateCowswapOrder(data, uid, {"from": seller_v_0_3_deployed_manager})
  assert settlement.preSignature(uid) > 0
  assert weth.allowance(seller_v_0_3_deployed.address, seller_v_0_3_deployed.RELAYER()) == sell_amount

  ## Second order to override smaller approval to Cowswap relayer 
  sell_amount2 = 100 * 1000000000000000000
  order_details2 = get_cowswap_order(seller_v_0_3_deployed, weth, wbtc, sell_amount2)
  data2 = order_details2.order_data
  uid2 = order_details2.order_uid
  assert uid2 == seller_v_0_3_deployed.getOrderID(data2)
  seller_v_0_3_deployed.initiateCowswapOrder(data2, uid2, {"from": seller_v_0_3_deployed_manager})
  assert settlement.preSignature(uid2) > 0
  
  ## According to Cowswap relayer code, the first order will fail to be filled due to insufficient allowance to transfer sell_token
  ## https://etherscan.io/address/0xc92e8bdf79f0507f65a392b0ab4667716bfe0110#code#F15#L112  
  assert weth.allowance(seller_v_0_3_deployed.address, seller_v_0_3_deployed.RELAYER()) == sell_amount2
  
def test_approval_override_fix(seller, usdc, weth, wbtc, manager):
  sell_amount = 500 * 1000000000000000000
  settlement = interface.ICowSettlement(seller.SETTLEMENT())

  ## First order to setup inital approval to Cowswap relayer 
  order_details = get_cowswap_order(seller, weth, usdc, sell_amount)
  data = order_details.order_data
  uid = order_details.order_uid
  assert uid == seller.getOrderID(data)
  seller.initiateCowswapOrder(data, uid, {"from": manager})
  assert settlement.preSignature(uid) > 0
  assert weth.allowance(seller.address, seller.RELAYER()) == sell_amount

  ## Second order to override smaller approval to Cowswap relayer 
  sell_amount2 = 100 * 1000000000000000000
  order_details2 = get_cowswap_order(seller, weth, wbtc, sell_amount2)
  data2 = order_details2.order_data
  uid2 = order_details2.order_uid
  assert uid2 == seller.getOrderID(data2)
  seller.initiateCowswapOrder(data2, uid2, {"from": manager})
  assert settlement.preSignature(uid2) > 0
  
  assert weth.allowance(seller.address, seller.RELAYER()) == sell_amount2 + sell_amount
  
  

