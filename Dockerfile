FROM rocker/binder:no-xdg-set

# this env var is recognized by jupyter-vscode-proxy:
ENV CODE_EXTENSIONSDIR=/opt/share/code-server

# Switch to root for installing system dependencies
USER root
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


RUN curl -L \
  "https://drive.usercontent.google.com/download?id=12y4nqRhPMNso3q_xnxdtO_r--uFnwOYZ&confirm=xxx" \
  -o /tmp/GitHub.copilot-1.370.1783.vsix && \
  /usr/bin/code-server --install-extension /tmp/GitHub.copilot-1.370.1783.vsix && \
  rm /tmp/GitHub.copilot-1.370.1783.vsix

COPY vscode-extensions.txt /tmp/vscode-extensions.txt
RUN xargs -n 1 /usr/bin/code-server --extensions-dir ${CODE_EXTENSIONSDIR}  --install-extension < /tmp/vscode-extensions.txt

# Install from the requirements.txt file
COPY requirements.txt install.R /tmp/
RUN pip install --no-cache-dir --requirement /tmp/requirements.txt
# Install R packages
RUN Rscript /tmp/install.R


