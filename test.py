from web3 import Web3
from eth_account import Account

# Подключение к Arbitrum RPC
arbitrum_rpc_url = 'https://arb1.arbitrum.io/rpc'
w3 = Web3(Web3.HTTPProvider(arbitrum_rpc_url))

assert w3.is_connected()


new_account = Account.create()
private_key = new_account._private_key.hex()
public_key = new_account.address

print(f"Новый адрес: {public_key}")
print(f"Приватный ключ: {private_key}")


def get_balance(address):
    balance = w3.eth.get_balance(address)
    return w3.from_wei(balance, 'ether')


balance = get_balance(public_key)
print(f"Баланс на Arbitrum: {balance} ETH")