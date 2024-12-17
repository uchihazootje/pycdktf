from cdktf import AzurermBackend, TerraformStack
from constructs import Construct
from cdktf_cdktf_provider_azurerm.provider import AzurermProvider
from cdktf_cdktf_provider_azurerm.resource_group import ResourceGroup
from pycdktf.example_functional_construct.constructs.azure_storage import create_container, create_storage_account
from pycdktf.example_functional_construct.constructs.data_factory import create_data_factory, create_data_factory_blob_linked_service
from pycdktf.settings import TerraformAzureStorageBackendSetting, TerraformStackSettings
from cdktf_cdktf_provider_azurerm.storage_account import StorageAccount
from cdktf_cdktf_provider_azurerm.storage_data_lake_gen2_filesystem import StorageDataLakeGen2Filesystem
from cdktf_cdktf_provider_azurerm.data_factory import DataFactory
from cdktf_cdktf_provider_azurerm.data_azurerm_data_factory import DataAzurermDataFactory
from cdktf_cdktf_provider_azurerm.role_assignment import RoleAssignment
from cdktf_cdktf_provider_azurerm.data_factory_linked_service_azure_blob_storage import DataFactoryLinkedServiceAzureBlobStorage

class MyFunctionalConstructStack(TerraformStack):
    def __init__(self, scope: Construct, id: str):

        # define private class variables to be used in stack
        self._id: str = id
        self._stack_settings: TerraformStackSettings = TerraformStackSettings()
        self._storage_backend_settings: TerraformAzureStorageBackendSetting = TerraformAzureStorageBackendSetting(state_file_name=f"{self._id}-myfunctionalconstructstack")

        # Run TerraformStack as it's a prerequisite to define this class as a terraform stack
        super().__init__(scope, self._id)

        # Setup stack for terraform deployment to Azure
        self.setup_state_backend()

        # Get azure provider
        self._azure_provider = self.get_azure_provider(
            subscription_id=self._stack_settings.subscription_id
        )

        # Create a resource group in subscription
        self._simple_stack_rg: ResourceGroup = ResourceGroup(
            scope=self,
            provider=self._azure_provider,
            id_="MyFuncStackResourceGroup",
            name="myfuncstack-rg",
            location="West Europe",
        )

        # Create a storage account in the resource group
        self._storage_account: StorageAccount = create_storage_account(
            scope=self,
            provider=self._azure_provider,
            id="MyFuncStorageAccount",
            name="myrsfuncstackadls",
            resource_group_name=self._simple_stack_rg.name,
            location=self._simple_stack_rg.location,
            account_tier="Standard",
            account_replication_type ="LRS"
        )

        # Create a container in the storage account
        self._storage_container: StorageDataLakeGen2Filesystem = create_container(
            scope=self,
            provider=self._azure_provider,
            id="MyFuncStorageContainer",
            name="myrsfunccontainer",
            storage_account_id=self._storage_account.id,
        )

        # Create azure data factory instance
        self._data_factory = create_data_factory(
            scope=self,
            provider=self._azure_provider,
            id="MyFuncDataFactory",
            name="myrsfuncadf",
            resource_group_name=self._simple_stack_rg.name,
            location=self._simple_stack_rg.location,
            identity={"type": "SystemAssigned"},
        )

        # Get data about the data factory instance that are only known after creation is done
        self._data_factory_data_source: DataAzurermDataFactory = DataAzurermDataFactory(
            scope=self,
            provider=self._azure_provider,
            id_="MyFuncDataFactoryData",
            name=self._data_factory.name,
            resource_group_name=self._simple_stack_rg.name,
            depends_on=[self._data_factory],
        )

        # Add role storage blob data contributor permission for data factory on storage account
        RoleAssignment(
            id_="MyFuncDataFactoryRoleStorage",
            provider=self._azure_provider,
            scope_=self,
            scope=self._storage_account.id,
            principal_id=self._data_factory_data_source.identity.get(index=0).principal_id,
            role_definition_name="Storage Blob Data Contributor",
            depends_on=[self._data_factory_data_source],
        )

        # Add storage account as a linked service to azure data factory
        create_data_factory_blob_linked_service(
            scope=self,
            provider=self._azure_provider,
            id="MyFuncDataFactoryLinkedService",
            name=self._storage_account.name,
            data_factory_id=self._data_factory.id,
            use_managed_identity=True,
            service_endpoint=self._storage_account.primary_blob_endpoint,
            storage_kind=self._storage_account.account_kind,
            depends_on=[self._data_factory, self._storage_account]
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
