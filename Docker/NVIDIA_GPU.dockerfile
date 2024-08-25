# NVIDIA Tookkitが必要っぽい？
# あとローカルPC側でのセットアップが必要
FROM nvidia/cuda:12.6.0-base-ubuntu22.04 as base

ENV NV_CUDA_LIB_VERSION 12.6.0-1

FROM base as base-amd64

ENV NV_NVTX_VERSION=12.6.37-1
ENV NV_LIBNPP_VERSION=12.3.1.23-1
ENV NV_LIBNPP_PACKAGE libnpp-12-6=${NV_LIBNPP_VERSION}
ENV NV_LIBCUSPARSE_VERSION=12.5.2.23-1

ENV NV_LIBCUBLAS_PACKAGE_NAME=libcublas-12-6
ENV NV_LIBCUBLAS_VERSION=12.6.0.22-1
ENV NV_LIBCUBLAS_PACKAGE ${NV_LIBCUBLAS_PACKAGE_NAME}=${NV_LIBCUBLAS_VERSION}

FROM base as base-arm64

ENV NV_NVTX_VERSION 12.6.37-1
ENV NV_LIBNPP_VERSION 12.3.1.23-1
ENV NV_LIBNPP_PACKAGE libnpp-12-6=${NV_LIBNPP_VERSION}
ENV NV_LIBCUSPARSE_VERSION 12.5.2.23-1

ENV NV_LIBCUBLAS_PACKAGE_NAME libcublas-12-6
ENV NV_LIBCUBLAS_VERSION 12.6.0.22-1
ENV NV_LIBCUBLAS_PACKAGE ${NV_LIBCUBLAS_PACKAGE_NAME}=${NV_LIBCUBLAS_VERSION}

FROM base-${TARGETARCH}

ARG TARGETARCH

LABEL maintainer "NVIDIA CORPORATION <cudatools@nvidia.com>"

RUN apt-get update && apt-get install -y --no-install-recommends \
    cuda-libraries-12-6=${NV_CUDA_LIB_VERSION} \
    ${NV_LIBNPP_PACKAGE} \
    cuda-nvtx-12-6=${NV_NVTX_VERSION} \
    libcusparse-12-6=${NV_LIBCUSPARSE_VERSION} \
    ${NV_LIBCUBLAS_PACKAGE} \
    && rm -rf /var/lib/apt/lists/*

# Keep apt from auto upgrading the cublas and nccl packages. See https://gitlab.com/nvidia/container-images/cuda/-/issues/88
RUN apt-mark hold ${NV_LIBCUBLAS_PACKAGE_NAME}

# Add entrypoint items
COPY entrypoint.d/ /opt/nvidia/entrypoint.d/
COPY nvidia_entrypoint.sh /opt/nvidia/
ENV NVIDIA_PRODUCT_NAME="CUDA"
ENTRYPOINT ["/opt/nvidia/nvidia_entrypoint.sh"]
ARG DEBIAN_FRONTEND=noninteractive

HEALTHCHECK NONE
RUN useradd -d /home/Copy_YourSelf-Project -m -s /bin/bash Copy_YourSelf-Project

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
RUN pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib pyyaml
RUN cd mecab-ipadic-neologd && ./bin/install-mecab-ipadic-neologd -n -y
RUN apt-get update && apt-get install -y \
    vim \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Rust install
ENV RUST_HOME /usr/local/lib/rust
ENV RUSTUP_HOME ${RUST_HOME}/rustup
ENV CARGO_HOME ${RUST_HOME}/cargo
RUN mkdir /usr/local/lib/rust && \
    chmod 0755 $RUST_HOME
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs > ${RUST_HOME}/rustup.sh \
    && chmod +x ${RUST_HOME}/rustup.sh \
    && ${RUST_HOME}/rustup.sh -y --default-toolchain nightly --no-modify-path
ENV PATH $PATH:$CARGO_HOME/bin
RUN cd /home/Copy_YourSelf-Project && git clone https://github.com/tagaiza2129/Copy_YourSelf.git
WORKDIR /home/Copy_YourSelf-Project/Copy_YourSelf
RUN cargo build --release