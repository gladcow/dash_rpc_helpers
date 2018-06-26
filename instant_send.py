#!/usr/bin/env python
from dash_config import DashConfig
from dashd_api import DashdApi


def instant_send_block():
    dashd = DashdApi.from_dash_conf(DashConfig.get_default_dash_conf())

    for i in range(0, 3):
        tx_id = dashd.instant_send("ye5F5rfx44YqvqCpVvi1SfFS4dvqaqyuDr", 0.1)
        print(tx_id)


instant_send_block()
