Accounts
========

Overview
--------

Open Budget supports user accounts. Several features, such as sharing to social networks, and commenting, require the user to have an account and to be authenticated.

User accounts are based on Django's built in auth.User, and take advantage of Django 1.5's new custom user model implementation.

Configuration
-------------

All configuration of Open Budget accounts is done via the project settings:

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/settings/base.py

The default settings look something like this::

    # openbudget.settings.base.py
    ACCOUNT_ACTIVATION_DAYS = 7
    AUTH_USER_MODEL = 'accounts.Account'
    LOGIN_URL = '/accounts/login/'
    LOGIN_REDIRECT_URL = '/'
    LOGOUT_URL = '/accounts/logout/'
    ABSOLUTE_URL_OVERRIDES = {
        'auth.user': lambda u: '/accounts/{uuid}/'.format(uuid=u.uuid)
    }

In the vast majority of cases, you would not expect to modify any of these settings, except perhaps ACCOUNT_ACTIVATION_DAYS, which sets how long as activation token is valid for after a user registers.

Dependencies
------------

Open Budget accounts depend on the following 3rd party packages:

* django
* registration

Django
~~~~~~

https://github.com/django/django

Django comes with a bunch of "contrib" apps that provide common web application functionality. The "auth" app is one of those, and our accounts sit on this.

https://docs.djangoproject.com/en/1.5/ref/contrib/auth/#user

https://docs.djangoproject.com/en/dev/topics/auth/customizing/#auth-custom-user

How to import::

    from django.contrib.auth import get_user_model

Example implementation:

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/apps/accounts/models.py

Registration
~~~~~~~~~~~~

https://bitbucket.org/ubernostrum/django-registration

https://bitbucket.org/prjts/django-registration

django-registration is a widely used 3rd party app for Django that provides a user registration framework.

Functionality includes managing registration confirmation via tokens, full integration with the Django User model, and pluggable backends to write custom registration flow functionality with ease.

We are currently using our own fork of django-registration due to bugs in its new Django 1.5 support.

Information about our changes can be found here:

https://bitbucket.org/prjts/django-registration/commits/ba31fc3053bfca7eb7a19d912882e50e295adc55

https://bitbucket.org/prjts/django-registration/commits/1cddccb187ed865fd28599f0de2cc063cfa8c55a

https://bitbucket.org/ubernostrum/django-registration/pull-request/41/removed-dependency-on-django-during/diff

https://groups.google.com/forum/?fromgroups=#!topic/django-users/P6DA7PvDVzs


How to import::

    from registration.backends.default import urls as registration_urls

Example implementation:

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/apps/accounts/urls.py

Project Code
------------

Models
~~~~~~

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/apps/accounts/models.py

Account
+++++++

The Account model is configured as Django's AUTH_USER_MODEL, thus extending the built in auth.User.

See the Django docs for specifics on how this works in Django:

https://docs.djangoproject.com/en/dev/topics/auth/customizing/#auth-custom-user

On top of all the properties of the default auth.User model, we have a language field, and a bunch of methods to get to other objects in the Open Budget codebase.

Proxies
+++++++

Proxy Models are an excellent feature of Django, allowing the developer to customize an interface over a model with ease.

We make use of Proxy Models on user accounts in the admin, to separate the different types of users we have into distinct entities in the admin.

Forms
~~~~~

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/apps/accounts/forms.py

AccountForm
+++++++++++

The form used to update a user's account details.

Views
~~~~~

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/apps/accounts/views.py

AccountDetailView
+++++++++++++++++

Simply returns a view of the user's account page. This page is only visible to the to the user (via the LoginRequired and UserDataObject mixins).

AccountUpdateView
+++++++++++++++++

Return a form over the user's account, so the user can update account details. This page is only visible to the to the user (via the LoginRequired and UserDataObject mixins).

URLs
~~~~

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/apps/accounts/urls.py

The main thing to note in the account urls is that we include django-registration urls, and let it handle all common auth views. We then add additional views for the User's account detail and account update pages.


Templates
~~~~~~~~~

https://github.com/hasadna/omuni-budget/tree/develop/openbudget/commons/templates/registration

We provide templates for all authentication/registration views.
