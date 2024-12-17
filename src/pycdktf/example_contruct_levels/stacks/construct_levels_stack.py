from cdktf import AzurermBackend, TerraformStack
from constructs import Construct
from cdktf_cdktf_provider_azurerm.provider import AzurermProvider
from cdktf_cdktf_provider_azurerm.resource_group import ResourceGroup
from pycdktf.example_contruct_levels.constructs.level1.azure_storage import MyCustomAzureStorageAccount, MyCustomAzureStorageAccountConfig
from pycdktf.example_contruct_levels.constructs.level1.data_factory import MyCustomAzureDataFactory, MyCustomAzureDataFactoryConfig
from pycdktf.example_contruct_levels.constructs.level2.azure_data_factory_solution import AzureDataFactorySolution, AzureDataFactorySolutionConfig
from pycdktf.settings import TerraformAzureStorageBackendSetting, TerraformStackSettings
from cdktf_cdktf_provider_azurerm.storage_account import StorageAccount
from cdktf_cdktf_provider_azurerm.storage_data_lake_gen2_filesystem import StorageDataLakeGen2Filesystem
from cdktf_cdktf_provider_azurerm.data_factory import DataFactory
from cdktf_cdktf_provider_azurerm.data_azurerm_data_factory import DataAzurermDataFactory
from cdktf_cdktf_provider_azurerm.role_assignment import RoleAssignment
from cdktf_cdktf_provider_azurerm.data_factory_linked_service_azure_blob_storage import DataFactoryLinkedServiceAzureBlobStorage

class MyConstructLevelsStack(TerraformStack):
    def __init__(self, scope: Construct, id: str):

        # define private class variables to be used in stack
        self._id: str = id
        self._stack_settings: TerraformStackSettings = TerraformStackSettings()
        self._storage_backend_settings: TerraformAzureStorageBackendSetting = TerraformAzureStorageBackendSetting(state_file_name=f"{self._id}-myconstructlevelsstack")

        # Run TerraformStack as it's a prerequisite to define this class as a terraform stack
        super().__init__(scope, self._id)

        # Setup stack for terraform deployment to Azure
        self.setup_state_backend()

        # Get azure provider
        self._azure_provider = self.get_azure_provider(
            subscription_id=self._stack_settings.subscription_id
        )

        # Create a resource group in subscription
        self._construct_stack_rg: ResourceGroup = ResourceGroup(
            scope=self,
            provider=self._azure_provider,
            id_="MyConstructLevelsStackResourceGroup",
            name="myconstructlevelsstack-rg",
            location="West Europe",
        )

        # Deploy a full solution package (construct level 2)
        full_solution_config: AzureDataFactorySolutionConfig = AzureDataFactorySolutionConfig(
            resource_group_name=self._construct_stack_rg.name,
            location=self._construct_stack_rg.location,
            containers=["myconlevelscontainer", "nogeencontainerconlevels"]
        )
        AzureDataFactorySolution(
            scope=self,
            id="MyCustomFullSolution",
            azure_provider=self._azure_provider,
            config=full_solution_config,
        )

    @property
    def id(self) -> str:
        return self._id

    @property
    def stack_settings(self) -> TerraformStackSettings:
        return self._stack_settings

    @property
    def storage_backend_settings(self) -> TerraformAzureStorageBackendSetting:
        return self._storage_backend_settings

    def get_azure_provider(self, subscription_id: str) -> AzurermProvider:
        azure_provider: AzurermProvider = AzurermProvider(
            scope=self,
            id="AzureResourceManagerProvider",
            subscription_id=subscription_id,
            features=[{}],
        )

        return azure_provider

    def setup_state_backend(
        self,
    ) -> None:
        AzurermBackend(
            scope=self,
            resource_group_name=self.storage_backend_settings.resource_group,
            storage_account_name=self.storage_backend_settings.storage_account_name,
            container_name=self.storage_backend_settings.container_name,
            tenant_id=self.storage_backend_settings.tenant_id,
            key=self.storage_backend_settings.state_file,
            use_azuread_auth=True,
        )
