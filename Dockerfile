FROM python:3.8.2-alpine

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

VOLUME ["/app/database/db", "/app/images", "/app/dataset", "/app/train"]

CMD [ "python", "./app.py" ]