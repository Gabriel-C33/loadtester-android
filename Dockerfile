FROM ubuntu:22.04

# Prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git zip unzip openjdk-17-jdk wget \
    python3 python3-pip python3-venv \
    autoconf automake libtool pkg-config \
    zlib1g-dev libncurses5-dev libncursesw5-dev \
    cmake libffi-dev libssl-dev ccache \
    gettext texinfo help2man gperf libltdl-dev m4 \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -s /bin/bash builduser && \
    mkdir -p /app && \
    chown -R builduser:builduser /app

# Switch to non-root user
USER builduser
WORKDIR /app

# Install buildozer and cython
RUN python3 -m pip install --user --upgrade pip && \
    python3 -m pip install --user buildozer cython

# Add pip binaries to PATH
ENV PATH="/home/builduser/.local/bin:${PATH}"

# Copy entrypoint script
COPY --chown=builduser:builduser entrypoint.sh /entrypoint.sh
USER root
RUN chmod +x /entrypoint.sh
USER builduser

# Use entrypoint script
CMD ["/entrypoint.sh"]
