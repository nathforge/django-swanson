import unittest

import six

from swanson.data import Step
from swanson.decorators import step, given, when, then
from swanson.exceptions import MultipleStepHandlers, NoStepHandlers
from swanson.handlers import StepHandlers

class StepHandlersTestCase(unittest.TestCase):
    def test_handler_match_without_clause(self):
        @step(r'^I have (\d+) apples$')
        def my_handler():
            pass

        step_handlers = StepHandlers([
            my_handler
        ])
        
        match = step_handlers.get_handler_match_for_step(self.create_step('given', 'I have 10 apples'))
        self.assertEqual(match.match.groups(), ('10',))

    def test_handler_match_with_clause(self):
        @given(r'^I have (\d+) apples$')
        def my_handler():
            pass

        step_handlers = StepHandlers([
            my_handler
        ])

        match = step_handlers.get_handler_match_for_step(self.create_step('given', 'I have 10 apples'))
        self.assertEqual(match.match.groups(), ('10',))

        with six.assertRaisesRegex(self, NoStepHandlers, r"^No step handlers found .*$"):
            match = step_handlers.get_handler_match_for_step(self.create_step('when', 'I have 10 apples'))

    def test_multiple_handler_matches(self):
        @given(r'^I have (\d+) apples$')
        def my_handler1():
            pass

        @given(r'^I have (\d+) apples$')
        def my_handler2():
            pass

        step_handlers = StepHandlers([
            my_handler1,
            my_handler2
        ])

        with six.assertRaisesRegex(self, MultipleStepHandlers, r"(?m)^Multiple step handlers found .*$"):
            match = step_handlers.get_handler_match_for_step(self.create_step('given', 'I have 10 apples'))

    def test_handler_aliases(self):
        @given(r'^I have (\d+) apples$')
        @given(r'^I have (\d+) bananas$')
        def my_handler():
            pass

        step_handlers = StepHandlers([
            my_handler
        ])

        match = step_handlers.get_handler_match_for_step(self.create_step('given', 'I have 10 apples'))
        self.assertEqual(match.match.groups(), ('10',))

        match = step_handlers.get_handler_match_for_step(self.create_step('given', 'I have 10 bananas'))
        self.assertEqual(match.match.groups(), ('10',))

    def create_step(self, clause, title):
        return Step(None, {
            'title': {
                'index': 0,
                'clause': clause,
                'content': title
            },
            'text': {'content': None},
            'table': None
        })
