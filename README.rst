Swanson
=======

|CILink|_

**Behaviour-driven development** is an agile technique, encouraging collaboration
with customers, testers, and developers.

It helps you think about what you're creating, before development starts -
when change is least expensive.

**Swanson** is a BDD test runner, **designed for Django**. It takes
specs in plain-text format, and runs them with the rest of your test suite.

*Example:*

.. code-block:: gherkin

   Given I am on the signup page
   And I have entered mostly valid data
   But the username field consists only of spaces
   When I try to register an account
   Then the username field displays a "this field is required" error message

Links
-----

* Documentation: http://swanson.readthedocs.org/
* Source: https://github.com/nathforge/django-swanson
* PyPI: https://pypi.python.org/pypi/django-swanson


.. |CILink| image:: https://travis-ci.org/nathforge/django-swanson.svg?branch=master
.. _CILink: https://travis-ci.org/nathforge/django-swanson
