from constructs import Construct
from cdktf_cdktf_provider_azurerm.provider import AzurermProvider
from cdktf_cdktf_provider_azurerm.data_factory import DataFactory
from cdktf_cdktf_provider_azurerm.data_factory_linked_service_azure_blob_storage import DataFactoryLinkedServiceAzureBlobStorage

def create_data_factory(
    scope: Construct,
    provider: AzurermProvider,
    id: str,
    name: str,
    resource_group_name: str,
    location: str,
    identity: dict[str, str],
) -> DataFactory:

    data_factory: DataFactory = DataFactory(
        scope=scope,
        provider=provider,
        id_=id,
        name=name,
        resource_group_name=resource_group_name,
        location=location,
        identity=identity,
    )

    return data_factory

def create_data_factory_blob_linked_service(
    scope: Construct,
    provider: AzurermProvider,
    id: str,
    name: str,
    data_factory_id: str,
    use_managed_identity: bool,
    service_endpoint: str,
    storage_kind: str,
    depends_on: list[Construct],
) -> DataFactoryLinkedServiceAzureBlobStorage:

    blob_linked_service: DataFactoryLinkedServiceAzureBlobStorage = DataFactoryLinkedServiceAzureBlobStorage(
        scope=scope,
        id_=id,
        provider=provider,
        name=name,
        data_factory_id=data_factory_id,
        use_managed_identity=use_managed_identity,
        service_endpoint=service_endpoint,
        storage_kind=storage_kind,
        depends_on=depends_on,
    )

    return blob_linked_service
