FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive 

RUN apt-get -q update && \
    apt-get purge -q -y snapd lxcfs lxd ubuntu-core-launcher snap-confine && \
    apt-get -q -y install \
        file wget cpio rsync locales \
        build-essential libncurses5-dev python3-setuptools \
        python3-dev python3-pip python3-dbus python3-gi \
        python3-protobuf protobuf-compiler \
        git bzr cvs mercurial subversion libc6 unzip bc \
        vim ccache && \
    apt-get -q -y autoremove && \
    apt-get -q -y clean && \
    update-locale LC_ALL=C

# Configure ccache
RUN mkdir -p /root/.ccache && \
    echo "max_size = 50.0G" > /root/.ccache/ccache.conf && \
    echo "compression = true" >> /root/.ccache/ccache.conf && \
    echo "compression_level = 1" >> /root/.ccache/ccache.conf

VOLUME /app/buildroot/dl
VOLUME /app/buildroot/output
VOLUME /root/.ccache

CMD /bin/bash
