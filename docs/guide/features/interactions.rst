Interactions
============

Overview
--------

Interactions are ways that a user can engage with data. In Open Budget, this means *Commenting* on an object to start or partake in a discussion, *Starring* an object for later reference from her/his user account, *Following* an object to get updates as changes occur, and *Sharing* an object by broadcasting on social networks or via email.

How it works
~~~~~~~~~~~~

Comment
+++++++

* Only authenticated users can comment
* In the current codebase, only Budget Items and Actual Items can have comments
* Budgets and Actuals can (and will) agregate the comments of their children
* Implemented with a generic foreign key, so adding Comments to new models is trivial

Star
++++

* Only authenticated users can Star
* Starring an item adds it to a user's account page, where this is a list of starred items
* Starred items can be unstarred from the account page, or the view of the object that is starred
* Implemented with a generic foreign key, so adding Stars to new models is trivial

Follow
++++++

** Only basic UI and models are implemented. Sending follow notifications is not. This is not a core feature of this stage of the project **

* Only authenticated users can Follow
* Following an item adds it to a user's account page, where this is a list of followed items
* Followed items can be unfollowed from the account page, or the view of the object that is followed
* Implemented with a generic foreign key, so adding Follows to new models is trivial
* TODO: Logic to know what events on a given object (or related objects to an object) trigger notifications.
* TODO: Actually send notifications
* TODO: The email message for the notifications

Share
+++++

* Implemented with a generic foreign key, so adding comments to new models is trivial
* TODO: Everything else. This is a placeholder for a coming feature

Configuration
-------------

There are no global configuration settings for interactions. Experienced programmers can enable/disable certain features as required, for example, by removing/adding generic relation helpers for commentable objects; or removing Interation template tags from certain templates.

Dependencies
------------

* Django (Comments)

Django Comments
~~~~~~~~~~~~~~~

https://github.com/django/django

Django comes with a bunch of "contrib" apps that provide common web application functionality. The "comments" app is one of those. Our comments are exactly Django Comments.

https://docs.djangoproject.com/en/dev/ref/contrib/comments/

How to import::

    from django.contrib.comments.models import Comment

Example implementation:

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/apps/budgets/models.py

Project Code
------------

Models
~~~~~~

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/apps/interactions/models.py

There is a model for each custom interaction type (comments are elsewhere, as defined by Django).

Each Interaction type subclasses an abstract Interaction model, which defines common interaction fields and methods. For simple "togglable interactions", like "Star" and "Follow", this is enough. Share declares additional fields for broadcast method, and so on.

Views
~~~~~

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/apps/interactions/views.py

Comment Feed
++++++++++++

Comment Feed returns a list of comments in Atom format, for a given object.

This view is exposes to templates that have a comment form, and is in our template that overrides the default Django template for a comment list:

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/commons/templates/comments/list.html

toggleable_interaction
++++++++++++++++++++++

This simple view takes posted data, and either creates or deletes a toggleable interaction object (Star or Follow), depending on the current status of this object/user combination.

URLs
~~~~

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/apps/interactions/urls.py

There is nothing special in the urls.py for interactions.

Templates
~~~~~~~~~

https://github.com/hasadna/omuni-budget/tree/develop/openbudget/apps/interactions/templates/interactions

A collection of partials that are used in various places for Comments, Stars, Follows and Shares.

Template Tags
~~~~~~~~~~~~~

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/apps/interactions/templatetags/interactions.py

Each interaction has a template tag, which includes a widget exposing functionality related to that particular interaction.

star
++++

Adds a form for starring objects to any page it is included in. If the user is not authenticated, the form will not appear. If the user is authenticated, the form will appear and show the current state of relations between this user and this object ("Star" if the object is currently unstarred, "Unstar" if the object is currently starred).

See the detail template for Entities for an example implementation:

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/apps/entities/templates/entities/entity_detail.html

follow
++++++

Adds a form for following objects to any page it is included in. If the user is not authenticated, the form will not appear. If the user is authenticated, the form will appear and show the current state of relations between this user and this object ("Follow" if the object is currently unfollowed, "Unfollow" if the object is currently followed).

See the detail template for Entities for an example implementation:

https://github.com/hasadna/omuni-budget/blob/develop/openbudget/apps/entities/templates/entities/entity_detail.html
