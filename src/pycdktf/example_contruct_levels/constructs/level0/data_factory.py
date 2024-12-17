from constructs import Construct
from cdktf_cdktf_provider_azurerm.provider import AzurermProvider
from dataclasses import dataclass, field
from typing import Protocol
from cdktf_cdktf_provider_azurerm.data_factory import DataFactory

class DataFactoryConfig(Protocol):
    id: str
    name: str
    resource_group_name: str
    location: str
    identity: dict[str, str]


@dataclass
class AzureDataFactoryConfig:
    id: str = field()
    name: str = field()
    resource_group_name: str = field()
    location: str = field()
    identity: dict[str, str] = field()


class AzureDataFactory(Construct):
    def __init__(
        self,
        scope: Construct,
        azure_provider: AzurermProvider,
        config: DataFactoryConfig,
    ):
        self._config = config
        self._azure_provider = azure_provider

        super().__init__(scope, self._config.id)

        # Create a storage account in the resource group
        self._data_factory = DataFactory(
            scope=self,
            provider=self._azure_provider,
            id_=self._config.id,
            name=self._config.name,
            resource_group_name=self._config.resource_group_name,
            location=self._config.location,
            identity=self._config.identity,
        )

    @property
    def data_factory(self) -> DataFactory:
        return self._data_factory
