FROM python:3.11.5

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
