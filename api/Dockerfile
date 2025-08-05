FROM python:3.13

ENV PYTHONUNBUFFERED=1

WORKDIR /webscavul/api

COPY ./requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

RUN playwright install
RUN playwright install-deps

EXPOSE 80

COPY . .

CMD ["uvicorn", "main:api", "--host", "0.0.0.0", "--port", "80", "--reload", "--reload-dir", "."]