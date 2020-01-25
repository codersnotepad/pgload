# docker build -t pgload-dev-01 .
# docker run -v "$(pwd):/opt/app/pgload" --name pgload-dev-01 -d pgload-dev-01 /bin/sh -c "while true; do ping 8.8.8.8; sleep 30; done"
# docker run -v "$(pwd):/home/jovyan/" -p 18888:8888 --name base-notebook-01 jupyter/base-notebook:python-3.7.4

FROM python:3.7.6-buster

COPY requirements_dev.txt /opt/app/requirements_dev.txt
WORKDIR /opt/app
RUN pip install -r requirements_dev.txt
