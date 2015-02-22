Overview
========

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


Requirements
------------

Swanson requires the following:

* Python 2.7 or 3.4
* Django 1.7


.. _installation:

Installation
------------

Install the latest release with ``pip``:

.. code-block:: shell

   pip install swanson

Or the development version from `Github`_:

.. code-block:: shell
   
   pip install git+https://github.com/nathforge/swanson

Add ``swanson`` to your ``INSTALLED_APPS``:

.. code-block:: python

   INSTALLED_APPS = (
       # ...
       'swanson',
   )

Set the ``TEST_RUNNER``:

.. code-block:: python

   TEST_RUNNER = 'swanson.test.runner.DiscoverRunner'


.. _`Github`: https://github.com/nathforge/swanson
