from ape.api.config import PluginConfig
from ape.api.networks import LOCAL_NETWORK_NAME
from ape_ethereum.ecosystem import Ethereum, NetworkConfig

NETWORKS = {
    # chain_id, network_id
    "mainnet": (1313161554, 1313161554),
    "testnet": (1313161555, 1313161555),
}


class AuroraConfig(PluginConfig):
    mainnet: NetworkConfig = NetworkConfig(required_confirmations=1, block_time=2)  # type: ignore
    testnet: NetworkConfig = NetworkConfig(required_confirmations=1, block_time=2)  # type: ignore
    local: NetworkConfig = NetworkConfig(default_provider="test")  # type: ignore
    default_network: str = LOCAL_NETWORK_NAME


class Aurora(Ethereum):
    @property
    def config(self) -> AuroraConfig:  # type: ignore
        return self.config_manager.get_config("aurora")  # type: ignore