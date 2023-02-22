FROM python:3.10

RUN apt-get update -yqq && apt-get install -yqq \
    libgraphviz-dev

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

EXPOSE 8000
ENTRYPOINT ["./docker-entrypoint.sh"]
