# brp_demo Harvest

# We are using wheezy here because openjdk-6 is not yet stable on jessie
# python 2.7.9 does weird things with SSL so we'll stick with 2.7.8
FROM python:2.7.8-wheezy


MAINTAINER Tyler Rivera "riverat2@email.chop.edu"

RUN apt-get update -qq
RUN apt-get install -y openjdk-6-jre\
    libjansi-java\
    build-essential\
    git-core\
    libldap2-dev\
    libpq-dev\
    libsasl2-dev\
    libssl-dev\
    libxml2-dev\
    libxslt1-dev\
    libffi-dev\
    openssl\
    python-dev\
    python-setuptools\
    wget\
    zlib1g-dev\
    postgresql-client

# Scala needed for DataExpress scripts
RUN curl -O http://www.scala-lang.org/files/archive/scala-2.9.3.deb
RUN dpkg -i scala-2.9.3.deb
RUN apt-get update
RUN apt-get install -y scala zip

# Python dependencies
RUN pip install "git+http://github.com/tjrivera/csvkit.git"
RUN pip install "Django>=1.4.11,<1.6"
RUN pip install "Markdown"
RUN pip install "uWSGI"
RUN pip install "Fabric"
RUN pip install "avocado>=2.3.0,<2.4"
RUN pip install "serrano>=2.3.0,<2.4"
RUN pip install "modeltree>=1.1.7,<1.2"
RUN pip install "git+https://github.com/tjrivera/django-haystack.git@hotfix#egg=django-haystack"
RUN pip install "python-memcached==1.53"
RUN pip install "psycopg2"
RUN pip install "whoosh>=2.5"
RUN pip install "git+https://github.com/sburns/PyCap.git#egg=redcap"
RUN pip install "django-environ"
RUN pip install "python-etcd"
RUN pip install "raven"
RUN pip install "python-social-auth"
RUN pip install "south>=1.0"

# Add application files
RUN mkdir /opt/app
ADD . /opt/app/

ENV APP_NAME brp_demo
ENV APP_ENV test

# Ensure all python requirements are met
RUN pip install -r /opt/app/requirements.txt

WORKDIR /opt/app

CMD ["/opt/app/scripts/run.sh"]

EXPOSE 8000
