ARG PYTHON_IMAGE_VERSION=3.9

ARG VERSION=0.0.2

FROM python:$PYTHON_IMAGE_VERSION

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt && \
  python init_db.py && \
  useradd --no-create-home quark && \
  chmod +x /app/entrypoint.sh && \
  chown -R quark:quark /app

ENV VERSION $VERSION

CMD ["/bin/sh", "-c", "/app/entrypoint.sh"]

USER quark

EXPOSE 8080

