FROM python:3.9-slim-buster
WORKDIR /app
COPY requirements.txt fib.py .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5001

CMD ["python", "fib.py"]
