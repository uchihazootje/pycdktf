import os


class TerraformConfigEnvironmentValueMissingI(Exception):
    """Raised when Terraform config environment values are missing."""


class TerraformStackSettings:

    @property
    def subscription_id(self) -> str:
        return get_env_value(key="ARM_SUBSCRIPTION_ID")


class TerraformAzureStorageBackendSetting:
    def __init__(self, state_file_name: str) -> None:
        self._state_file_name = state_file_name

    @property
    def tenant_id(self) -> str:
        return get_env_value(key="ARM_TENANT_ID")

    @property
    def resource_group(self) -> str:
        return get_env_value(key="ARM_BACKEND_RESOURCE_GROUP_NAME")

    @property
    def storage_account_name(self) -> str:
        return get_env_value(key="ARM_BACKEND_STORAGE_ACCOUNT_NAME")

    @property
    def container_name(self) -> str:
        return get_env_value(key="ARM_BACKEND_BLOB_CONTAINER_NAME")

    @property
    def state_file(self) -> str:
        return f"{self._state_file_name}-state.tfstate"


def get_env_value(key: str, exception: bool | None = True) -> str:
    value: str | None = os.getenv(key)
    if (not value or value == "") and exception:
        raise TerraformConfigEnvironmentValueMissingI(
            f"Environment config {key} is missing."
        )
    return value
