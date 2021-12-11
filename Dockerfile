# Dockerfile for Collision Predictor project
# Author: MDS-2021-22 block3 group21
# Date: 2021-12-09

FROM jupyter/scipy-notebook

# Install Python 3 packages
RUN conda install -c conda-forge --quiet --yes \
    'altair==4.1.*' \
    'altair_saver==0.5.*' \
    'imbalanced-learn==0.8.*' \
    'pandas==1.3.*' \
    'pandoc==2.16.*' \
    'scikit-learn==1.0.*' \
    'pip'

RUN pip install docopt-ng==0.7.2

USER root    
    
# R pre-requisites
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    fonts-dejavu \
    unixodbc \
    unixodbc-dev \
    r-cran-rodbc \
    gfortran \
    gcc && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install R packages
RUN conda install -c conda-forge --quiet --yes \
    'r-base=4.0.3' \
    'r-tidyverse=1.3*' \
    'r-rmarkdown=2.5*' \
    'r-knitr=1.36.*' \
    'r-kableExtra=1.3.*' \
    && \
    conda clean --all -f -y && \
    fix-permissions "${CONDA_DIR}"
