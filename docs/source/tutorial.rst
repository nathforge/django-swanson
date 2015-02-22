Tutorial
========

Prerequisites
-------------

:ref:`Install Swanson! <installation>`


Create a feature file
---------------------

Find a place to store tests. `Django docs`_ suggest a ``tests`` directory
for each app.

Feature files are written in the `Gherkin format`_. Paste the following into
``tests/example.feature``:

.. code-block:: gherkin
    
   Feature: BDD example
       Scenario: Eating apples
           Given I have 8 apples
           When I eat 2 apples
           Then I have 6 apples left

Run Django's test command:

.. code-block:: shell

   $ ./manage.py test
   ...
   UnimplementedScenariosError:
    * djangoproject/app/tests/example.feature
      * Eating apples
   ...

Ah. We haven't implemented our steps yet.

Let's start off with a barebones test case. We *could* do that manually, but
it's easier to...


Run the code generator
----------------------

.. code-block:: shell

   $ ./manage.py bddgen
   Generated code:
    * djangoproject/app/tests/test_example.py

This creates ``tests/test_example.py``:

.. code-block:: python

   from swanson import TestCase, step, given, when, then
   
   class BDDExampleTestCase(TestCase):
       def test_eating_apples(self):
           self.run_scenario(u'Eating apples')
       
       @given(r'(?i)^I have 8 apples$')
       def given_i_have_8_apples(self, step):
           assert False
       
       @when(r'(?i)^I eat 2 apples$')
       def when_i_eat_2_apples(self, step):
           assert False
       
       @then(r'(?i)^I have 6 apples left$')
       def then_i_have_6_apples_left(self, step):
           assert False

Note the ``assert False`` lines - these cause the test to fail. Let's replace
them with something more useful:

.. code-block:: python

   @given(r'(?i)^I have 8 apples$')
   def given_i_have_8_apples(self, step):
       self.apples = 8
   
   @when(r'(?i)^I eat 2 apples$')
   def when_i_eat_2_apples(self, step):
       self.apples -= 2
   
   @then(r'(?i)^I have 6 apples left$')
   def then_i_have_6_apples_left(self, step):
       self.assertEqual(self.apples, 6)

(We use ``assertEqual`` in the last step - that's one of the built-in
`unittest assertions`_.)

Run the tests again:

.. code-block:: shell

   $ ./manage.py test
   ...
   Ran 2 tests in 0.005s
   
   OK
   ...

Nice!

Still, our test case isn't very smart. If we change the number of ``apples`` in
the feature file, we also need to change the implementation.

What if we had...


Step parameters
---------------

Budget cuts require we start with **7** apples. Update the feature file:

.. code-block:: gherkin

   Given I have 7 apples
   When I eat 2 apples
   Then I have 5 apples left

And re-run the tests...

.. code-block:: shell

   $ ./manage.py test
   ...
   StepError: Error running 'Given I have 7 apples' on line 3 of djangoproject/app/tests/example.feature:
   
   NoStepHandlers: No step handlers found for 'Given I have 7 apples'
   ...

Dang. We *could* update the Python code to match, but what would that teach us?
Let's try using step parameters.

Take a look at ``r'(?i)^I have 8 apples$'``. That's a `regular expression`_, a
mini-language for matching text against patterns.

Change it to accept a variable number of apples:

.. code-block:: python

   @given(r'(?i)^I have (.+) apples$')
   def given_i_have_x_apples(self, step):

Note we've also updated the function definition - it takes captured text from
the regular expression. ``apples`` is passed as a string, so convert it
to an integer:

.. code-block:: python

   @given(r'(?i)^I have (.+) apples$')
   def given_i_have_x_apples(self, step):
       apples = int(apples)

To share ``apples`` with later steps, store it on ``self``:

.. code-block:: python

   @given(r'(?i)^I have (.+) apples$')
   def given_i_have_x_apples(self, step):
       self.apples = int(apples)

Our ``given`` step doesn't do a lot, but that's ok:

* ``Given`` steps set up the test.
* ``When`` steps perform an action.
* ``Then`` steps check that everything is as expected.

Now, update the other steps:

.. code-block:: python

   @when(r'(?i)^I eat (.+) apples$')
   def when_i_eat_x_apples(self, step, eat_apples):
       self.apples -= int(eat_apples)

   @then(r'(?i)^I have (.+) apples left$')
   def then_i_have_x_apples_left(self, step, expected_apples):
       self.assertEqual(self.apples, int(expected_apples))

And run the tests:

.. code-block:: shell

   $ ./manage.py test
   ...
   Ran 2 tests in 0.005s
   
   OK
   ...

Boom. BDD test implemented.


.. _`Django docs`: https://docs.djangoproject.com/en/dev/topics/testing/overview/
.. _`Gherkin format`: https://github.com/cucumber/cucumber/wiki/Gherkin
.. _`unittest assertions`: https://docs.python.org/2/library/unittest.html#unittest.TestCase.assertEqual
.. _`regular expression`: https://developers.google.com/edu/python/regular-expressions
