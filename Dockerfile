FROM python:3

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENV IS_INSIDE_DOCKER 1

EXPOSE 5000

CMD ["python", "/app/app.py"]