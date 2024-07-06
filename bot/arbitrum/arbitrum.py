from web3 import Web3
import json
from eth_keys import keys
from web3.middleware import geth_poa_middleware
from web3.exceptions import InvalidAddress
from bot.core.crud import create_user


arbitrum_url = "https://arb1.arbitrum.io/rpc"
web3 = Web3(Web3.HTTPProvider(arbitrum_url))
web3.eth.account.enable_unaudited_hdwallet_features()
web3.middleware_onion.inject(geth_poa_middleware, layer=0)


try:
    web3.is_connected()
except Exception:
    Exception("Failed to connect to the Arbitrum network")

erc20_abi = json.loads("""
[
    {
        "constant":true,
        "inputs":[{"name":"_owner","type":"address"}],
        "name":"balanceOf",
        "outputs":[{"name":"balance","type":"uint256"}],
        "type":"function"
    },
    {
        "constant":false,
        "inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],
        "name":"transfer",
        "outputs":[{"name":"success","type":"bool"}],
        "type":"function"
    }
]
""")


async def create_wallet(user_id, six_code):
    mnemonic = web3.eth.account.create_with_mnemonic()[1]
    account = web3.eth.account.from_mnemonic(mnemonic)
    private_key = account.key.hex()
    address = account.address
    eth_private_key = keys.PrivateKey(bytes.fromhex(private_key[2:]))
    public_key = eth_private_key.public_key.to_hex()
    await create_user(
        six_code=six_code,
        user_id=user_id,
        seed_phrase=mnemonic,
        private_key=private_key,
        address=address,
        public_key=public_key,
    )
    return address, mnemonic


async def arb_get_balanse(address, currency):
    try:
        balance = web3.eth.get_balance(address)
        return web3.from_wei(balance, currency)
    except InvalidAddress:
        return None


async def send_currency(sender_address, recipient_address, private_key, amount):
    nonce = web3.eth.get_transaction_count(sender_address)
    tx = {
        'nonce': nonce,
        'to': recipient_address,
        'value': web3.to_wei(amount, 'ether'),
        'gas': 21000,
        'gasPrice': web3.to_wei('50', 'gwei')
    }
    signed_tx = web3.eth.account.signTransaction(tx, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    return f"Transaction sent! TX Hash: {tx_hash.hex()}"
