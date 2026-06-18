FROM alpine

RUN apk update && apk add \
    gcc-arm-none-eabi \
    newlib-arm-none-eabi \
    python3 \
    py3-pip \
    cmake \
    make \
    bash \
    build-base

RUN python3 -m venv /venv

WORKDIR /app