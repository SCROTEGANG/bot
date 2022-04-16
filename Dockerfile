FROM python:alpine

RUN apk --no-cache upgrade
RUN apk add git

RUN pip install --upgrade pip

RUN adduser -D dilf
USER dilf
WORKDIR /home/dilf

RUN pip install --user pipenv
ENV PATH="/home/dilf/.local/bin:${PATH}"

COPY --chown=dilf:dilf ./Pipfile ./Pipfile.lock ./
RUN pipenv install --system

COPY --chown=dilf:dilf ./ ./

CMD [ "python", "main.py" ]