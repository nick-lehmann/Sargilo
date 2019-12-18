FROM nicklehmann/poetry:py3.8-latest-alpine

WORKDIR /app

RUN apk add build-base libffi-dev openssl-dev git
COPY . .

WORKDIR /app/sargilo/tests/django30_test_project
RUN poetry install

CMD ["poetry"]
