# docker image build -t jupyter-notebook-01 .
# docker run -v "$(pwd):/home/jovyan/CPU" -p 18888:8888 --name jupyter-notebook-01 jupyter-notebook-01

FROM jupyter/base-notebook:python-3.7.4

COPY --chown=jovyan:users requirements_dev.txt /tmp/

USER root
RUN sudo apt-get update
RUN sudo apt-get install -y libpq-dev
RUN sudo apt-get install -y gcc
RUN sudo apt-get install -y htop

RUN pip install --requirement /tmp/requirements_dev.txt && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER

RUN pip install --index-url https://test.pypi.org/simple/ \
    --extra-index-url https://pypi.org/simple \
    pgload==0.1.7

RUN ln -sv /home/jovyan/CPU /mnt/ns01

# pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple pgload==0.1.7
