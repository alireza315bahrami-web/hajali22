FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir python-telegram-bot[job-queue]
CMD ["python", "HajAli.py"]
