ARG node_version=20
ARG python_version=3.11
ARG alpine_version=3.20

FROM node:${node_version}-alpine${alpine_version} AS node
FROM python:${python_version}-alpine${alpine_version} AS python

    LABEL \
    author="Zohair" \
    version="1.0"

    ## Install Packages ##
    RUN apk update && \
        apk upgrade
    RUN apk add build-base libffi-dev git curl unzip make jq

    ## Install Terraform ##
    ARG terraform_version=1.9.0
    RUN curl -fsSL https://releases.hashicorp.com/terraform/${terraform_version}/terraform_${terraform_version}_linux_amd64.zip -o terraform.zip && \
        unzip terraform.zip && \
        mv terraform /usr/local/bin/ && \
        rm terraform.zip

    ## Install Poetry and Azure CLI ##
    RUN python -m pip install pipx
    RUN pipx install --global poetry azure-cli

    ## Configure Node ##
    # copy node installation from stage
    COPY --from=node /usr/lib /usr/lib
    COPY --from=node /usr/local/lib /usr/local/lib
    COPY --from=node /usr/local/include /usr/local/include
    COPY --from=node /usr/local/bin /usr/local/bin

    ## Install CDKTF ##
    ARG cdktf_version=0.20
    RUN npm install --global cdktf-cli@${cdktf_version}

    # Dependencies for Azure Devops Pipeline
    RUN apk add --no-cache --virtual .pipeline-deps readline linux-pam \
        && apk add bash sudo shadow \
        && apk del .pipeline-deps
    LABEL "com.azure.dev.pipelines.agent.handler.node.path"="/usr/local/bin/node"
    CMD ["node"]
