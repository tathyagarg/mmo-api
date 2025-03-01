FROM python:3.12

WORKDIR /mmo-api

COPY ./requirements.txt /mmo-api/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /mmo-api/requirements.txt

COPY ./mmo /mmo-api/mmo
COPY ./docs /mmo-api/docs
COPY ./mcurl /mmo-api/mcurl
COPY ./.env /mmo-api/.env

CMD ["fastapi", "run", "mmo/main.py", "--port", "36607"]
