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
    def TRAN_TEST(self)->bool:
        return False

    @property
    def V1_TRAN_TEST(self)->bool:
        return False
    
    @property
    def V2_TRAN_TEST(self)->bool:
        return False

    @property 
    def CONTRACT_TEST(self)->bool:
        return True
    
    @property
    def CONTRACT_DEPLOY_A(self)->bool:
        return False

    @property
    def CONTRACT_DEPLOY_B(self)->bool:
        return False

    @property
    def CONTRACT_DEPLOY_C(self)->bool:
        return False

    @property
    def CONTRACT_TRAN_TEST(self)->bool:
        return False;

    # コントラクト A の アドレス: 0xE891dAf43996985411D99574f9A5735213E3FA34
    # コントラクト B の アドレス: 0xC097f39C91B1282bB7396D73643c5D6BbebF882e
    # コントラクト C の アドレス: 0x794f1AECB84f3979569A485d5C7D6C8b14692B0a