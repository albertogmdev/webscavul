FROM python:3.11

ENV PYTHONUNBUFFERED=1

WORKDIR /webscavul/app

COPY requirements.txt .
RUN chmod +r requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 80

COPY . .

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "80"]