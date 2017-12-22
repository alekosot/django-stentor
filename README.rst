===============================
Django Stentor
===============================


A newsletter/mailing app for django.

**Currently in Pre-Alpha version. Most functionalities are working but the API is not stable and anything could change at any point.**

Dependencies
------------

* PostgreSQL (stentor uses ``django.contrib.postgres.fields.ArrayField``)
* ``django.contrib.sites``


How to Install
--------------

Install in your virtual environment with:

.. code:: bash

  $ pip install -e git+https://github.com/alxs/django-stentor.git#egg=stentor


How to Use
----------

Add ``'stentor'`` in your INSTALLED_APPS:

.. code:: python

  INSTALLED_APPS = (
    # ...
    'stentor'
    #...
  )

Create the MailingLists that correspond to the names given in the ``STENTOR_DEFAULT_MAILING_LISTS`` setting (``['Website subscribers']`` by default).


Features
--------

* Python 2 / Python 3 compatible
* Admin integration
* Mailing lists
* Subscribers registered on multiple mailing lists
* HTML based emails
* Scheduled sending of newsletters (send in the future)
* Newsletter templates
* Newsletters that can be viewed on the browser (aka web views)
* Tracking of email and web "impressions" of sent newsletters
* Obfuscation backends for publicly visible database values
* Many settings and hooks for tweaking the behavior of the app, with reasonable defaults, so that you don't get lost in configuration.


TODO
----

* Documentation
* Tests
* Better admin integration
* Multilingual newsletters
* Plain text emails
* Template backends
* Hash generator backends
* Tracker backends (i.e. fetch data from a local or a remote app/service)
* Restructure things so that Newsletter becomes a ``Proxy`` model to a more generic Message model. Basically, make this a mailling app and not strictly a newsletter one.
* Add the ability to add content from other models in the newletter/message.
* Newsletters with different authors/sender names and emails
* Make all views class based so that their extension becomes easier.
* Make models as extensible as possible, taking into account the possibility of model subclasses.

**Constant efforts**

* Simplicity, ideally this should be a plug-and-play app
* Configuration/extensibility without sacrificing simplicity (if possible)
* Documentation


License
-------

Free software: BSD license
