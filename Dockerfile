# Minimal Dockerfile for building Fast Downward (Ubuntu + C++ toolchain + CMake + make + Python 3)
# Based on Ubuntu 22.04 LTS

FROM ubuntu:22.04

# Avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install required build tools: build-essential (includes g++ and make), cmake, python3
# Keep image small by removing apt lists afterwards
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    python3 \
    python3-venv \
    ca-certificates \
    wget \
    git \
 && rm -rf /var/lib/apt/lists/*

# Optional: make 'python' point to python3
RUN ln -sf /usr/bin/python3 /usr/bin/python || true

# Create a non-root user to run builds (optional but recommended)
ARG USERNAME=builder
ARG UID=1000
RUN useradd -m -u ${UID} -s /bin/bash ${USERNAME} || true
WORKDIR /home/${USERNAME}
RUN chown ${USERNAME}:${USERNAME} /home/${USERNAME}
USER ${USERNAME}

# Default working directory (you can mount your repo here when running)
WORKDIR /home/${USERNAME}/src

# Small label for the image
LABEL org.opencontainers.image.source="https://github.com/your/repo"

# Default command
CMD ["bash"]
