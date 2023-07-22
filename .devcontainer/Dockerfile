FROM pandoc/extra:latest-ubuntu

# packages for devcontainer
RUN apt-get update 
RUN apt-get install -y git 
RUN apt-get install -y python-is-python3

WORKDIR /tmp

# python dependencies for build.py
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# install texliveonfly
RUN tlmgr install texliveonfly

# install wrapper for texliveonfly
COPY .devcontainer/pandoc-texliveonfly.py /usr/bin/
RUN chmod +x /usr/bin/pandoc-texliveonfly.py

ENTRYPOINT [ "pandoc-texliveonfly.py" ]
