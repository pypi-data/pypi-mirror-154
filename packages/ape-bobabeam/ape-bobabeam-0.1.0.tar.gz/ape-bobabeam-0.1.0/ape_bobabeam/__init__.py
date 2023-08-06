from ape import plugins
from ape.api import NetworkAPI, create_network_type
from ape.api.networks import LOCAL_NETWORK_NAME
from ape_geth import GethProvider
from ape_test import LocalProvider

from .ecosystem import NETWORKS, Bobabeam, BobabeamConfig


@plugins.register(plugins.Config)
def config_class():
    return BobabeamConfig


@plugins.register(plugins.EcosystemPlugin)
def ecosystems():
    yield Bobabeam


@plugins.register(plugins.NetworkPlugin)
def networks():
    for network_name, network_params in NETWORKS.items():
        yield "bobabeam", network_name, create_network_type(*network_params)

    # NOTE: This works for development providers, as they get chain_id from themselves
    yield "bobabeam", LOCAL_NETWORK_NAME, NetworkAPI
    yield "bobabeam", "bobabeam-fork", NetworkAPI


@plugins.register(plugins.ProviderPlugin)
def providers():
    for network_name in NETWORKS:
        yield "bobabeam", network_name, GethProvider

    yield "bobabeam", LOCAL_NETWORK_NAME, LocalProvider
