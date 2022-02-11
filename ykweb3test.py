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
if config.TRAN_TEST:
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

if config.CONTRACT_TEST:
    if config.CONTRACT_DEPLOY_A:
        print_e("コントラクト A の ABI 読み込み中... ")
        with open ('contracts/CoinA.abi') as aa:
            abi=aa.read()
        print_e("完了\n")
        print_e("コントラクト A の BIN 読み込み中... ")
        with open ('contracts/CoinA.bin') as bb:
            bin=bb.read()
        print_e("完了\n")

        print_e("コントラクト A のコンストラクタ作成中... ")
        tx_a=w3.eth.contract(abi=abi,bytecode=bin).constructor().buildTransaction({"from":acc.address})
        print_e("完了\n")

        print_e("コントラクト A のコンストラクタ試験中... ")
        try:            
            tx_a["nonce"]=w3.eth.get_transaction_count(acc.address)
            gas=w3.eth.estimate_gas(tx_a)
            print_e("%s\n" % gas)
            tx_a["gas"]=gas
        except ValueError as e:
            print_e("失敗\n")
            print_e("エラー: コントラクト A のコンストラクタ 確認に失敗しました。\n")
            print_e(e)
            exit(1)

        print_e("コントラクト A のコンストラクタ署名中... ")
        signed=w3.eth.account.sign_transaction(tx_a, config.WALLET_PRIVATE_KEY)
        print_e("完了\n")

        print_e("コントラクト A のコンストラクタ送信中... ")
        hash_a=w3.eth.send_raw_transaction(signed.rawTransaction)
        print_e("完了\n")
        done=False
        while not done:
            try:
                TxRetA=w3.eth.get_transaction_receipt(w3.toHex(hash_a))
                ContractA=TxRetA["contractAddress"]
                print("コントラクト A の アドレス: %s" % ContractA)
                done=True
            except:
                done=False

    if config.CONTRACT_DEPLOY_B:
        print_e("コントラクト B の ABI 読み込み中... ")
        with open ('contracts/CoinB.abi') as aa:
            abi=aa.read()
        print_e("完了\n")
        print_e("コントラクト B の BIN 読み込み中... ")
        with open ('contracts/CoinB.bin') as bb:
            bin=bb.read()
        print_e("完了\n")

        print_e("コントラクト B のコンストラクタ作成中... ")
        tx_b=w3.eth.contract(abi=abi,bytecode=bin).constructor().buildTransaction({"from":acc.address})
        print_e("完了\n")

        print_e("コントラクト B のコンストラクタ試験中... ")
        try:            
            tx_b["nonce"]=w3.eth.get_transaction_count(acc.address)
            gas=w3.eth.estimate_gas(tx_b)
            print_e("%s\n" % gas)
            tx_b["gas"]=gas
        except ValueError as e:
            print_e("失敗\n")
            print_e("エラー: コントラクト B のコンストラクタ 確認に失敗しました。\n")
            print_e(e)
            exit(1)

        print_e("コントラクト B のコンストラクタ署名中... ")
        signed=w3.eth.account.sign_transaction(tx_b, config.WALLET_PRIVATE_KEY)
        print_e("完了\n")

        print_e("コントラクト B のコンストラクタ送信中... ")
        hash_b=w3.eth.send_raw_transaction(signed.rawTransaction)
        print_e("完了\n")
        done=False
        while not done:
            try:
                TxRetB=w3.eth.get_transaction_receipt(w3.toHex(hash_b))
                ContractB=TxRetB["contractAddress"]
                print("コントラクト B の アドレス: %s" % ContractB)
                done=True
            except:
                done=False

    if config.CONTRACT_DEPLOY_C:
        print_e("コントラクト C の ABI 読み込み中... ")
        with open ('contracts/CoinC.abi') as aa:
            abi=aa.read()
        print_e("完了\n")
        print_e("コントラクト C の BIN 読み込み中... ")
        with open ('contracts/CoinC.bin') as bb:
            bin=bb.read()
        print_e("完了\n")

        print_e("コントラクト C のコンストラクタ作成中... ")
        tx_c=w3.eth.contract(abi=abi,bytecode=bin).constructor().buildTransaction({"from":acc.address})
        print_e("完了\n")

        print_e("コントラクト C のコンストラクタ試験中... ")
        try:            
            tx_c["nonce"]=w3.eth.get_transaction_count(acc.address)
            gas=w3.eth.estimate_gas(tx_c)
            print_e("%s\n" % gas)
            tx_c["gas"]=gas
        except ValueError as e:
            print_e("失敗\n")
            print_e("エラー: コントラクト C のコンストラクタ 確認に失敗しました。\n")
            print_e(e)
            exit(1)

        print_e("コントラクト C のコンストラクタ署名中... ")
        signed=w3.eth.account.sign_transaction(tx_c, config.WALLET_PRIVATE_KEY)
        print_e("完了\n")

        print_e("コントラクト C のコンストラクタ送信中... ")
        hash_c=w3.eth.send_raw_transaction(signed.rawTransaction)
        print_e("完了\n")
        done=False
        while not done:
            try:
                TxRetC=w3.eth.get_transaction_receipt(w3.toHex(hash_c))
                ContractC=TxRetC["contractAddress"]
                print("コントラクト C の アドレス: %s" % ContractC)
                done=True
            except:
                done=False

    if config.CONTRACT_TRAN_TEST:
        print_e("コントラクト A のトランザクション作成中... ")
        tx_tran=w3.eth.contract(address=ContractA, abi=abi).functions.transfer(acc.address, w3.toWei(1, 'ether')).buildTransaction({"from":acc.address});
        print_e("完了\n")

        print_e("コントラクト A のトランザクション試験中... ")        
        tx_tran["nonce"]=w3.eth.get_transaction_count(acc.address)
        gas=w3.eth.estimate_gas(tx_tran)        
        tx_tran["gas"]=gas
        print_e("%s\n" % gas)

        print_e("コントラクト A のトランザクション署名中... ")
        signed_tran=w3.eth.account.sign_transaction(tx_tran, config.WALLET_PRIVATE_KEY)
        print_e("完了\n")

        print_e("コントラクト A のトランザクション送信中... ")
        hash_tran=w3.eth.send_raw_transaction(signed_tran.rawTransaction)
        print_e("完了\n")
        done=False
        while not done:
            try:
                TxTranRet=w3.eth.get_transaction_receipt(w3.toHex(hash_tran))
                done=True
            except:
                done=False