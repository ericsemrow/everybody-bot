FROM python:3.8-buster

RUN apt-get update && apt-get install -y supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

RUN mkdir /opt/everybody/ && mkdir /opt/storage/

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

ENV PATH="/home/root/.poetry/bin:${PATH}"

WORKDIR /opt/everybody/

COPY . ./

RUN poetry self update
RUN poetry install


CMD ["supervisord"]
