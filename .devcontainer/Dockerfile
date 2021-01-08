FROM mcr.microsoft.com/vscode/devcontainers/base:buster

# [Option] Install zsh
ARG INSTALL_ZSH="true"
# [Option] Upgrade OS packages to their latest versions
ARG UPGRADE_PACKAGES="false"
# [Option] Enable non-root Docker access in container
ARG ENABLE_NONROOT_DOCKER="true"

# Install needed packages and setup non-root user. Use a separate RUN statement to add your own dependencies.
ARG SOURCE_SOCKET=/var/run/docker-host.sock
ARG TARGET_SOCKET=/var/run/docker.sock
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

COPY .devcontainer/library-scripts/*.sh /tmp/library-scripts/
RUN apt-get update \
    && /bin/bash /tmp/library-scripts/common-debian.sh "${INSTALL_ZSH}" "${USERNAME}" "${USER_UID}" "${USER_GID}" "${UPGRADE_PACKAGES}" \
    # Use Docker script from script library to set things up
    && /bin/bash /tmp/library-scripts/docker-debian.sh "${ENABLE_NONROOT_DOCKER}" "${SOURCE_SOCKET}" "${TARGET_SOCKET}" "${USERNAME}" \
    # Clean up
    && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/* /tmp/library-scripts/

ENTRYPOINT [ "/usr/local/share/docker-init.sh" ]
CMD [ "sleep", "infinity" ]

### Setup python ###
# helpful links:
# https://github.com/pyenv/pyenv/wiki/Common-build-problems
# https://github.com/pyenv/pyenv/blob/32922007863c4a54feca2a95226c8307cfdfea3d/plugins/python-build/README.md
# https://github.com/pyenv/pyenv/issues/990
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    libbz2-dev \
    libffi-dev \
    liblzma-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libreadline-dev \
    libsqlite3-dev \
    libssl-dev \
    llvm \
    make \
    tk-dev \
    wget \
    xz-utils \
    zlib1g-dev \
    && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/*

USER ${USERNAME}

ENV LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    PYENV_SHELL="zsh"

RUN curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash

ENV PATH=/home/${USERNAME}/.pyenv/shims:/home/${USERNAME}/.pyenv/bin:$PATH

RUN set -ex; \
    pyenv install 3.8.6 \
    && pyenv global 3.8.6 \
    && pyenv rehash

RUN set -x; python -m pip install --disable-pip-version-check --no-cache-dir pylint pytest

WORKDIR /workspace

COPY --chown=${USERNAME}:${USERNAME} requirements.txt .

RUN python -m pip install --disable-pip-version-check --no-cache-dir -r requirements.txt