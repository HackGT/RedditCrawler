FROM ubuntu:latest

RUN apt-get update && apt-get install -y supervisor python-pip
RUN mkdir -p /var/log/supervisor
RUN mkdir -p /var/log/reddit-crawler
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

ARG APP_PATH=/usr/src/reddit-crawler
WORKDIR $APP_PATH

ADD requirements.txt $APP_PATH
RUN pip install -r requirements.txt
COPY . /usr/src/reddit-crawler

CMD ["/usr/bin/supervisord","-c","/etc/supervisor/conf.d/supervisord.conf"]
