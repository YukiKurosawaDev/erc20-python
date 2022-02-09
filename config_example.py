class Web3ClientConfig:
    @property
    def WEB3_RPC_URL(self)->str:
        return "https://rinkeby.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161"
    @property
    def WEB3_CHAIN_ID(self)->int:
        return 4
    @property
    def WEB3_CHAIN_NAME(self)->str:
        return "ETHEREUM 試験ネットワーク"

    @property
    def WEB3_EIP1159_COMPACTIBLE(self)->bool:
        return True

    @property
    def WALLET_PRIVATE_KEY(self)->str:
        return ""

    @property
    def V1_TRAN_TEST(self)->bool:
        return True
    
    @property
    def V2_TRAN_TEST(self)->bool:
        return True