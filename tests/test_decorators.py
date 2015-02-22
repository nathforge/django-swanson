import unittest

from swanson.decorators import step, given, when, then
from swanson.handlers import Matcher, StepHandler

class DecoratorTestCase(unittest.TestCase):
    def test_step(self):
        @step(r'^pattern$')
        def my_handler():
            pass

        self.assertIsInstance(my_handler, StepHandler)
        self.assertEqual(len(my_handler.matchers), 1)
        self.assertIsInstance(my_handler.matchers[0], Matcher)
        self.assertEqual(my_handler.matchers[0].regex.pattern, r'^pattern$')
        self.assertEqual(my_handler.matchers[0].clause, None)
        self.assertTrue(callable(my_handler.func))
        self.assertEqual(my_handler.func.__name__, 'my_handler')

    def test_given(self):
        @given(r'^pattern$')
        def my_handler():
            pass

        self.assertIsInstance(my_handler, StepHandler)
        self.assertEqual(len(my_handler.matchers), 1)
        self.assertIsInstance(my_handler.matchers[0], Matcher)
        self.assertEqual(my_handler.matchers[0].regex.pattern, r'^pattern$')
        self.assertEqual(my_handler.matchers[0].clause, 'given')
        self.assertTrue(callable(my_handler.func))
        self.assertEqual(my_handler.func.__name__, 'my_handler')

    def test_when(self):
        @when(r'^pattern$')
        def my_handler():
            pass

        self.assertIsInstance(my_handler, StepHandler)
        self.assertEqual(len(my_handler.matchers), 1)
        self.assertIsInstance(my_handler.matchers[0], Matcher)
        self.assertEqual(my_handler.matchers[0].regex.pattern, r'^pattern$')
        self.assertEqual(my_handler.matchers[0].clause, 'when')
        self.assertTrue(callable(my_handler.func))
        self.assertEqual(my_handler.func.__name__, 'my_handler')

    def test_then(self):
        @then(r'^pattern$')
        def my_handler():
            pass

        self.assertIsInstance(my_handler, StepHandler)
        self.assertEqual(len(my_handler.matchers), 1)
        self.assertIsInstance(my_handler.matchers[0], Matcher)
        self.assertEqual(my_handler.matchers[0].regex.pattern, r'^pattern$')
        self.assertEqual(my_handler.matchers[0].clause, 'then')
        self.assertTrue(callable(my_handler.func))
        self.assertEqual(my_handler.func.__name__, 'my_handler')

    def test_aliases(self):
        @given(r'^given-pattern$')
        @when(r'^when-pattern$')
        @then(r'^then-pattern$')
        def my_handler():
            pass

        self.assertIsInstance(my_handler, StepHandler)
        self.assertEqual(len(my_handler.matchers), 3)

        self.assertIsInstance(my_handler.matchers[0], Matcher)
        self.assertEqual(my_handler.matchers[0].regex.pattern, r'^given-pattern$')
        self.assertEqual(my_handler.matchers[0].clause, 'given')

        self.assertIsInstance(my_handler.matchers[1], Matcher)
        self.assertEqual(my_handler.matchers[1].regex.pattern, r'^when-pattern$')
        self.assertEqual(my_handler.matchers[1].clause, 'when')

        self.assertIsInstance(my_handler.matchers[2], Matcher)
        self.assertEqual(my_handler.matchers[2].regex.pattern, r'^then-pattern$')
        self.assertEqual(my_handler.matchers[2].clause, 'then')

        self.assertTrue(callable(my_handler.func))
        self.assertEqual(my_handler.func.__name__, 'my_handler')
