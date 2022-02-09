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

if config.V1_TRAN_TEST:
    print_e("トランザクション V1 作成中... ")
    Txv1Obj={
        "nonce":w3.eth.get_transaction_count(acc.address),
        "gas":w3.toWei(1000000, 'gwei'),
        "gasPrice":w3.eth.gas_price,
        "to":acc.address,
        "from":acc.address,
        "value":w3.toWei(1, 'gwei'),
        "data":b'',
    }
    print_e("完了\n")

    print_e("トランザクション V1 試験中... ")
    try:
        TxV1Gas=w3.eth.estimate_gas(Txv1Obj);
        Txv1Obj["gas"]=TxV1Gas
        print_e("%s\n" % TxV1Gas)
    except ValueError as e:
        print_e("失敗\n")
        print_e("エラー: トランザクション V1 確認に失敗しました。\n")
        print_e(e)
        exit(1)
    
    print_e("トランザクション V1 署名中... ")
    TxV1Signed=w3.eth.account.sign_transaction(Txv1Obj, config.WALLET_PRIVATE_KEY)
    print_e("完了\n")

    print_e("トランザクション V1 送信中... ")
    #try:
    TxV1=w3.eth.send_raw_transaction(TxV1Signed.rawTransaction)
    print_e("完了\n")
    print_e("トランザクション V1 ID: " + w3.toHex(TxV1) + "\n")

    print_e("トランザクション V1 確認中... ")
    done=False
    while not done:
        try:
            TxV1Ret=w3.eth.get_transaction_receipt(w3.toHex(TxV1))
            done=True
        except:
            done=False

    print_e("完了\n")

print_e("\n")
print_e("EIP1159テストは実施します... ")
if (not config.WEB3_EIP1159_COMPACTIBLE) or (not config.V2_TRAN_TEST):
    print_e("いいえ\n")
else:
    print_e("はい\n")
    print_e("トランザクション V2 作成中... ")
    base_fee=w3.eth.get_block(w3.eth.get_block_number()).baseFeePerGas
    Txv1Obj={
        "nonce":w3.eth.get_transaction_count(acc.address),
        "gas":w3.toWei(1000000, 'gwei'),
        "maxFeePerGas":w3.eth.max_priority_fee+base_fee,
        "maxPriorityFeePerGas":w3.eth.max_priority_fee,
        "to":acc.address,
        "from":acc.address,
        "value":w3.toWei(1, 'gwei'),
        "data":b'',
        "chainId":config.WEB3_CHAIN_ID,

    }
    print_e("完了\n")

    print_e("トランザクション V2 試験中... ")
    try:
        TxV1Gas=w3.eth.estimate_gas(Txv1Obj);
        Txv1Obj["gas"]=TxV1Gas
        print_e("%s\n" % TxV1Gas)
    except ValueError as e:
        print_e("失敗\n")
        print_e("エラー: トランザクション V2 確認に失敗しました。\n")
        print_e(e)
        exit(1)
    
    print_e("トランザクション V2 署名中... ")
    TxV1Signed=w3.eth.account.sign_transaction(Txv1Obj, config.WALLET_PRIVATE_KEY)
    print_e("完了\n")

    print_e("トランザクション V2 送信中... ")
    #try:
    TxV1=w3.eth.send_raw_transaction(TxV1Signed.rawTransaction)
    print_e("完了\n")
    print_e("トランザクション V2 ID: " + w3.toHex(TxV1) + "\n")

    print_e("トランザクション V2 確認中... ")
    done=False
    while not done:
        try:
            TxV1Ret=w3.eth.get_transaction_receipt(w3.toHex(TxV1))
            done=True
        except:
            done=False

    print_e("完了\n")

