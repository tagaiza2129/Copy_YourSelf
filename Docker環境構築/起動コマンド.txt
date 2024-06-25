RUN_TYPERUN_TYPE=$1
RUN_PLATFORM=$2
IMAGE_NAME=deep_learning_image
if [ "$RUNTYPE" = "XPU" ]; then 
    docker run  -ti \
        --memory=13g \
        --memory-swap=13g \
        -v /mnt:/media/ \
        -p 2459:2460  \
        --device /dev/dxg \
        --mount type=bind,src=/usr/lib/wsl,dst=/usr/lib/wsl \
        -e LD_LIBRARY_PATH=/usr/lib/wsl/lib  \
        $IMAGE_NAME
elif [ "$RUNTYPE" = "GPU" ]; then
    docker run -ti \
        --memory=10g \
        --memory-swap=13g \
        -v /mnt:/media/ \
        -p 2459:2460 \
        --gpus all \
        -it --rm \
        $IMAGE_NAME
else
    if [ "$RUN_PLATFORM" = "mac" ]; then
        docker run -ti \
            --memory=5g \
            --memory-swap=5g \
            -v /Volumes:/media/ \
            -p 2459:2460 \
            $IMAGE_NAME
    else
        docker run -ti \
            --memory=5g \
            --memory-swap=5g \
            -v /mnt:/media/ \
            -p 2459:2460 \
            $IMAGE_NAME
    fi
fi
