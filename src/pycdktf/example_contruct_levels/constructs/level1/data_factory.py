from cdktf_cdktf_provider_azurerm.provider import AzurermProvider
from dataclasses import dataclass, field
from cdktf_cdktf_provider_azurerm.data_factory import DataFactory
from constructs import Construct
from pycdktf.example_contruct_levels.constructs.level0.azure_storage import AzureStorageAccount, AzureStorageAccountConfig, AzureStorageContainer, AzureStorageContainerConfig, StorageAccountConfig, StorageContainerConfig
import warnings
from cdktf_cdktf_provider_azurerm.storage_account import StorageAccount
from cdktf_cdktf_provider_azurerm.storage_data_lake_gen2_filesystem import StorageDataLakeGen2Filesystem

from pycdktf.example_contruct_levels.constructs.level0.data_factory import AzureDataFactory, AzureDataFactoryConfig, DataFactoryConfig

class InvalidIdentity(Exception):
    """Raised when identity doesnt comply to desired value."""


@dataclass
class MyCustomAzureDataFactoryConfig(AzureDataFactoryConfig):
    def __post_init__(self):
        self.check_identity_is_system_assigned()

    def check_identity_is_system_assigned(self) -> None:
        if self.identity.get("type") != "SystemAssigned":
            raise InvalidIdentity(
                f"{self.identity} is not correctly set to SystemAssigned"
            )


class MyCustomAzureDataFactory(Construct):
    def __init__(
        self,
        scope: Construct,
        id: str,
        azure_provider: AzurermProvider,
        config: DataFactoryConfig,
    ):
        self._id = id
        self._azure_provider = azure_provider
        self._config = config

        super().__init__(scope, self._id)

        self._data_factory: DataFactory = AzureDataFactory(
            scope=self,
            azure_provider=azure_provider,
            config=self._config
        ).data_factory

    @property
    def data_factory(self) -> DataFactory:
        return self._data_factory
