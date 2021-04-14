ARG IMAGE_TAG="python3.8-alpine3.10"

# Build dependencies in separate container
FROM tiangolo/uvicorn-gunicorn:${IMAGE_TAG} AS builder
ENV WORKDIR /app
COPY Pipfile ${WORKDIR}/
COPY Pipfile.lock ${WORKDIR}/

RUN apk add --update postgresql-dev gcc python3-dev musl-dev

RUN cd ${WORKDIR} \
    && pip install pipenv \
    && pipenv install --system

# Create the final container with the app
FROM tiangolo/uvicorn-gunicorn:${IMAGE_TAG}

RUN apk add --update libpq

ENV USER=docker \
    GROUP=docker \
    UID=12345 \
    GID=23456 \
    HOME=/app \
    PYTHONUNBUFFERED=1
WORKDIR ${HOME}

# Create user/group
RUN addgroup --gid "${GID}" "${GROUP}" \
    && adduser \
    --disabled-password \
    --gecos "" \
    --home "$(pwd)" \
    --ingroup "${GROUP}" \
    --no-create-home \
    --uid "${UID}" \
    "${USER}"

# Run as docker user
USER ${USER}
# Copy installed packages
COPY --from=builder /usr/local/lib/python3.7/site-packages /usr/local/lib/python3.7/site-packages
# Copy the application
COPY --chown=docker:docker . .
# Collect the static files
RUN python manage.py collectstatic --noinput