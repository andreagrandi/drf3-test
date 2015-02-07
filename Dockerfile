FROM ubuntu:14.04
MAINTAINER Andrea Grandi <a.grandi@gmail.com>

# Install basic Ubuntu packages for development
RUN apt-get update -y && apt-get install -y python-dev build-essential python-pip \
    libcurl4-gnutls-dev python2.7-dev libpq-dev

# Add drftest user
RUN groupadd -g 1001 drftest
RUN useradd -m -s /bin/bash -u 1001 -g 1001 drftest

# Deploy source code
ADD drftest /home/drftest/drftest/
ADD requirements.txt /home/drftest/drftest/
ADD docker/run.sh /home/drftest/drftest/
RUN chmod +x /home/drftest/drftest/run.sh
RUN chown -R drftest /home/drftest/drftest/
RUN chgrp -R drftest /home/drftest/drftest/

# Configure virtualenv
RUN pip install virtualenv virtualenvwrapper uwsgi
RUN mkdir -p /home/drftest/.virtualenvs
ENV WORKON_HOME /home/drftest/.virtualenvs
RUN /bin/bash -c "source /usr/local/bin/virtualenvwrapper.sh \
    && mkvirtualenv drftest \
    && workon drftest \
    && pip install -r /home/drftest/drftest/requirements.txt"

USER drftest
EXPOSE 8000
WORKDIR /home/drftest/drftest/
CMD ['run.sh']
