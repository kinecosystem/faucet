FROM python:3.6-alpine

COPY . /opt/stellar-faucet
WORKDIR /opt/stellar-faucet
RUN pip install pipenv 
RUN apk add -qU --no-cache -t .devstuff gcc musl-dev git \
    &&  pipenv install \
    &&  apk del -q .devstuff
EXPOSE 5000
CMD pipenv run gunicorn -w $SEEDS_NUMBER -b 0.0.0.0:5000 main:app
