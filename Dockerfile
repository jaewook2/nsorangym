FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
ENV log_level_e2sim=info

# 기본 패키지 설치
RUN apt-get update && apt-get install -y \
    build-essential git cmake libsctp-dev autoconf automake libtool bison flex \
    libboost-all-dev g++ python3 python3-pip python3-venv \
    pkg-config libeigen3-dev sqlite3 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

# ----------------------------------
# E2SIM 설치
# ----------------------------------
RUN git clone https://github.com/jaewook2/nsorangym_e2sim /workspace/e2sim

RUN mkdir -p /workspace/e2sim/e2sim/build
WORKDIR /workspace/e2sim/e2sim/build
RUN cmake .. -DDEV_PKG=1 -DLOG_LEVEL=${log_level_e2sim} \
    && make package \
    && dpkg --install ./e2sim-dev_1.0.0_amd64.deb \
    && ldconfig

# ----------------------------------
# ns-3 + oran-interface 설치
# ----------------------------------
WORKDIR /workspace
RUN git clone https://github.com/jaewook2/nsorangym_mmwave /workspace/ns3-mmwave-oran
RUN git clone https://github.com/jaewook2/nsorangym_nsoran /workspace/ns3-mmwave-oran/contrib/oran-interface

WORKDIR /workspace/ns3-mmwave-oran
RUN ./ns3 configure --enable-examples --enable-tests
RUN ./ns3 build
# ----------------------------------
# Python 패키지 + hatch + nsoranGym 설치
# ----------------------------------
WORKDIR /workspace
RUN pip install "numpy<2" hatch --break-system-packages


RUN git clone https://github.com/jaewook2/nsorangym_gym /workspace/nsorangym_gym
WORKDIR /workspace/nsorangym_gym
RUN hatch build
RUN pip install dist/*.tar.gz --break-system-packages






# ----------------------------------
# Default command
# ----------------------------------
CMD [ "/bin/bash" ]
