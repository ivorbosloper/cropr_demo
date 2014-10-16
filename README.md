cropr_demo
==========

Crop-R Demo Application for using the Crop-R API v3

Currently in beta and only running on [Crop-R test server](https://test.crop-r.com/), create your own account there or [contact us](https://www.crop-r.com/contact) for more info

==========
Installation
==========

1. set up virtual env
2. pip install south
3. rename settings.copy to settings.py
4. follow <a href="https://test.crop-r.com/oauth2/tutorial/">the tutorial</a>
5. copy client_id and client_secret to settings.py
6. run ./manage.py syncdb
7. run ./manage.py migrate
8. run ./manage.py runserver
