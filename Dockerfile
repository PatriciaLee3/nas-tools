# ============================================
# Stage 1: 基础构建器
# ============================================
FROM python:3.13-alpine AS base-builder

# 复制系统包列表
COPY package_list.txt /tmp/

# 安装 uv 包管理器
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 安装系统构建依赖和运行时依赖
RUN apk add --no-cache --virtual .build-deps \
        libffi-dev \
        gcc \
        musl-dev \
        libxml2-dev \
        libxslt-dev \
    && apk add --no-cache $(cat /tmp/package_list.txt) \
    && ln -sf /usr/bin/python3 /usr/bin/python \
    && rm -rf /tmp/* /root/.cache /var/cache/apk/*

# ============================================
# Stage 2: 依赖构建器
# ============================================
FROM base-builder AS dep-builder

WORKDIR /tmp

# 复制 Python 依赖配置（利用 Docker 缓存）
COPY pyproject.toml uv.lock ./

# 创建虚拟环境并安装依赖
RUN uv venv .venv \
    && uv sync --frozen --no-install-project \
    && mv .venv /usr/local/uv-venv

# 安装外部工具 (rclone 和 mc)
RUN curl -sSL https://rclone.org/install.sh | bash \
    && ARCH=$(case "$(uname -m)" in \
        x86_64) echo "amd64";; \
        aarch64) echo "arm64";; \
        esac) \
    && curl -sSL https://dl.min.io/client/mc/release/linux-${ARCH}/mc -o /usr/bin/mc \
    && chmod +x /usr/bin/mc

# 清理构建缓存
RUN rm -rf /tmp/* /root/.cache

# ============================================
# Stage 3: 应用构建器
# ============================================
FROM base-builder AS app-builder

# 复制 Python 虚拟环境
COPY --from=dep-builder /usr/local/uv-venv /usr/local/uv-venv
COPY --from=dep-builder /usr/bin/rclone /usr/bin/
COPY --from=dep-builder /usr/bin/mc /usr/bin/

# 复制应用代码
WORKDIR /nas-tools
COPY . .

# 复制 s6-overlay rootfs 配置
COPY --chmod=755 docker/rootfs/ /

# 创建用户和目录
ENV HOME="/nt" \
    WORKDIR="/nas-tools"

RUN mkdir -p ${WORKDIR} ${HOME} \
    && addgroup -S nt -g 911 \
    && adduser -S nt -G nt -h ${HOME} -s /bin/bash -u 911 \
    && echo 'fs.inotify.max_user_watches=5242880' >> /etc/sysctl.conf \
    && echo 'fs.inotify.max_user_instances=5242880' >> /etc/sysctl.conf \
    && echo 'vm.overcommit_memory=1' >> /etc/sysctl.conf \
    && echo "nt ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers \
    && chown -R nt:nt ${WORKDIR} ${HOME}

# ============================================
# Stage 4: 最终运行时镜像
# ============================================
FROM scratch

# 复制应用构建器的文件系统
COPY --from=app-builder / /

# 设置环境变量（移除自动更新相关变量）
ENV S6_SERVICES_GRACETIME=30000 \
    S6_KILL_GRACETIME=60000 \
    S6_CMD_WAIT_FOR_SERVICES_MAXTIME=0 \
    S6_SYNC_DISKS=1 \
    HOME="/nt" \
    TERM="xterm" \
    PATH=${PATH}:/usr/lib/chromium:/usr/local/uv-venv/bin \
    LANG="C.UTF-8" \
    TZ="Asia/Shanghai" \
    NASTOOL_CONFIG="/config/config.yaml" \
    PS1="\u@\h:\w \$ " \
    PYPI_MIRROR="https://pypi.tuna.tsinghua.edu.cn/simple" \
    ALPINE_MIRROR="mirrors.ustc.edu.cn" \
    PUID=0 \
    PGID=0 \
    UMASK=000 \
    WORKDIR="/nas-tools"

WORKDIR ${WORKDIR}

# 暴露端口
EXPOSE 3000

# 挂载配置目录
VOLUME ["/config"]

# 启动入口
ENTRYPOINT ["/init"]
