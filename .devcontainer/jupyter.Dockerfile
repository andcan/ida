FROM debian:buster

ARG USERNAME=jupyter

RUN useradd -s /bin/bash -m $USERNAME

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

ENV TINI_VERSION v0.19.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
RUN chmod +x /usr/bin/tini
ENTRYPOINT ["/usr/bin/tini", "--"]

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

COPY requirements.txt .

RUN python -m pip install --disable-pip-version-check --no-cache-dir -r requirements.txt

RUN python -m pip install jupyter
RUN python -m pip install jupyterlab


CMD ["python", "-m", "jupyter", "lab", "--port=8888", "--no-browser", "--ip=0.0.0.0"]