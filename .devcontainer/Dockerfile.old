FROM alpine:latest

ARG USERNAME=dev
ARG USER_UID=1000
ARG USER_GID=1000
ARG HOME=/home/${USERNAME}
ARG ENABLE_NONROOT_DOCKER="true"
ARG SOURCE_SOCKET=/var/run/docker-host.sock
ARG TARGET_SOCKET=/var/run/docker.sock

ENV PYTHONUNBUFFERED 1

COPY .devcontainer/app/*.sh /tmp/library-scripts/

RUN set -x; \
    apk add --no-cache \
        curl \
        git \
        python2 \
        py3-virtualenv \
        shadow \
        zsh \
    && addgroup --gid ${USER_GID} ${USERNAME} \
    && adduser \
        --disabled-password \
        --gecos '' \
        --home "${HOME}" \
        --ingroup "${USERNAME}" \
        --uid "${USER_UID}" \
        --shell /bin/zsh \
        "${USERNAME}" \
    && echo 'dev ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers \
    && /bin/ash /tmp/library-scripts/docker-alpine.sh "${ENABLE_NONROOT_DOCKER}" "${SOURCE_SOCKET}" "${TARGET_SOCKET}" "${USERNAME}" \
    && virtualenv -p /usr/bin/python2.7 ${HOME}/.virtualenvs/venv \
    && ash -c 'echo '"'"'export PATH=${HOME}/.virtualenvs/venv/bin:"$PATH"'"'"' >> ${HOME}/.zshenv' \
    && chown -R ${USERNAME}:${USERNAME} ${HOME}/.virtualenvs/venv

COPY --chown=${USERNAME}:${USERNAME} .devcontainer/.zshrc ${HOME}/.zshrc

RUN set -e; \
    apk add --no-cache ncurses 

USER ${USERNAME}

ENV TERM=dumb

RUN set -e; \
    zsh -c 'curl -sL --proto-redir -all,https https://raw.githubusercontent.com/zplug/installer/master/installer.zsh | zsh'

WORKDIR /workspace

COPY --chown=${USERNAME}:${USERNAME} requirements.txt .

RUN set -x; \
    zsh -c 'python -m pip install --disable-pip-version-check --no-cache-dir pylint pytest' \
    && zsh -c 'python -m pip install --disable-pip-version-check --no-cache-dir -r requirements.txt'

ENTRYPOINT [ "/usr/local/share/docker-init.sh" ]


