# Using torchnlp via Docker

This directory contains `Dockerfile.gpu`s to make it easy to get up and running with
tensor2tensor via [Docker](http://www.docker.com/).

## Installing Docker

General installation instructions are
[on the Docker site](https://docs.docker.com/installation/), or some quick links here:

* [OSX](https://www.docker.com/products/docker#/mac)
* [Ubuntu](https://docs.docker.com/engine/installation/linux/ubuntulinux/)

# Build docker image
- CPU
> docker build -t tensor2tensor:tf-1.12.0-py3 -f Dockerfile .

- GPU
> docker build -t tensor2tensor:tf-1.12.0-gpu-py3 -f Dockerfile.gpu .

# Run docker

For GPU support install NVidia drivers (ideally latest) and
[nvidia-docker](https://github.com/NVIDIA/nvidia-docker). Run using

- CPU
> nvidia-docker run -ti tensor2tensor:tf-1.12.0-py3

- GPU
> nvidia-docker run -ti tensor2tensor:tf-1.12.0-gpu-py3