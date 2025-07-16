FROM ubuntu22-cuda118-python310:latest


# Install Torch + CUDA
RUN pip install torch==2.5.1 \
                torchvision==0.20.1 \
                torchaudio==2.5.1 \
                --index-url https://download.pytorch.org/whl/cu118

# Install Whisper
RUN pip install git+https://github.com/openai/whisper.git

WORKDIR /workspace
CMD ["/bin/bash"]
