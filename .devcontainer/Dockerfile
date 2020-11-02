FROM python:3

ENV PYTHONUNBUFFERED 1

ARG USERNAME=dev
ARG USER_UID=1000
ARG USER_GID=1000
ARG HOME=/home/${USERNAME}

RUN set -x; \
    apt-get update \
    && apt-get install -y --no-install-recommends \
        git \
        python2 \
        zsh \
        zplug gawk \
    && useradd --create-home --uid 1000 --shell /bin/zsh ${USERNAME} \
    && rm -rf /var/lib/apt/lists/*

COPY .devcontainer/.zshrc ${HOME}/.zshrc

USER ${USERNAME}

WORKDIR ${HOME}

RUN set -x; \
    python3 -m pip install --disable-pip-version-check --no-warn-script-location --no-cache-dir --user pipx \
    && bash -c 'echo '"'"'export PATH="$PATH":${HOME}/.local/bin'"'"' >> ${HOME}/.zshenv' \
    && bash -c 'echo pycodestyle pydocstyle pylint pytest virtualenv | xargs -n 1 python3 -m pipx install --system-site-packages --pip-args "--no-cache-dir --force-reinstall"' \
    && mkdir -p ${HOME}/venvs && ${HOME}/.local/bin/virtualenv -p /usr/bin/python2.7 venvs/venv \
    && bash -c 'echo '"'"'export PATH=${HOME}/venvs/venv/bin:$PATH'"'"' >> ${HOME}/.zshenv'

WORKDIR /workspace

COPY --chown=dev:dev requirements.txt .

RUN zsh -c 'pip install -r requirements.txt'

# [Optional] If your requirements rarely change, uncomment this section to add them to the image.
# COPY requirements.txt /tmp/pip-tmp/
# RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
#    && rm -rf /tmp/pip-tmp




