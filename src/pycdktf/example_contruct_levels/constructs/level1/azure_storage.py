from constructs import Construct
from cdktf_cdktf_provider_azurerm.provider import AzurermProvider
from dataclasses import dataclass, field
from pycdktf.example_contruct_levels.constructs.level0.azure_storage import AzureStorageAccount, AzureStorageAccountConfig, AzureStorageContainer, AzureStorageContainerConfig, StorageAccountConfig, StorageContainerConfig
import warnings
from cdktf_cdktf_provider_azurerm.storage_account import StorageAccount
from cdktf_cdktf_provider_azurerm.storage_data_lake_gen2_filesystem import StorageDataLakeGen2Filesystem

@dataclass
class MyCustomAzureStorageAccountConfig(AzureStorageAccountConfig):
    def __post_init__(self):
        self.check_account_replication_type()

    def check_account_replication_type(self) -> None:
        if self.account_replication_type != "LRS":
            self.account_replication_type = "LRS"
            warnings.warn(f"account_replication_type is set to {self.account_replication_type} but only LRS is allowed. Modified to {self.account_replication_type}")


@dataclass
class MyCustomAzureStorageContainerConfig(AzureStorageContainerConfig):
    def __post_init__(self):
        self.check_storage_container_name_starts_with()

    def check_storage_container_name_starts_with(self):
        prefix: str = "rs"
        if not self.name.startswith(prefix):
            self.name = f"{prefix}{self.name}"
            warnings.warn(f"storage container name doesnt start with {prefix}. Modified to {self.name}")


class MyCustomAzureStorageAccount(Construct):
    _containers: list[str] = []

    def __init__(
        self,
        scope: Construct,
        id: str,
        azure_provider: AzurermProvider,
        config: StorageAccountConfig,
    ):
        self._id = id
        self._azure_provider = azure_provider
        self._config = config

        super().__init__(scope, self._id)

        self.storage_account: StorageAccount = AzureStorageAccount(
            scope=self,
            azure_provider=azure_provider,
            config=self._config
        ).storage_account

    @property
    def containers(self) -> list[str]:
        return self._containers

    def create_container(self, name: str):
        container_config: MyCustomAzureStorageContainerConfig = MyCustomAzureStorageContainerConfig(
            id=f"AzureContainer{name}",
            name=name,
            storage_account_id=self.storage_account.id
        )
        container: StorageDataLakeGen2Filesystem = AzureStorageContainer(
            scope=self,
            azure_provider=self._azure_provider,
            config=container_config,
        )
        self._containers.append(container)
