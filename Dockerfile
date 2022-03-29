# docker/backend/Dockerfile
FROM python:3.10-slim

RUN cd ~

# setup
RUN apt-get update
ARG  jpeg=libjpeg-dev
ARG  ssl=libssl-dev
# ----------------------------------------------------------------------------
RUN apt-get install wget -y
RUN apt-get update && apt-get install -y -q --no-install-recommends \
    build-essential \
    libfontconfig1-dev \
    libfreetype6-dev \
    $jpeg \
    libpng-dev \
    $ssl \
    libx11-dev \
    libxext-dev \
    libxrender-dev \
    fontconfig \
    zlib1g-dev \
    xfonts-75dpi \
    xfonts-base \
    && rm -rf /var/lib/apt/lists/*

RUN wget http://archive.ubuntu.com/ubuntu/pool/main/libj/libjpeg-turbo/libjpeg-turbo8_2.0.6-0ubuntu2_amd64.deb
RUN dpkg -i libjpeg-turbo8_2.0.6-0ubuntu2_amd64.deb

RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.focal_amd64.deb
RUN dpkg -i wkhtmltox_0.12.6-1.focal_amd64.deb
RUN apt --fix-broken install


# set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Setup app config
ENV FLASK_ENV=local

RUN #apt-get install -y wkhtmltopdf

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
#HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=5 \
#CMD curl -f http://localhost:5000/health || exit 1
# run server
CMD ["sh", "./entrypoint-local.sh"]