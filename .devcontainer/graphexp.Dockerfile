FROM nginx

RUN apt-get update \
    && apt-get -y --no-install-recommends install git \
    && git clone https://github.com/bricaud/graphexp \
    && mv graphexp/*  /usr/share/nginx/html \
    && apt-get remove -y git \
    && apt-get autoremove -y \
    && apt-get autoclean -y \
    && rm -rf /var/lib/apt/lists/*