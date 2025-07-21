FROM nvidia/cuda:11.8.0-devel-ubuntu22.04

# Suppress tzdata timezone config prompt
ENV DEBIAN_FRONTEND=noninteractive

# Set UTF-8 locale
RUN apt-get update && \
    apt-get install --no-install-recommends -y locales && \
    locale-gen en_US.UTF-8 && \
    rm -rf /var/lib/apt/lists/*
ENV LANG=en_US.UTF-8 \
    LANGUAGE=en_US:en \
    LC_ALL=en_US.UTF-8

# Install Python 3.10 and essential tools
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
        python3.10 \
        python3.10-venv \
        python3.10-distutils \
        curl \
        git \
        sudo \
        openssh-client \
        ca-certificates \
        wget && \
	    ln -sf python3.10 /usr/bin/python3 && \
	    rm -rf /var/lib/apt/lists/*
    
RUN apt-get update && \
    apt-get install --no-install-recommends -y \    
    ffmpeg \
    mediainfo \
    sox \
    libsndfile1 \
    gstreamer1.0-tools \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-ugly \
    gstreamer1.0-libav


# Install pip (latest) and PyTorch + dependencies
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3 && \
    pip install --upgrade pip && \
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

RUN pip install --no-cache-dir opencv-contrib-python

RUN rm -rf /var/lib/apt/lists/*

# Create non-root user
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid ${USER_GID} ${USERNAME} && \
    useradd --uid ${USER_UID} --gid ${USER_GID} -m ${USERNAME} && \
    echo "${USERNAME} ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/${USERNAME} && \
    chmod 0440 /etc/sudoers.d/${USERNAME}

USER ${USERNAME}
ENV PATH=/home/${USERNAME}/.local/bin:$PATH
