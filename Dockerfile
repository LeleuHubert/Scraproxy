FROM ubuntu
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update &&\
apt-get install -y python3-pip &&\
apt-get install -y python3-lxml &&\
apt-get install -y git &&\
pip3 install cloudscraper &&\
pip3 install -U requests[socks] &&\
apt-get update
WORKDIR home/
RUN git clone https://github.com/LeleuHubert/Scraproxy.git

CMD [ "python3", "-u", "./Scraproxy/scraproxy.py", "(flag)"]
