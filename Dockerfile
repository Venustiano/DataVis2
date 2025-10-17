FROM rocker/binder:4.4.2

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
    zlib1g-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN tlmgr install preview standalone luatex85 pgfplots fancyhdr

RUN echo "copilot-enabled=1" >> /etc/rstudio/rsession.conf
    
RUN chown -R ${NB_USER}:${NB_USER} /opt/venv


# Install from the requirements.txt file
COPY requirements.txt install.R /tmp/
RUN pip install --no-cache-dir --requirement /tmp/requirements.txt
# Install R packages
RUN Rscript /tmp/install.R


USER ${NB_USER}
