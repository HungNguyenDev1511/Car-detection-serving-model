# Dockerfile.mlflow
FROM python:3.9-slim

RUN pip install mlflow

CMD ["mlflow", "server", "--host", "0.0.0.0", "--port", "5000"]