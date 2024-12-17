from constructs import Construct
from cdktf_cdktf_provider_azurerm.provider import AzurermProvider
from dataclasses import dataclass, field
from cdktf_cdktf_provider_azurerm.storage_account import StorageAccount
from typing import Protocol
from cdktf_cdktf_provider_azurerm.storage_data_lake_gen2_filesystem import StorageDataLakeGen2Filesystem

class StorageAccountConfig(Protocol):
    id: str
    name: str
    resource_group_name: str
    location: str
    account_tier: str
    account_replication_type: str


@dataclass
class AzureStorageAccountConfig:
    id: str = field()
    name: str = field()
    resource_group_name: str = field()
    location: str = field()
    account_tier: str = field()
    account_replication_type: str = field()


class AzureStorageAccount(Construct):
    def __init__(
        self,
        scope: Construct,
        azure_provider: AzurermProvider,
        config: StorageAccountConfig,
    ):
        self._config = config
        self._azure_provider = azure_provider

        super().__init__(scope, self._config.id)

        # Create a storage account in the resource group
        self._storage_account = StorageAccount(
            scope=self,
            provider=self._azure_provider,
            id_=self._config.id,
            name=self._config.name,
            resource_group_name=self._config.resource_group_name,
            location=self._config.location,
            account_tier=self._config.account_tier,
            account_replication_type=self._config.account_replication_type,
        )

    @property
    def storage_account(self) -> StorageAccount:
        return self._storage_account


class StorageContainerConfig(Protocol):
    id: str
    name: str
    storage_account_id: str


@dataclass
class AzureStorageContainerConfig:
    id: str = field()
    name: str = field()
    storage_account_id: str = field()


class AzureStorageContainer(Construct):
    def __init__(
        self,
        scope: Construct,
        azure_provider: AzurermProvider,
        config: AzureStorageContainerConfig,
    ):
        self._config = config
        self._azure_provider = azure_provider

        super().__init__(scope, self._config.id)

        self._storage_container = StorageDataLakeGen2Filesystem(
            scope=self,
            provider=self._azure_provider,
            id_=self._config.id,
            name=self._config.name,
            storage_account_id=self._config.storage_account_id,
        )

    @property
    def storage_container(self) -> StorageDataLakeGen2Filesystem:
        return self._storage_container
