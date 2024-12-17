# ONLY source this script to deploy using cdktf LOCALLY
export ARM_TENANT_ID="" # tenant id
export ARM_CLIENT_ID="" # client id to use for deployment
export ARM_SUBSCRIPTION_ID="" # subscription id where resources will be deployed

if [[ -z "$ARM_CLIENT_SECRET" ]]; then
    echo "Type/paste your Terraform spn's secret:"
    export ARM_CLIENT_SECRET="$(read -s sec; echo $sec)"
fi

# Required for terraform remote backend hosted in azure
export ARM_BACKEND_RESOURCE_GROUP_NAME="" # name of resource group where storage account is created which will be used as backend for terraform state
export ARM_BACKEND_STORAGE_ACCOUNT_NAME="" # name of storage account which will be used as backend for terraform state
export ARM_BACKEND_BLOB_CONTAINER_NAME="" # name of container in storage account which will be used as backend for terraform state

# Allow passing optional argument to also login to az cli using the same spn env vars exported here above
if [[ "$@" =~ "azlogin" ]]; then
    echo 'logging into azcli'
    az login --service-principal \
        -u ${ARM_CLIENT_ID} \
        -p ${ARM_CLIENT_SECRET} \
        --tenant ${ARM_TENANT_ID}
    az account set --subscription ${ARM_SUBSCRIPTION_ID}
fi
