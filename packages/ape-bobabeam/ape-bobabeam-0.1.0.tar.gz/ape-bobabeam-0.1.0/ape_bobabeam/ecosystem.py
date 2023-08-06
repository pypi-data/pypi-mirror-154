from ape.api.config import PluginConfig
from ape.api.networks import LOCAL_NETWORK_NAME
from ape_ethereum.ecosystem import Ethereum, NetworkConfig

NETWORKS = {
    # chain_id, network_id
    "bobabeam": (1294, 1294),
    "bobabase": (1297, 1297),
}


class BobabeamConfig(PluginConfig):
    bobabeam: NetworkConfig = NetworkConfig(required_confirmations=1, block_time=1)  # type: ignore
    bobabase: NetworkConfig = NetworkConfig(required_confirmations=1, block_time=1)  # type: ignore
    local: NetworkConfig = NetworkConfig(default_provider="test")  # type: ignore
    default_network: str = LOCAL_NETWORK_NAME


class Bobabeam(Ethereum):
    @property
    def config(self) -> BobabeamConfig:  # type: ignore
        return self.config_manager.get_config("bobabeam")  # type: ignore
