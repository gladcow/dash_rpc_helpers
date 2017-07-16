#!/usr/bin/env python
from dash_config import DashConfig
from dashd_api import DashdApi


# send trx with zero fee
def send_zero_fee_trx(address_to,  amount):
    dashd = DashdApi.from_dash_conf(DashConfig.get_default_dash_conf())

    unspent = dashd.get_unspent_amount()
    if len(unspent) == 0:
        raise Exception("No unspent inputs")
    address_from = unspent[0]["address"]
    tx_in = unspent[0]["txid"]
    vin = unspent[0]["vout"]
    full_amount = float(unspent[0]["amount"])
    change = full_amount - amount
    raw_trx = dashd.create_raw_trx(tx_in, vin, amount, address_to, change, address_from)
    signed = dashd.sign_raw_trx(raw_trx)
    tx_id = dashd.send_raw_trx(signed)

    print tx_id


send_zero_fee_trx("ye5F5rfx44YqvqCpVvi1SfFS4dvqaqyuDr", 1.0)
