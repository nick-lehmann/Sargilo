FROM nicklehmann/poetry:py2.7-latest-alpine

WORKDIR /app

RUN apk add build-base libffi-dev openssl-dev git
COPY . .

WORKDIR /app/sargilo/tests/django14_test_project
RUN poetry install

CMD ["poetry"]
