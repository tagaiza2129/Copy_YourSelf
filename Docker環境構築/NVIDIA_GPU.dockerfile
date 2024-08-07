FROM nvidia/cuda:11.4.2-cudnn8-runtime-ubuntu22.04
ARG DEBIAN_FRONTEND=noninteractive

HEALTHCHECK NONE
RUN useradd -d /home/itex -m -s /bin/bash itex

RUN ln -sf bash /bin/sh
EXPOSE 2459

RUN apt-get update && \
    apt-get install -y --no-install-recommends --fix-missing \
    apt-utils \
    ca-certificates \
    clinfo \
    git \
    gnupg2 \
    gpg-agent \
    rsync \
    sudo \
    unzip \
    wget && \
    apt-get clean && \
    rm -rf  /var/lib/apt/lists/*

ENV LANG=C.UTF-8
ARG PYTHON=python3.10

RUN apt-get update && apt-get install -y --no-install-recommends --fix-missing \
    ${PYTHON} lib${PYTHON} python3-pip && \
    apt-get clean && \
    rm -rf  /var/lib/apt/lists/*

RUN ln -sf $(which ${PYTHON}) /usr/local/bin/python && \
    ln -sf $(which ${PYTHON}) /usr/local/bin/python3 && \
    ln -sf $(which ${PYTHON}) /usr/bin/python && \
    ln -sf $(which ${PYTHON}) /usr/bin/python3

RUN pip --no-cache-dir install --upgrade \
    pip \
    setuptools

ARG TF_VER="2.15"

RUN pip --no-cache-dir install tensorflow==${TF_VER}

RUN pip install wget tqdm gensim flask
RUN pip install websockets
RUN pip install scipy==1.10.1

RUN sudo apt update \
        && sudo apt install -y mecab libmecab-dev mecab-ipadic-utf8 git make curl xz-utils file

RUN pip install mecab-python3 
RUN git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git
RUN sudo apt install --reinstall -y build-essential
RUN pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
RUN cd mecab-ipadic-neologd && ./bin/install-mecab-ipadic-neologd -n -y