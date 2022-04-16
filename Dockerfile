FROM python:alpine

RUN apk update
RUN apk add git

RUN pip install --upgrade pip

RUN adduser -D bot
USER bot
WORKDIR /home/bot

RUN pip install --user --no-cache-dir pipenv

ENV PATH="/home/bot/.local/bin:${PATH}"

COPY --chown=bot:bot Pipfile Pipfile
RUN pipenv install --system

COPY --chown=bot:bot . .

CMD [ "python", "main.py" ]