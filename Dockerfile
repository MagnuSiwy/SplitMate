FROM python:3

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir /app/db

ENV IS_INSIDE_DOCKER=1

EXPOSE 2306

CMD ["gunicorn", "-b", "0.0.0.0:2306", "app:app"]