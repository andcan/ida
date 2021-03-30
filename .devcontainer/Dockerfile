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


### setup java ###
RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
    bzip2 \
    unzip \
    xz-utils \
    \
    # java.lang.UnsatisfiedLinkError: /usr/local/openjdk-11/lib/libfontmanager.so: libfreetype.so.6: cannot open shared object file: No such file or directory
    # java.lang.NoClassDefFoundError: Could not initialize class sun.awt.X11FontManager
    # https://github.com/docker-library/openjdk/pull/235#issuecomment-424466077
    fontconfig libfreetype6 \
    \
    # utilities for keeping Debian and OpenJDK CA certificates in sync
    ca-certificates p11-kit \
    ; \
    rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME /usr/local/openjdk-11
RUN { echo '#/bin/sh'; echo 'echo "$JAVA_HOME"'; } > /usr/local/bin/docker-java-home && chmod +x /usr/local/bin/docker-java-home && [ "$JAVA_HOME" = "$(docker-java-home)" ] # backwards compatibility
ENV PATH $JAVA_HOME/bin:$PATH
ENV LANG C.UTF-8
ENV JAVA_VERSION 11.0.10

RUN set -eux; \
    \
    arch="$(dpkg --print-architecture)"; \
    case "$arch" in \
    'amd64') \
    downloadUrl='https://github.com/AdoptOpenJDK/openjdk11-upstream-binaries/releases/download/jdk-11.0.10%2B9/OpenJDK11U-jdk_x64_linux_11.0.10_9.tar.gz'; \
    ;; \
    'arm64') \
    downloadUrl='https://github.com/AdoptOpenJDK/openjdk11-upstream-binaries/releases/download/jdk-11.0.10%2B9/OpenJDK11U-jdk_aarch64_linux_11.0.10_9.tar.gz'; \
    ;; \
    *) echo >&2 "error: unsupported architecture: '$arch'"; exit 1 ;; \
    esac; \
    \
    wget --progress=dot:giga -O openjdk.tgz "$downloadUrl"; \
    wget --progress=dot:giga -O openjdk.tgz.asc "$downloadUrl.sign"; \
    \
    export GNUPGHOME="$(mktemp -d)"; \
    # pre-fetch Andrew Haley's (the OpenJDK 8 and 11 Updates OpenJDK project lead) key so we can verify that the OpenJDK key was signed by it
    # (https://github.com/docker-library/openjdk/pull/322#discussion_r286839190)
    # we pre-fetch this so that the signature it makes on the OpenJDK key can survive "import-clean" in gpg
    gpg --batch --keyserver ha.pool.sks-keyservers.net --recv-keys EAC843EBD3EFDB98CC772FADA5CD6035332FA671; \
    # TODO find a good link for users to verify this key is right (https://mail.openjdk.java.net/pipermail/jdk-updates-dev/2019-April/000951.html is one of the only mentions of it I can find); perhaps a note added to https://adoptopenjdk.net/upstream.html would make sense?
    # no-self-sigs-only: https://salsa.debian.org/debian/gnupg2/commit/c93ca04a53569916308b369c8b218dad5ae8fe07
    gpg --batch --keyserver ha.pool.sks-keyservers.net --keyserver-options no-self-sigs-only --recv-keys CA5F11C6CE22644D42C6AC4492EF8D39DC13168F; \
    gpg --batch --list-sigs --keyid-format 0xLONG CA5F11C6CE22644D42C6AC4492EF8D39DC13168F \
    | tee /dev/stderr \
    | grep '0xA5CD6035332FA671' \
    | grep 'Andrew Haley'; \
    gpg --batch --verify openjdk.tgz.asc openjdk.tgz; \
    gpgconf --kill all; \
    rm -rf "$GNUPGHOME"; \
    \
    mkdir -p "$JAVA_HOME"; \
    tar --extract \
    --file openjdk.tgz \
    --directory "$JAVA_HOME" \
    --strip-components 1 \
    --no-same-owner \
    ; \
    rm openjdk.tgz*; \
    \
    # update "cacerts" bundle to use Debian's CA certificates (and make sure it stays up-to-date with changes to Debian's store)
    # see https://github.com/docker-library/openjdk/issues/327
    #     http://rabexc.org/posts/certificates-not-working-java#comment-4099504075
    #     https://salsa.debian.org/java-team/ca-certificates-java/blob/3e51a84e9104823319abeb31f880580e46f45a98/debian/jks-keystore.hook.in
    #     https://git.alpinelinux.org/aports/tree/community/java-cacerts/APKBUILD?id=761af65f38b4570093461e6546dcf6b179d2b624#n29
    { \
    echo '#!/usr/bin/env bash'; \
    echo 'set -Eeuo pipefail'; \
    echo 'trust extract --overwrite --format=java-cacerts --filter=ca-anchors --purpose=server-auth "$JAVA_HOME/lib/security/cacerts"'; \
    } > /etc/ca-certificates/update.d/docker-openjdk; \
    chmod +x /etc/ca-certificates/update.d/docker-openjdk; \
    /etc/ca-certificates/update.d/docker-openjdk; \
    \
    # https://github.com/docker-library/openjdk/issues/331#issuecomment-498834472
    find "$JAVA_HOME/lib" -name '*.so' -exec dirname '{}' ';' | sort -u > /etc/ld.so.conf.d/docker-openjdk.conf; \
    ldconfig; \
    \
    # https://github.com/docker-library/openjdk/issues/212#issuecomment-420979840
    # https://openjdk.java.net/jeps/341
    java -Xshare:dump;
RUN \
    # basic smoke test
    fileEncoding="$(echo 'System.out.println(System.getProperty("file.encoding"))' | jshell -s -)"; [ "$fileEncoding" = 'UTF-8' ]; rm -rf ~/.java; \
    javac --version; \
    java --version

### Setup python ###
# helpful links:
# https://github.com/pyenv/pyenv/wiki/Common-build-problems
# https://github.com/pyenv/pyenv/blob/32922007863c4a54feca2a95226c8307cfdfea3d/plugins/python-build/README.md
# https://github.com/pyenv/pyenv/issues/990

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    software-properties-common \
    && add-apt-repository non-free \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    libarchive-dev \
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
    p7zip-full \
    tk-dev \
    unrar \
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
