# Stage 1 - up-to-date ubuntu base #############################################
FROM ubuntu:18.04 AS base-environment

# avoid hangs on packages like tzdata
ARG DEBIAN_FRONTEND=noninteractive

RUN apt update && \
    apt -y upgrade && \
    apt -y dist-upgrade && \
    apt -y autoclean && \
    apt -y autoremove

# Stage 2 - package installation ###############################################
FROM base-environment AS packages-installed

ARG DEBIAN_FRONTEND=noninteractive

RUN apt -y install python3 python3-pip postgresql postgis libpq-dev locales

# fix locales for postgres
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen

ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8 

# Stage 3 python environment setup #############################################
FROM packages-installed AS python-environment

# Pip installs done here *before* adding the rest of the files, so that docker
# cache can better be utilized, and the pip installs don't have to run every
# time any one source file has been modified
COPY ./requirements.txt /map_api/requirements.txt
RUN pip3 install -r /map_api/requirements.txt

COPY . /map_api

WORKDIR /map_api


# Stage 4 set up database ######################################################
FROM python-environment AS database-setup

USER postgres

WORKDIR /map_api

RUN service postgresql restart && psql < /map_api/data/storymap.sql

# Stage 5 closing config #######################################################
FROM database-setup AS final-setup
EXPOSE 5000

CMD ["./bootstrap.sh"]
