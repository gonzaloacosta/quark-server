ARG PYTHON_IMAGE_VERSION=3.7-slim
ARG VERSION=0.0.1
FROM python:$PYTHON_IMAGE_VERSION
FROM python:3.7-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt && \
  python init_db.py
ENV VERSION $VERSION
CMD ["python", "server.py"]
EXPOSE 80

