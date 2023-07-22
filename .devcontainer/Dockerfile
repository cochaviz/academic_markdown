FROM pandoc/extra:latest-ubuntu

# packages for devcontainer
RUN apt-get update 
RUN apt-get install --fix-missing
RUN apt-get install -y git 
RUN apt-get install -y curl

WORKDIR /tmp

# python dependencies for build.py
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# install tectonic
RUN curl --proto '=https' --tlsv1.2 -fsSL https://drop-sh.fullyjustified.net | sh
RUN mv tectonic /usr/bin/
RUN wget http://nz2.archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.1f-1ubuntu2.19_amd64.deb
RUN dpkg -i libssl1.1_1.1.1f-1ubuntu2.19_amd64.deb

# install texliveonfly
# RUN tlmgr install texliveonfly

# install wrapper for texliveonfly
# COPY pandoc-texliveonfly.py /usr/bin/
# RUN chmod +x /usr/bin/pandoc-texliveonfly.py

# ENTRYPOINT [ "pandoc-texliveonfly.py" ]
