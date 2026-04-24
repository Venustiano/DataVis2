FROM rocker/binder:latest
# this env var is recognized by jupyter-vscode-proxy:
# ENV CODE_EXTENSIONSDIR=/opt/share/code-server

# Provide the VS Code Marketplace gallery endpoint (EXTENSIONS_GALLERY)
ENV EXTENSIONS_GALLERY='{"serviceUrl":"https://marketplace.visualstudio.com/_apis/public/gallery","itemUrl":"https://marketplace.visualstudio.com/items"}'


# Switch to root for installing system dependencies
USER root

RUN curl -fsSL https://code-server.dev/install.sh | sh && rm -rf .cache \
 && rm -f /usr/local/bin/code-server \
 && ln -s /usr/bin/code-server /usr/local/bin/code-server


RUN apt-get update && apt-get install -y --no-install-recommends \
    libudunits2-dev \
    libpoppler-cpp-dev \
    gdal-bin \
    libgdal-dev \
    libgeos-dev \
    libproj-dev \
    libmagick++-dev \
    libxt6 \
    libxtst6 \
    libssl-dev \
    libprotobuf-dev \
    protobuf-compiler \
    cmake \
    libpoppler-cpp-dev \
    poppler-utils \
    ghostscript \
    tk \
    libxml2-dev \
    libcurl4-openssl-dev \
    liblzma-dev \
    zlib1g-dev \
    texlive-latex-extra \
    texlive-luatex \
    texlive-pictures && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# RUN tlmgr install preview standalone luatex85 pgfplots fancyhdr

RUN echo "copilot-enabled=1" >> /etc/rstudio/rsession.conf
    
# RUN chown -R ${NB_USER}:${NB_USER} /opt/venv

RUN adduser "$NB_USER" sudo && echo '%sudo ALL=(ALL) NOPASSWD:ALL' >>/etc/sudoers

USER ${NB_USER}

RUN echo "PATH: $PATH" && \
    which code-server || find / -type f -name code-server 2>/dev/null | head -20


COPY requirements.txt install.R vscode-extensions.txt /tmp/
RUN xargs -n 1 code-server --extensions-dir ${CODE_EXTENSIONSDIR} --install-extension < /tmp/vscode-extensions.txt

# Install from the requirements.txt file
RUN ls -l /tmp && cat /tmp/requirements.txt && \
    pip install --no-cache-dir --requirement /tmp/requirements.txt && \
    jupyter server extension enable --py nbgitpuller --sys-prefix && \
    Rscript /tmp/install.R

USER root
COPY ./material/ /home/jovyan/work
RUN chown -R ${NB_USER}:users /home/jovyan/work
USER ${NB_USER}

