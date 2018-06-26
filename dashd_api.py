"""
dashd JSONRPC interface
"""

from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException


class DashdApi():
    def __init__(self, **kwargs):
        host = kwargs.get('host')
        user = kwargs.get('user')
        password = kwargs.get('password')
        port = kwargs.get('port')

        self.creds = (user, password, host, port)

    @property
    def rpc_connection(self):
        return AuthServiceProxy("http://{0}:{1}@{2}:{3}".format(*self.creds))

    @classmethod
    def from_dash_conf(self, dash_dot_conf):
        from dash_config import DashConfig
        config = DashConfig(DashConfig.get_default_dash_conf())
        creds = config.get_rpc_creds()
        return self(**creds)

    def rpc_command(self, *params):
        return self.rpc_connection.__getattr__(params[0])(*params[1:])

    def get_unspent_amount(self):
        return self.rpc_command("listunspent")

    def create_raw_trx(self, tx_in, vin, amount, address_to, change, change_address):
        in_entry = {}
        in_entry["vout"] = vin
        in_entry["txid"] = tx_in
        inputs = [in_entry]
        outputs = {}
        outputs[address_to] = amount
        outputs[change_address] = change
        return self.rpc_command("createrawtransaction", inputs, outputs)

    def sign_raw_trx(self, raw_trx):
        signed = self.rpc_command("signrawtransaction", raw_trx)
        return signed["hex"]

    def send_raw_trx(self, signed):
        return self.rpc_command("sendrawtransaction", signed)

    # send instant send trx
    def instant_send(self, address_to, amount):
        return self.rpc_command("instantsendtoaddress", address_to, amount)

    # set IX lock for transaction
    def locktransaction(self, trx_id):
        return self.rpc_command("locktransaction", trx_id)