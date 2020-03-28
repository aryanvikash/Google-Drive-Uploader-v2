
# FROM alpine:3.10.2

# install ca-certificates so that HTTPS works consistently
# RUN apk add --no-cache ca-certificates

# RUN apk add --no-cache --update \
#       python3 \
#       bash \
#       aria2
# More information: https://www.gitpod.io/docs/config-docker/


FROM ubuntu:18.04


RUN apt -qq update
RUN apt -qq install -y aria2 python3 python3-pip locales
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8


