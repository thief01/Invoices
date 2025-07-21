FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
   gcc \
   && rm -rf /var/lib/apt/lists/*


COPY req /app/req


RUN pip install --no-cache-dir -r req


COPY . .


EXPOSE 8001

CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]

