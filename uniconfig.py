class Web3UniswapConfig:
    @property
    def CONTRACT_A(self)->str:
        return "0xE891dAf43996985411D99574f9A5735213E3FA34"
    
    @property
    def CONTRACT_B(self)->str:
        return "0xC097f39C91B1282bB7396D73643c5D6BbebF882e"

    @property
    def CONTRACT_C(self)->str:
        return "0x794f1AECB84f3979569A485d5C7D6C8b14692B0a"

    @property
    def UNISWAP_ROUTER(self)->str:
        return "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"

    @property
    def UNISWAP_FACTORY(self)->str:
        return "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f"

    @property
    def UNISWAP_WETH(self)->str:
        return "0xc778417E063141139Fce010982780140Aa0cD5Ab"

    @property
    def NULLPTR(self)->str:
        return "0x0000000000000000000000000000000000000000"

    @property
    def APPROVE_A(self)->bool:
        return False

    @property
    def APPROVE_B(self)->bool:
        return False

    @property
    def APPROVE_C(self)->bool:
        return False

    @property
    def ADD_A_WETH(self)->bool:
        return False