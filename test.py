from web3 import Web3
from eth_account import Account
from web3.exceptions import InvalidAddress
# Подключение к Arbitrum RPC
arbitrum_rpc_url = 'https://arb1.arbitrum.io/rpc'
w3 = Web3(Web3.HTTPProvider(arbitrum_rpc_url))

assert w3.is_connected()


def get_balance(address):
    try:
        balance = w3.eth.get_balance(address)
        return w3.from_wei(balance, 'ether')
    except InvalidAddress:
        return None


def get_address(address):
    return w3.is_address(address)


print(get_balance('0xfea3192FC12C9bd72415B62E12eC7F82'))