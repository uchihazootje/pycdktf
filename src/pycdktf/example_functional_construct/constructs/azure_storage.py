from constructs import Construct
from cdktf_cdktf_provider_azurerm.provider import AzurermProvider
from cdktf_cdktf_provider_azurerm.storage_account import StorageAccount
from cdktf_cdktf_provider_azurerm.storage_data_lake_gen2_filesystem import StorageDataLakeGen2Filesystem

def create_storage_account(
    scope: Construct,
    provider: AzurermProvider,
    id: str,
    name: str,
    resource_group_name: str,
    location: str,
    account_tier: str,
    account_replication_type: str,
) -> StorageAccount:

    storage_account: StorageAccount = StorageAccount(
        scope=scope,
        provider=provider,
        id_=id,
        name=name,
        resource_group_name=resource_group_name,
        location=location,
        account_tier=account_tier,
        account_replication_type=account_replication_type,
    )

    return storage_account

def create_container(
    scope: Construct,
    provider: AzurermProvider,
    id: str,
    name: str,
    storage_account_id: str,
) -> StorageDataLakeGen2Filesystem:

    storage_container: StorageDataLakeGen2Filesystem = StorageDataLakeGen2Filesystem(
        scope=scope,
        provider=provider,
        id_=id,
        name=name,
        storage_account_id=storage_account_id,
    )

    return storage_container
