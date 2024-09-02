> [!NOTE]  
　GPU等はWSL環境の場合のコマンドです windowsのDockerで動かす場合コマンドが多少変わるかもしれません
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
        -v $MOUNT_FILE:/home/Copy_YourSelf-Project/Copy_YourSelf/ \
        -p 2459:2460 \
        --gpus all \
        -it --rm \
        copy_yourself:lastest
```
※ $MOUNT_FILEはアプリと連動させるファイルを指定してください \
# INTEL GPUの場合
インストールコマンド
``` sh 
$ docker build --no-cache -t copy_yourself:lastest -f intel_GPU.dockerfile .
```
起動コマンド
``` sh
$ docker run  -ti \
        --memory=13g \
        --memory-swap=13g \
        -v $MOUNT_FILE:/home/Copy_YourSelf-Project/Copy_YourSelf/ \
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
        -v $MOUNT_FILE:/home/Copy_YourSelf-Project/Copy_YourSelf/ \
        -p 2459:2460 \
        copy_yourself:lastest
```
