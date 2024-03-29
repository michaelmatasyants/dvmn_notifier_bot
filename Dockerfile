FROM python:3.11.4-slim

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

WORKDIR /app

ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser


RUN apt-get update && apt-get install -y python3 && apt-get install -y python3-pip
RUN --mount=type=cache,target=/root/.cache/pip

USER appuser

COPY . /app

# adding port
EXPOSE 3000

CMD ["python3", "main.py"]
