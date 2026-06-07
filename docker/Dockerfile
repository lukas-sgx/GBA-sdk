FROM alpine

RUN apk update && apk add \
    gcc-arm-none-eabi \
    newlib-arm-none-eabi \
    python3 \
    py3-pip \
    make \
    bash

RUN python3 -m venv /venv

WORKDIR /app