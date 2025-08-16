FROM python:3.12-bookworm

ENV PYTHONUNBUFFERED=1

WORKDIR /webscavul/api

COPY ./requirements.txt .

# Dependencias del sistema y Playwright
RUN apt-get update && apt-get install -y wget gnupg ca-certificates && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    playwright install-deps && \
    playwright install

COPY . .

EXPOSE 80

CMD ["uvicorn", "main:api", "--host", "0.0.0.0", "--port", "80", "--reload", "--reload-dir", "."]