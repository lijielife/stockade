stockade
========
Open-source password management interface for sharing credentials between multiple users.

Functionality slated to include:
* CRUD for projects - a project can have multiple sets of credentials
* CRUD for credentials - credentials are associated to a single project
* Authentication of users - prevents unauthorized users from accessing credentials
* Role Based Access Control
  * Admin users can add admin and regular users to a project, can perform CRUD operations on project and secrets
  * Regular users have access to project and can perform CRUD on secrets
  
Uses Barbican back end to obscure secret data - more information on Barbican can be found in the cloudkeep/barbican wiki.

To run cd to the stockade directory and then:

* Create a venv
* pip install -r tools/requirements.txt
* python manage.py syncdb
* python manage.py runserver


**Note** - If you have problems installing the requirements, you might need to install the ldap2 and sasl2 headers.

On Ubuntu:

```
sudo apt-get install libldap2-dev libsasl2-dev
```
