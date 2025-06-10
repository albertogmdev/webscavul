FROM python:3.13

ENV PYTHONUNBUFFERED=1

WORKDIR /webscavul

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 80

COPY . .

CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "80"]