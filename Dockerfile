# 使用官方的Ubuntu基础镜像
FROM ubuntu:20.04

# 设定非交互式安装（自动化安装，不需要人工介入）
ARG DEBIAN_FRONTEND=noninteractive

# 安装必要的系统包
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    software-properties-common \
    build-essential \
    git \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# 添加LLVM的官方仓库到源列表，并安装LLVM和Clang
RUN wget https://apt.llvm.org/llvm.sh && \
    chmod +x llvm.sh && \
    ./llvm.sh 10

# 安装Clang和Clang-Tools
RUN apt-get update && apt-get install -y \
    clang-10 \
    clang-tools-10 \
    clang-tidy-10 \
    clang-format-10 \
    libclang-10-dev \
    && rm -rf /var/lib/apt/lists/*

# 设置环境变量，指定编译器和路径
ENV CC=clang-10
ENV CXX=clang++-10
ENV PATH="/usr/lib/llvm-10/bin:${PATH}"

# 安装Python依赖
COPY requirements.txt /tmp/
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

# 工作目录
WORKDIR /project

# 将项目文件复制到工作目录
COPY . /project

# 运行静态分析命令
CMD ["clang-tidy-10", "./data/extracted_snippet.c", "--", "-I/usr/lib/llvm-10/include"]
