Why shouldn't I use Swanson?
============================

This is a very early version.

Non-Django use is not supported, and might never be. You're better off with
:ref:`another tool <alternative_options>`.


Why *should* I use Swanson?
---------------------------

Swanson is designed for Django. This gives us:

* Improved speed through test reordering.
* Database setup and teardown, including fixtures. Data doesn't persist between tests.
* Ability to test against a "live" web server.
* Third-party app extensions - South, Jenkins, etc.

By using unit tests, it couldn't be easier to share code. Other tools
use Python modules, making code re-use more difficult.


.. _alternative_options:

Alternative options
-------------------

Behave / Lettuce
""""""""""""""""

The best known Python projects. Each has decent community support, including
IDE integration. They both implement their own test infrastructure.

`Behave`_ is a fantastic option. It's mature, with a well thought-out design.
Django integration isn't included, though `Django Behave`_ seems a popular
choice.

`Lettuce`_ comes with Django integration out of the box - it's very easy to get
started. Unfortunately it stores much of it's state in a global namespace, which
isn't cleared between tests. BDD tests start to silently conflict, making it
difficult to add new features.


.. _behave: http://pythonhosted.org/behave/
.. _django behave: https://github.com/django-behave/django-behave
.. _lettuce: http://lettuce.it/
