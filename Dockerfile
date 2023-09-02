# builder image
# note only 2 files are needed for compiling the version lock
FROM python:3.11-slim AS builder

RUN pip install poetry==1.5.1

WORKDIR /build
ADD pyproject.toml poetry.lock ./

RUN poetry export -f requirements.txt -o requirements.txt

# production image
FROM python:3.11-alpine as runtime

COPY --from=builder /build/requirements.txt .

RUN set -eux; \
    export PYTHONDONTWRITEBYTECODE=1; \
    pip install \
    --no-cache-dir \
    --requirement requirements.txt; \
    rm requirements.txt;

WORKDIR /app
COPY pyproject.toml ./
COPY midjourney_api ./midjourney_api