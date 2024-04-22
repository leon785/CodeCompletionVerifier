FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive

# system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    software-properties-common \
    build-essential \
    git \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# install LLVM clang
RUN wget https://apt.llvm.org/llvm.sh && \
    chmod +x llvm.sh && \
    ./llvm.sh 10

RUN apt-get update && apt-get install -y \
    clang-10 \
    clang-tools-10 \
    clang-tidy-10 \
    clang-format-10 \
    libclang-10-dev \
    && rm -rf /var/lib/apt/lists/*

ENV CC=clang-10
ENV CXX=clang++-10
ENV PATH="/usr/lib/llvm-10/bin:${PATH}"

# project dependencies
COPY requirements.txt /tmp/
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /project
COPY . /project

COPY start.sh /start.sh
RUN chmod +x /start.sh
CMD ["/start.sh"]