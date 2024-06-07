docker run  -ti \
        --memory=13g \
        --memory-swap=13g \
        -v /mnt:/media/ \
        -p 2459:2459  \
        --device /dev/dxg \
        --mount type=bind,src=/usr/lib/wsl,dst=/usr/lib/wsl \
        -e LD_LIBRARY_PATH=/usr/lib/wsl/lib  \
        --network host \
        deep_learning_image