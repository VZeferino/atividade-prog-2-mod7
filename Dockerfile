FROM python:3.9

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
COPY ./templates /app/templates
COPY ./static /app/static

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
