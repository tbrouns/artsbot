# Build an image that can do training and inference in SageMaker
# This is a Python 3 image that uses the nginx, gunicorn, flask stack
# for serving inferences in a stable way.

FROM nvidia/cuda:11.4.0-base-ubuntu20.04

MAINTAINER t.s.n.brouns@gmail.com

# 1. Define the packages required in our environment.
RUN apt-get -y update && apt-get install -y --no-install-recommends \
         wget \
         python3 \
         nginx \
         ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get -y update && apt-get install -y python3-pip

# 2. Here we define all python packages we want to include in our environment.
# Pip leaves the install caches populated which uses a significant amount of space.
# These optimizations save a fair amount of space in the image, which reduces start up time.
COPY requirements.txt .
RUN pip install -r requirements.txt

# 3. Set some environment variables. PYTHONUNBUFFERED keeps Python from buffering our standard
# output stream, which means that logs can be delivered to the user quickly. PYTHONDONTWRITEBYTECODE
# keeps Python from writing the .pyc files which are unnecessary in this case. We also update
# PATH so that the train and serve programs are found when the container is invoked.

ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE
ENV PATH="/opt/program:${PATH}"

# 4. Define the folder (sentiment_analysis) where our inference code is located
COPY deploy model.py config.ini config.py /opt/program/
RUN mkdir /opt/program/utils
COPY utils /opt/program/utils
WORKDIR /opt/program