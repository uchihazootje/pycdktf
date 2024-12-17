from constructs import Construct
from cdktf_cdktf_provider_azurerm.provider import AzurermProvider
from dataclasses import dataclass, field

from pycdktf.example_contruct_levels.constructs.level1.azure_storage import MyCustomAzureStorageAccount, MyCustomAzureStorageAccountConfig
from pycdktf.example_contruct_levels.constructs.level1.data_factory import MyCustomAzureDataFactory, MyCustomAzureDataFactoryConfig

@dataclass
class AzureDataFactorySolutionConfig:
    resource_group_name: str = field()
    location: str = field()
    containers: list[str] = field()


class AzureDataFactorySolution(Construct):
    def __init__(
        self,
        scope: Construct,
        id: str,
        azure_provider: AzurermProvider,
        config: AzureDataFactorySolutionConfig,
    ):
        self._id = id
        self._config = config
        self._azure_provider = azure_provider

        super().__init__(scope, self._id)

        # Deploy Storage Account solution
        custom_azure_storage_config: MyCustomAzureStorageAccountConfig = MyCustomAzureStorageAccountConfig(
            id="MyStorageAccount",
            name="rsconlevelsadls",
            resource_group_name=self._config.resource_group_name,
            location=self._config.location,
            account_tier="Standard",
            account_replication_type="GRS",
        )

        self.storage_account = MyCustomAzureStorageAccount(
            scope=self,
            id="CustomStorageAccountSolution",
            azure_provider=self._azure_provider,
            config=custom_azure_storage_config,
        )

        # Create containers
        for container in self._config.containers:
            self.storage_account.create_container(name=container)

        # Deploy Data Factory
        custom_data_factory_config: MyCustomAzureDataFactoryConfig = MyCustomAzureDataFactoryConfig(
            id="MyDataFactory",
            name="myrsconlevelsadf",
            resource_group_name=self._config.resource_group_name,
            location=self._config.location,
            identity={"type": "SystemAssigned"},
        )
        self.data_factory = MyCustomAzureDataFactory(
            scope=self,
            id="CustomAzureDataFactorySolution",
            azure_provider=self._azure_provider,
            config=custom_data_factory_config,
        )
