FROM alpine as build

RUN apk add --no-cache curl tar \
    && curl -sSL 'https://github.com/armandleopold/graphexp/archive/v0.8.2.tar.gz' | tar -xz

FROM nginx

COPY --from=build /graphexp-0.8.2/ /usr/share/nginx/html
COPY .devcontainer/graphexp/graphConf.js /usr/share/nginx/html/scripts