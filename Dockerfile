FROM python:3.7
LABEL maintainer="ChangSeok Lee"

ENV PYTHONUNBUFFERD 1
ENV TZ=Asia/Seoul
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update && apt-get install -y \
    libspdlog-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code

ADD requirements.txt /code/
RUN pip install -r requirements.txt

ADD . /code/

EXPOSE 8000

CMD ["./scripts/start.sh"]