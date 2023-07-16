FROM pandoc/extra:latest-ubuntu

# packages for devcontainer
RUN apt install -y git

WORKDIR /tmp

# python dependencies for build.py
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
