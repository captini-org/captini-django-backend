FROM python:3.10

RUN apt-get update -yqq && apt-get install -yqq \
    libgraphviz-dev

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
COPY ./recordings/lessons/ ./lessons
COPY ./recordings/topics/ ./topics
# COPY ./recordings/user/profile_photos/profile.jpg ./profile.jpg
EXPOSE 8000
ENTRYPOINT ["./docker-entrypoint.sh"]
