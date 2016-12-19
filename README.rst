===============================
Django Stentor
===============================


A newsletter/mailing app for django.

**Currently in Pre-Alpha version. Most functionalities are working but the API is not stable and anything could change at any point.**


Features
--------

* No external dependencies
* Mailing lists
* Subscribers registered on multiple mailing lists
* HTML based emails
* Newsletter templates
* Newsletters that can be viewed on the browser (aka web views)
* Tracking of email and web "impressions" of sent newsletters
* Many settings and hooks for tweaking the behavior of the app, with reasonable defaults, so that you don't get lost in configuration.


TODO
----

* Documentation
* Tests
* Admin integration
* Plain text emails
* Template backends
* Hash generator backends
* Tracker backends
* Restructure things so that Newsletter becomes a ``Proxy`` model to a more generic Message model. Basically, make this a mailling app and not strictly a newsletter one.
* Add the ability to add content from other models in the newletter/message.
* Multilingual newsletters
* Newsletters with different authors/sender names and emails
* Make all views class based so that their extension becomes easier.
* Make models as extensible as possible, taking into account the possibility of model subclasses.

*Constant efforts*
* Simplicity, ideally this should be almost a plug-and-play app
* Configuration/extensibility without sacrificing simplicity (if possible)
* Documentation


License
-------

Free software: BSD license
