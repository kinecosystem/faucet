FROM python:3.6-alpine

WORKDIR /opt
COPY . stellar-faucet
WORKDIR stellar-faucet
RUN pip install pipenv 
RUN apk add -qU --no-cache -t .devstuff gcc musl-dev git \
    &&  pipenv install \
    &&  apk del -q .devstuff
EXPOSE 5000
CMD pipenv run gunicorn -w 9 -b 0.0.0.0:5000 main:app  
