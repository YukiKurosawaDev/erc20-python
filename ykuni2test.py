from web3 import Web3
from web3.middleware import geth_poa_middleware
import math
from common import print_e

try:
    print_e("設定読み込み中... ")
    from config import Web3ClientConfig
    config=Web3ClientConfig()
    print_e("完了\n")
except:
    print_e("失敗\n")
    print_e("エラー: config.py が存在しません。\n")
    print_e("プログラムを終了します。\n")
    exit(1)

print_e("ネットワーク接続中... ")
w3=Web3(Web3.HTTPProvider(config.WEB3_RPC_URL))
if w3.isConnected():
    print_e("完了\n")
else:
    print_e("失敗\n")
    print_e("エラー: 接続に失敗しました。\n")
    print_e("プログラムを終了します。\n")
    exit(1)

print_e("POAミドルウェアを設定中... ")
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
print_e("完了\n")

print_e("アカウント情報を取得中... ")
acc=w3.eth.account.privateKeyToAccount(config.WALLET_PRIVATE_KEY)
print_e("完了\n")
print_e("アカウント名: " + acc.address + "\n")

print_e("残高照会中... ")
balance=w3.eth.getBalance(acc.address)
print_e("完了\n")
print_e("残高: %.5f ETH\n" % (balance/math.pow(10,18)))

