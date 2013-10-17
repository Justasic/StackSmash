===========
StackSmash
===========


To install:
===========

Generic:
--------
1. install python 2.7.*
2. go to djangoproject.org and download the latest version, setup, and install or use python pip to install it (also on django's download page)
3. install docutils and pygments (pip install pygments && pip install docutils)
4. install your favorite database software (I use PostgreSQL)
5. setup the settings.py file for your specific installation as well as generate a new django secret (you can use `this site`_ for a new secret)
6. Run ``./manage.py syncdb`` to initialize the database with the needed tables

Ubuntu/Debian:
--------------
1. sudo apt-get install python python-pygments python-docutils

2. go to djangoproject.org and download the latest version, setup, and install or use python pip to install it (also on django's download page)
3. install your favorite database software (I use PostgreSQL)
4. setup the settings.py file for your specific installation as well as generate a new django secret (you can use `this site`_ for a new secret)
5. Run ``./manage.py syncdb`` to initialize the database with the needed tables


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

