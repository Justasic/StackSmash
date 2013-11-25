===========
StackSmash
===========


To install:
===========

Generic:
--------
1. install python 2.7.* or python 3.*
2. go to djangoproject.org and download the latest version, setup, and install or use python pip to install it (also on django's download page)
3. install docutils, pygments, and recaptcha-client (pip install pygments && pip install docutils && pip install recaptcha-client)
4. install your favorite database software (I use PostgreSQL)
5. setup the settings.py file for your specific installation
6. Create the file ~/.django_secret and generate a new django secret (you can use `this site`_ for a new secret)
7. Create the file ~/.django_db and setup your db settings. the following are available:
	user=<username>
	passwd=<password>
	host=<hostname of database server - optional>
	port=<port of database server - optional>
8. Run ``./manage.py syncdb`` to initialize the database with the needed tables

Ubuntu/Debian:
--------------
1. sudo apt-get install python python-pygments python-docutils python-recaptcha-client
2. go to djangoproject.org and download the latest version, setup, and install or use python pip to install it (also on django's download page)
3. follow steps 4 to 8 above

.. _`this site`: http://www.miniwebtool.com/django-secret-key-generator/


To Run:
=======

Choose your favorite web server and research how to install and run django under it.
If you use fastcgi you will need python's flup library (sudo apt-get install python-flup on debian systems)


Notes:
======

If you are using Django admin and nginx (like I am), you will need to use the following config as well as find your admin static pages in the python dist-packages directory somewhere on your server.

You can find the exact file path for this with the following command:

``python -c "import sys; sys.path = sys.path[1:]; import django; print(django.__path__[0]+\"/contrib/admin/static/admin/\")"``

replace the ``location /static/admin`` alias with the output from the command above.

Nginx config:
-------------

::

 server {
	listen 80;
	
	root /var/www/;
	
	location /static/admin {
		# Replace the below alias with the output from the command above
		alias /usr/local/lib/python2.7/dist-packages/django/contrib/admin/static/admin/;
	}
	
	location /static {
		alias /var/www/StackSmash/StackSmash/static/;
	}
	
	
	location / {
		include fastcgi_params;
		fastcgi_split_path_info ^()(.*)$;
		fastcgi_pass 127.0.0.1:3000;
	}
 }

