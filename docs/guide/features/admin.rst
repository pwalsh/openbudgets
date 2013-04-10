Admin
=====

The goal of any admin is to make it easy for content editors, not developers, to add content to a system. By default, the Django admin does not deliver on this promise, but it provides a foundation to build on.

First, we are using the excellent Grappelli_ app as our admin framework, overriding the default Django Admin. Grappelli gives us a more user-friendly UI "out of the box", and a nicer API for customizing Django Admin behaviour.

In addition, we have added some tweaks to make Grappelli play nicer with RTL language display, and with the modeltranslations app, and some of our own custom views. We also make extensive use of ProxyModels_ to simplify the admin interface for content editors.

If you contribute code that should be exposed in some way to the admin, please consider the end user - the content editor, and use Proxy Models or whatever else is required to make their lives easier.

**An example of using a Proxy Model**

A great example when to use a Proxy Model is the standard User/UserProfile dance in Django.

It is far from intuitive for a content editor to have two objects in the admin for what should be "one thing" - the User. Use Proxy Models and win. See our examples in account.models and account.admin.

.. _Grappelli: https://django-grappelli.readthedocs.org/en/latest/
.. _ProxyModels: https://docs.djangoproject.com/en/dev/topics/db/models/#proxy-models
