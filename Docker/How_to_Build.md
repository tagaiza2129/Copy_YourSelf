# NVIDIA GPUの場合
インストールコマンド \
``` sh 
$ docker build --no-cache -t copy_yourself:lastest -f NVIDIA_GPU.dockerfile .
```
起動コマンド \
``` sh
$ docker run -ti \
        --memory=10g \
        --memory-swap=13g \
        -v $MOUNT_FILE:/home/itex/Copy_YourSelf/ \
        -p 2459:2460 \
        --gpus all \
        -it --rm \
        copy_yourself:lastest
```
※ $MOUNT_FILEはアプリと連動させるファイルを指定してください \
# INTEL GPUの場合
インストールコマンド
``` sh 
$ docker build --no-cache --build-arg UBUNTU_VERSION=22.04 \
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
```
起動コマンド
``` sh
$ docker run  -ti \
        --memory=13g \
        --memory-swap=13g \
        -v /mnt:/media/ \
        -p 2459:2459  \
        --device /dev/dxg \
        --mount type=bind,src=/usr/lib/wsl,dst=/usr/lib/wsl \
        -e LD_LIBRARY_PATH=/usr/lib/wsl/lib  \
        --network host \
        copy_yourself:lastest
```
# CPU動作の場合
インストールコマンド
``` sh 
$ docker build --no-cache -t copy_yourself:lastest -f cpu.dockerfile .
```
起動コマンド
``` sh
$ docker run -ti \
        --memory=5g \
        --memory-swap=5g \
        -v $MOUNT_FILE:/home/itex/Copy_YourSelf/ \
        -p 2459:2460 \
        $IMAGE_NAME
```
