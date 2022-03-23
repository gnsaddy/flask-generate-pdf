# docker/backend/Dockerfile
FROM python:3.10-slim
# set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Setup app config
ENV FLASK_ENV=local

# setup
RUN apt-get update
RUN apt-get install -y wkhtmltopdf
RUN pip install pdfkit
RUN apt-get autoremove && apt-get clean
RUN pip install --upgrade pip
RUN pip install gunicorn

ADD . /usr/src/app
# add requirements (to leverage Docker cache)
ADD ./requirements.txt /usr/src/app/requirements.txt
# install requirements
RUN python -m pip install --upgrade pip
RUN pip install --no-cache -r requirements.txt
RUN pip freeze > requirements.txt

# add entrypoint.sh
ADD ./entrypoint-local.sh /usr/src/app/entrypoint-local.sh
# execute permission to entrypoint
RUN chmod +x ./entrypoint-local.sh
# add app
EXPOSE 5000
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=5 \
CMD curl -f http://localhost:5000/health || exit 1
# run server
CMD ["sh", "./entrypoint-local.sh"]