#!/bin/bash
source /usr/local/bin/virtualenvwrapper.sh
workon drftest
cd /home/drftest/drftest/
./manage.py migrate
./manage.py initshopdb
./manage.py runserver
