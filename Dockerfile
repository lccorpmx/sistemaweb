FROM python:3
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN mkdir /sistemaweb
WORKDIR /sistemaweb
COPY requirements.txt /sistemaweb/
RUN pip install -r requirements.txt
COPY . /sistemaweb/
