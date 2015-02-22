import textwrap
import unittest

from swanson.codegen import CodeGen
from swanson.data import Feature

class BaseTestCase(unittest.TestCase):
    maxDiff = None

    def assertGenerated(self, generator, expected_string):
        def strip_blank_lines(string):
            return '\n'.join(
                '' if line.strip() == '' else line
                for line in string.split('\n')
            )

        string = strip_blank_lines(generator)
        expected_string = strip_blank_lines(textwrap.dedent('\n'.join(expected_string.split('\n')[1:-1])))

        self.assertEqual(string, expected_string)


class FunctionParamsTestCase(BaseTestCase):
    def test_generate(self):
        self.assertEqual(
            CodeGen.generate_function_params(['a', 'b']),
            'a, b'
        )

    def test_duplicate_params(self):
        with self.assertRaises(CodeGen.InvalidParameters):
            CodeGen.generate_function_params(['a', 'a'])

class FunctionTestCase(BaseTestCase):
    def test_generate(self):
        self.assertGenerated(
            CodeGen.generate_function('add', ['a', 'b'], 'return a + b'),
            r'''
            def add(a, b):
                return a + b
            '''
        )

class StepHandlerTestCase(BaseTestCase):
    def test_generate(self):
        feature = Feature.from_string(u'''
            Feature:
                Scenario:
                    Given I enter "test@example.com" in the email field
        ''')
        step = feature.scenarios[0].steps[0]

        self.assertGenerated(
            CodeGen.generate_step_handler(step, 'given_example'),
            r'''
            @given(r'(?i)^I enter "test@example.com" in the email field$')
            def given_example(self, step):
                """
                Given I enter "test@example.com" in the email field
                """

                assert False
            '''
        )

class StepHandlersTestCase(BaseTestCase):
    def test_generate(self):
        feature = Feature.from_string(u"""
            Feature: Feature title
                Scenario: Scenario title
                    Given scenario given
                    When scenario when
                    Then scenario then
        """)
        steps = feature.scenarios[0].steps

        self.assertGenerated(
            CodeGen.generate_step_handlers(steps),
            r'''
            @given(r'(?i)^scenario given$')
            def given_scenario_given(self, step):
                """
                Given scenario given
                """

                assert False

            @when(r'(?i)^scenario when$')
            def when_scenario_when(self, step):
                """
                When scenario when
                """

                assert False

            @then(r'(?i)^scenario then$')
            def then_scenario_then(self, step):
                """
                Then scenario then
                """

                assert False
            '''
        )

    def test_same_step_title(self):
        feature = Feature.from_string(u"""
            Feature: Feature title
                Scenario: Scenario title
                    Given scenario given
                    And scenario given
        """)
        steps = feature.scenarios[0].steps

        self.assertGenerated(
            CodeGen.generate_step_handlers(steps),
            r'''
            @given(r'(?i)^scenario given$')
            def given_scenario_given(self, step):
                """
                Given scenario given
                """

                assert False
            '''
        )

    def test_function_name_collision(self):
        feature = Feature.from_string(u"""
            Feature: Feature title
                Scenario: Scenario title
                    Given step title
                    And step !! title
                    When step title
        """)
        steps = feature.scenarios[0].steps

        self.assertGenerated(
            CodeGen.generate_step_handlers(steps),
            r'''
            @given(r'(?i)^step title$')
            def given_step_title(self, step):
                """
                Given step title
                """

                assert False

            @given(r'(?i)^step !! title$')
            def given_step_title_2(self, step):
                """
                Given step !! title
                """

                assert False

            @when(r'(?i)^step title$')
            def when_step_title(self, step):
                """
                When step title
                """

                assert False
            '''
        )

class TestModuleTestCase(BaseTestCase):
    def test_generate(self):
        feature = Feature.from_string(u"""
            Feature: Feature title
                Background:
                    Given background given
                    When background when
                    Then background then

                Scenario: Scenario title
                    Given scenario title
                    When scenario title
                    Then scenario title

                Scenario Outline: Scenario Outline title
                    Given scenario outline <key> is <value>
                    When scenario outline <key> is <value>
                    Then scenario outline <key> is <value>

                    Examples:
                        | key     | value      |
                        | title   | "a title"  |
                        | success | guaranteed |
        """)

        self.assertGenerated(
            CodeGen.generate_test_module(feature),
            r'''
            from swanson import TestCase, step, given, when, then

            class BDDFeatureTitleTestCase(TestCase):
                """
                Feature title
                """

                def test_scenario_title(self):
                    """
                    Scenario title
                    """

                    self.run_scenario({Scenario title|u})

                def test_scenario_outline_title(self):
                    """
                    Scenario Outline title
                    """

                    self.run_scenario({Scenario Outline title|u})

                @given(r'(?i)^background given$')
                def given_background_given(self, step):
                    """
                    Given background given
                    """

                    assert False

                @given(r'(?i)^scenario title$')
                def given_scenario_title(self, step):
                    """
                    Given scenario title
                    """

                    assert False

                @given(r'(?i)^scenario outline title is "a title"$')
                def given_scenario_outline_title_is_a_title(self, step):
                    """
                    Given scenario outline title is "a title"
                    """

                    assert False

                @given(r'(?i)^scenario outline success is guaranteed$')
                def given_scenario_outline_success_is_guaranteed(self, step):
                    """
                    Given scenario outline success is guaranteed
                    """

                    assert False

                @when(r'(?i)^background when$')
                def when_background_when(self, step):
                    """
                    When background when
                    """

                    assert False

                @when(r'(?i)^scenario title$')
                def when_scenario_title(self, step):
                    """
                    When scenario title
                    """

                    assert False

                @when(r'(?i)^scenario outline title is "a title"$')
                def when_scenario_outline_title_is_a_title(self, step):
                    """
                    When scenario outline title is "a title"
                    """

                    assert False

                @when(r'(?i)^scenario outline success is guaranteed$')
                def when_scenario_outline_success_is_guaranteed(self, step):
                    """
                    When scenario outline success is guaranteed
                    """

                    assert False

                @then(r'(?i)^background then$')
                def then_background_then(self, step):
                    """
                    Then background then
                    """

                    assert False

                @then(r'(?i)^scenario title$')
                def then_scenario_title(self, step):
                    """
                    Then scenario title
                    """

                    assert False

                @then(r'(?i)^scenario outline title is "a title"$')
                def then_scenario_outline_title_is_a_title(self, step):
                    """
                    Then scenario outline title is "a title"
                    """

                    assert False

                @then(r'(?i)^scenario outline success is guaranteed$')
                def then_scenario_outline_success_is_guaranteed(self, step):
                    """
                    Then scenario outline success is guaranteed
                    """

                    assert False

            '''.format(**{
                'Scenario title|u': repr(u'Scenario title'),
                'Scenario Outline title|u': repr(u'Scenario Outline title')
            })
        )
