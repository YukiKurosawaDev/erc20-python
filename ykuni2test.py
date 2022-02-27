import time
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

try:
    print_e("Uniswap の設定読み込み中... ")
    from uniconfig import Web3UniswapConfig
    uniconfig=Web3UniswapConfig()
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

print_e("コントラクト A の ABI 読み込み中... ")
with open ('contracts/CoinA.abi') as aa:
    ABI_CoinA=aa.read()
    CoinA=w3.eth.contract(address=uniconfig.CONTRACT_A, abi=ABI_CoinA)
print_e("完了\n")

print_e("コントラクト B の ABI 読み込み中... ")
with open ('contracts/CoinB.abi') as ab:
    ABI_CoinB=ab.read()
    CoinB=w3.eth.contract(address=uniconfig.CONTRACT_B, abi=ABI_CoinB)
print_e("完了\n")

print_e("コントラクト C の ABI 読み込み中... ")
with open ('contracts/CoinC.abi') as ac:
    ABI_CoinC=ac.read()
    CoinC=w3.eth.contract(address=uniconfig.CONTRACT_C, abi=ABI_CoinC)
print_e("完了\n")

print_e("コントラクト UniswapV2Factory の ABI 読み込み中... ")
with open("uni-core/UniswapV2Factory.abi") as uni_factory:
    ABI_UniswapV2Factory=uni_factory.read()
    UniswapV2Factory=w3.eth.contract(address=uniconfig.UNISWAP_FACTORY, abi=ABI_UniswapV2Factory)
print_e("完了\n")

print_e("コントラクト UniswapV2Router02 の ABI 読み込み中... ")
with open("uni-periphery/UniswapV2Router02.abi") as uni_router:
    ABI_UniswapV2Router02=uni_router.read()
    UniswapV2Router02=w3.eth.contract(address=uniconfig.UNISWAP_ROUTER, abi=ABI_UniswapV2Router02)
print_e("完了\n")

if uniconfig.APPROVE_A:
    print_e("コントラクト A のトランザクション作成中... ")
    tx_a_approve=CoinA.functions.approve(uniconfig.UNISWAP_ROUTER,w3.toWei(1000,"ether")).buildTransaction({'from':acc.address})
    print_e("完了\n")

    print_e("コントラクト A のトランザクション試験中... ")        
    tx_a_approve["nonce"]=w3.eth.get_transaction_count(acc.address)
    gas=w3.eth.estimate_gas(tx_a_approve)        
    tx_a_approve["gas"]=gas
    print_e("%s\n" % gas)

    print_e("コントラクト A のトランザクション署名中... ")
    signed_tran=w3.eth.account.sign_transaction(tx_a_approve, config.WALLET_PRIVATE_KEY)
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

if uniconfig.APPROVE_B:
    print_e("コントラクト B のトランザクション作成中... ")
    tx_b_approve=CoinB.functions.approve(uniconfig.UNISWAP_ROUTER,w3.toWei(1000,"ether")).buildTransaction({'from':acc.address})
    print_e("完了\n")

    print_e("コントラクト B のトランザクション試験中... ")        
    tx_b_approve["nonce"]=w3.eth.get_transaction_count(acc.address)
    gas=w3.eth.estimate_gas(tx_b_approve)        
    tx_b_approve["gas"]=gas
    print_e("%s\n" % gas)

    print_e("コントラクト B のトランザクション署名中... ")
    signed_tran=w3.eth.account.sign_transaction(tx_b_approve, config.WALLET_PRIVATE_KEY)
    print_e("完了\n")

    print_e("コントラクト B のトランザクション送信中... ")
    hash_tran=w3.eth.send_raw_transaction(signed_tran.rawTransaction)
    print_e("完了\n")
    done=False
    while not done:
        try:
            TxTranRet=w3.eth.get_transaction_receipt(w3.toHex(hash_tran))
            done=True
        except:
            done=False

if uniconfig.APPROVE_C:
    print_e("コントラクト C のトランザクション作成中... ")
    tx_c_approve=CoinC.functions.approve(uniconfig.UNISWAP_ROUTER,w3.toWei(1000,"ether")).buildTransaction({'from':acc.address})
    print_e("完了\n")

    print_e("コントラクト C のトランザクション試験中... ")        
    tx_c_approve["nonce"]=w3.eth.get_transaction_count(acc.address)
    gas=w3.eth.estimate_gas(tx_c_approve)        
    tx_c_approve["gas"]=gas
    print_e("%s\n" % gas)

    print_e("コントラクト C のトランザクション署名中... ")
    signed_tran=w3.eth.account.sign_transaction(tx_c_approve, config.WALLET_PRIVATE_KEY)
    print_e("完了\n")

    print_e("コントラクト C のトランザクション送信中... ")
    hash_tran=w3.eth.send_raw_transaction(signed_tran.rawTransaction)
    print_e("完了\n")
    done=False
    while not done:
        try:
            TxTranRet=w3.eth.get_transaction_receipt(w3.toHex(hash_tran))
            done=True
        except:
            done=False

print_e("コントラクト A のペアアドレス 読み込み中... ")
Pair_WETH_A=UniswapV2Factory.functions.getPair(uniconfig.UNISWAP_WETH,uniconfig.CONTRACT_A).call();
print_e("コントラクト A のペアアドレス: " + Pair_WETH_A + "\n")

if Pair_WETH_A == uniconfig.NULLPTR:
    print_e("ペア WETH/A は存在しません。\n")
    
if uniconfig.ADD_A_WETH:
    print_e("コントラクト A の WETH/A 作成中... ")
    tx_a_weth_add=UniswapV2Router02.functions.addLiquidityETH(
        uniconfig.CONTRACT_A,
        w3.toWei(100,"ether"),
        0,
        w3.toWei(1,"ether"),
        acc.address,
        int(time.time())+600
        ).buildTransaction({'from':acc.address, 'value':w3.toWei(1,"ether")})
    print_e("完了\n")

    print_e("コントラクト A の WETH/A 試験中... ")        
    tx_a_weth_add["nonce"]=w3.eth.get_transaction_count(acc.address)
    gas=w3.eth.estimate_gas(tx_a_weth_add)        
    tx_a_weth_add["gas"]=gas
    print_e("%s\n" % gas)

    print_e("コントラクト A の WETH/A 署名中... ")
    signed_tran=w3.eth.account.sign_transaction(tx_a_weth_add, config.WALLET_PRIVATE_KEY)
    print_e("完了\n")

    print_e("コントラクト A の WETH/A 送信中... ")
    hash_tran=w3.eth.send_raw_transaction(signed_tran.rawTransaction)
    print_e("完了\n")
    done=False
    while not done:
        try:
            TxTranRet=w3.eth.get_transaction_receipt(w3.toHex(hash_tran))
            done=True
        except:
            done=False