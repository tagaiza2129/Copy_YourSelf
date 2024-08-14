#!/bin/bash

RUNTYPE=$1

if [ "$RUNTYPE" == "XPU" ]; then
    docker build --no-cache --build-arg UBUNTU_VERSION=22.04 \
                                --build-arg ICD_VER=23.43.27642.50-803~22.04 \
                                --build-arg LEVEL_ZERO_GPU_VER=1.3.27642.50-803~22.04 \
                                --build-arg LEVEL_ZERO_VER=1.14.0-744~22.04 \
                                --build-arg LEVEL_ZERO_DEV_VER=1.14.0-744~22.04 \
                                --build-arg DPCPP_VER=2024.2.1-1079 \
                                --build-arg MKL_VER=2024.2.1-103 \
                                --build-arg CCL_VER=2021.13.1-31 \
                                --build-arg PYTHON=python3.10 \
                                --build-arg TF_VER=2.15.1 \
                                -t copy_yourself:lastest \
				-f intel_GPU.dockerfile .
elif [ "$RUNTYPE" == "GPU" ]; then
    docker build --no-cache -t copy_yourself:latest -f NVIDIA_GPU.dockerfile .
else
    docker build --no-cache -t copy_yourself:latest -f cpu.dockerfile .
fi