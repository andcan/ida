FROM debian:jessie

RUN set -x; \
        apt-get update \
        && apt-get install -y --no-install-recommends \
            ca-certificates \
            curl \
            dirmngr \
            node-less \
            python-gevent \
            python-ldap \
            python-pip \
            python-qrcode \
            python-renderpm \
            python-support \
            python-vobject \
            python-watchdog \
            git \
            libxml2-dev \
            libxslt1-dev \
            zlib1g-dev \
            libjpeg62-turbo-dev \
            libldap2-dev \
            libsasl2-dev \
            libevent-dev \
            build-essential \
            python-dev \
        && curl -o wkhtmltox.deb -sSL https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.5/wkhtmltox_0.12.5-1.jessie_amd64.deb \
        && echo '4d104ff338dc2d2083457b3b1e9baab8ddf14202 wkhtmltox.deb' | sha1sum -c - \
        && dpkg --force-depends -i wkhtmltox.deb \
        && apt-get -y install -f --no-install-recommends \
        && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false -o APT::AutoRemove::SuggestsImportant=false npm \
        && rm -rf /var/lib/apt/lists/* wkhtmltox.deb \
        && pip install psycogreen==1.0

# install latest postgresql-client
RUN set -x; \
        echo 'deb http://apt.postgresql.org/pub/repos/apt/ jessie-pgdg main' > etc/apt/sources.list.d/pgdg.list \
        && export GNUPGHOME="$(mktemp -d)" \
        && repokey='B97B0AFCAA1A47F044F244A07FCC7D46ACCC4CF8' \
        && gpg --batch --keyserver keyserver.ubuntu.com --recv-keys "${repokey}" \
        && gpg --armor --export "${repokey}" | apt-key add - \
        && rm -rf "$GNUPGHOME" \
        && apt-get update  \
        && apt-get install -y \
            postgresql-server-dev-9.6 \
        && rm -rf /var/lib/apt/lists/*

RUN set -x; \
    mkdir -p /opt/odoo \
    && useradd -m -s /bin/bash -d /var/lib/odoo odoo \
    && chown -R odoo /opt/odoo


COPY .devcontainer/odoo/odoo.conf /etc/odoo/
RUN chown odoo /etc/odoo/odoo.conf
ENV ODOO_RC /etc/odoo/odoo.conf

USER odoo

WORKDIR /opt/odoo

RUN git clone https://bitbucket.org/creativiquadrati/cq_odoo10.git -b master --single-branch .

USER root

RUN pip install -r requirements.txt

USER odoo

ARG GITHUB_USER
ARG GITHUB_PASSWORD
RUN set -x; \
    mkdir -p /opt/odoo/extra_addons \
    && mkdir -p /opt/odoo/odoo10_generic_addons \
    && git clone https://github.com/ssiccardi/odoo10_generic_addons.git /opt/odoo/odoo10_generic_addons \
    && git clone https://bitbucket.org/creativiquadrati/account_type_menu.git /opt/odoo/extra_addons/account_type_menu \
    && git clone https://bitbucket.org/creativiquadrati/account_payment_term_extension.git /opt/odoo/extra_addons/account_payment_term_extension \
    && git clone https://bitbucket.org/creativiquadrati/account_invoice_entry_date_10.git /opt/odoo/extra_addons/account_invoice_entry_date \
    && git clone https://bitbucket.org/creativiquadrati/l10n_it_fiscalcode_10.git /opt/odoo/extra_addons/l10n_it_fiscalcode \
    && git clone https://${GITHUB_USER}:${GITHUB_PASSWORD}@github.com/ssiccardi/giustizia.git /opt/odoo/extra_addons/giustizia

ADD --chown=odoo:odoo .devcontainer/odoo/giustizia.tar.gz /var/lib/odoo/filestore/giustizia

VOLUME /var/lib/odoo

#
## Mount /var/lib/odoo to allow restoring filestore and /mnt/extra-addons for users addons
#RUN mkdir -p /mnt/extra-addons \
#        && chown -R odoo /mnt/extra-addons
#VOLUME ["/var/lib/odoo", "/mnt/extra-addons"]

EXPOSE 8069 8071

COPY --chown=odoo:odoo .devcontainer/odoo/entrypoint.py .

CMD ["python", "./entrypoint.py"]