import sys
import os
import io
import re


class DashConfig:
    def __init__(self, filename):
        try:
            # read dash.conf config but skip commented lines
            f = io.open(filename)
            lines = []
            for line in f:
                if re.match('^\s*#', line):
                    continue
                lines.append(line)
            f.close()

            # data is dash.conf without commented lines
            self.data = ''.join(lines)
            match = re.findall(r'(.*?)=(.*?)$', self.data, re.MULTILINE)
            self.tokens = {key: value for (key, value) in match}
        except IOError as e:
            print("[warning] error reading config file: %s" % e)

        # strip keys in tokens
        for key in self.tokens.keys():
            if ' ' in key:
                self.tokens[key.replace(' ', '')] = self.tokens[key]
                del self.tokens[key]

    def is_mainnet(self):
        if not ('testnet' in self.tokens):
            return True
        return int(self.tokens['testnet']) == 0

    def get_rpc_creds(self):
        creds = {}
        if not ('rpchost' in self.tokens):
            creds[u'host'] = '127.0.0.1'
        else:
            creds[u'host'] = self.tokens['rpchost']
        # standard Dash defaults...
        default_port = 9998 if (self.is_mainnet()) else 19998
        if not ('rpcport' in self.tokens):
            creds[u'port'] = default_port
        else:
            creds[u'port'] = int(self.tokens['rpcport'])
        creds[u'user'] = self.tokens['rpcuser']
        creds[u'password'] = self.tokens['rpcpassword']

        # return a dictionary with RPC credential key, value pairs
        return creds

    @classmethod
    def get_default_dash_conf(cls):
        home = os.environ.get('HOME')

        dash_conf = os.path.join(home, ".dashcore/dash.conf")
        if sys.platform == 'darwin':
            dash_conf = os.path.join(home, "Library/Application Support/DashCore/dash.conf")

        return dash_conf
