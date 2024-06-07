IMAGE_NAME=deep_learning_image
INSTALL_TYPE=$1

if [ "$INSTALL_TYPE" = "intel_GPU" ]; then
    docker build --no-cache --build-arg ICD_VER=23.43.27642.40-803~22.04 \
                            --build-arg LEVEL_ZERO_GPU_VER=1.3.27642.40-803~22.04 \
                            --build-arg LEVEL_ZERO_VER=1.14.0-744~22.04 \
                            --build-arg LEVEL_ZERO_DEV_VER=1.14.0-744~22.04 \
                            --build-arg DPCPP_VER=2024.1.0-963 \
                            --build-arg MKL_VER=2024.1.0-691 \
                            --build-arg CCL_VER=2021.12.0-309 \
                            --build-arg PYTHON=python3.10 \
                            --build-arg TF_VER=2.15 \
                            -t $IMAGE_NAME \
                            -f "${INSTALL_TYPE}.dockerfile" .
elif [ "$INSTALL_TYPE" = "NVIDIA_GPU" ]; then
    curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | \
    sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
    && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
        sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
        sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
    sudo apt update
    sudo apt install -y nvidia-container-toolkit
    sudo systemctl restart docker
    docker build --no-cache  \
        -t $IMAGE_NAME \
        -f "${INSTALL_TYPE}.dockerfile" .
else 
    docker build --no-cache --build-arg PYTHON=python3.10 \
        --build-arg TF_VER=2.15 \
        -t $IMAGE_NAME \
        -f "cpu.dockerfile" .
fi