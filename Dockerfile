FROM ubuntu:latest

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

RUN apt-get update &&  apt-get upgrade -y && apt-get install -qqy \
wget \
bzip2 \
libssl-dev \
openssh-server

# also commented out because we're not using the frontend:
# RUN apt-get install nodejs npm -y

RUN echo 'export PATH=/opt/miniconda/bin:$PATH' > /etc/profile.d/conda.sh && \
    wget --quiet https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/miniconda && \
    rm ~/miniconda.sh

# SSH Configuration start
RUN mkdir /var/run/sshd
RUN echo 'root:screencast' | chpasswd
RUN sed -i '/PermitRootLogin/c\PermitRootLogin yes' /etc/ssh/sshd_config


# SSH authentication fix. Otherwise users is kicked off after authentication
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile
# End SSH

RUN mkdir -p /app && \
mkdir -p /scripts && \
mkdir -p /media-files && \
mkdir -p /static-files

COPY ./app/requirements.yml /app/requirements.yml

RUN /opt/miniconda/bin/conda env create -f /app/requirements.yml
ENV PATH /opt/miniconda/envs/app/bin:$PATH

COPY ./app /app
COPY scripts /scripts
RUN chmod +x /scripts/*

WORKDIR /app

EXPOSE 8000
EXPOSE 22