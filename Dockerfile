FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
# COPY requirements.txt requirements.txt
# RUN pip3 install --default-timeout=1000 -r requirements.txt

RUN pip3 install pipenv
# -- Adding Pipfiles
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
# -- Install dependencies:
RUN set -ex && pipenv install --deploy --system

COPY . /app
ENV PYTHONPATH=/app