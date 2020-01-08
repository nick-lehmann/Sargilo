FROM nicklehmann/poetry:py3.5-preview-alpine

# Install native dependencies
RUN apk add build-base libffi-dev openssl-dev git

WORKDIR /app

# Copy both pyproject.toml files and all files referenced in them (e.g. README)
COPY sargilo/tests/django111_test_project/pyproject.toml sargilo/tests/django111_test_project/
COPY pyproject.toml README.md ./

# Install only dependencies
WORKDIR /app/sargilo/tests/django111_test_project/
RUN poetry install

# Copy the full source code
WORKDIR /app
COPY . .

# Change back to test project
WORKDIR /app/sargilo/tests/django111_test_project/

# Bring manage.py of test project into path
RUN ln -s /app/sargilo/tests/django111_test_project/manage.py /usr/local/bin/manage.py \
    && chmod +x /usr/local/bin/manage.py

CMD ["manage.py", "test", "sargilo.tests.blog"]
