FROM ubuntu:latest

RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install \
    flask \
    flask-api \
    flask-restful \
    flask-restful-swagger \
    flask-sqlalchemy \
    IPy \
    mock \
    SQLAlchemy
ADD rest_server /root/
RUN echo 'export PS1="\[\033[38;5;88m\]\[\033[48;5;22m\]REST-DOCKER\[\e[m\]:\W\\$ "' >> /root/.bashrc
WORKDIR /root

