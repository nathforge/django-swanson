import unittest

from gherkin_parser import parse_lines

from swanson.data import Feature, Scenario, ScenarioOutline

class ModelTestCase(unittest.TestCase):
    def setUp(self):
        parsed = parse_lines(u"""
            @tag1 @tag2
            @tag3
            Feature: Feature title
                Feature description 1
                Feature description 2

                Background: Background title
                    Background description 1
                    Background description 2

                    Given background-given
                    When background-when
                    Then background-then

                @tagA @tagB
                @tagC
                Scenario: Scenario title
                    Scenario description 1
                    Scenario description 2

                    Given scenario-given
                        | key | value |
                        | abc | 123   |
                        | def | 456   |
                        | ghi |
                    When scenario-when
                        '''
                        Text 1
                        Text 2
                        '''
                    Then scenario-then

                @tagD @tagE
                @tagF
                Scenario Outline: Scenario outline title
                    Scenario outline description 1
                    Scenario outline description 2

                    Given <key> is <value>-given
                        '''
                        Text <key> is <value>
                        '''
                    When <key> is <value>-when
                    Then <key> is <value>-then

                    Examples: Examples title
                        | key  | value  |
                        | key1 | value1 |
                        | key2 | value2 |
        """.split('\n'))

        self.feature = Feature(parsed)

    def test_feature(self):
        feature = self.feature

        self.assertEqual(feature.tags, ['tag1', 'tag2', 'tag3'])
        self.assertEqual(feature.title, 'Feature title')
        self.assertEqual(feature.description, 'Feature description 1\nFeature description 2')

        self.assertEqual(len(feature.scenarios), 2)

    def test_background(self):
        background = self.feature.background

        self.assertEqual(background.title, 'Background title')
        self.assertEqual(background.description, 'Background description 1\nBackground description 2')

        self.assertEqual(len(background.steps), 3)
        
        self.assertEqual(background.steps[0].clause, 'given')
        self.assertEqual(background.steps[0].title, 'background-given')
        
        self.assertEqual(background.steps[1].clause, 'when')
        self.assertEqual(background.steps[1].title, 'background-when')

        self.assertEqual(background.steps[2].clause, 'then')
        self.assertEqual(background.steps[2].title, 'background-then')

    def test_scenario(self):
        scenario = self.feature.scenarios[0]
        self.assertEqual(type(scenario), Scenario)

        self.assertEqual(scenario.tags, ['tagA', 'tagB', 'tagC'])
        self.assertEqual(scenario.title, 'Scenario title')
        self.assertEqual(scenario.description, 'Scenario description 1\nScenario description 2')

        self.assertEqual(len(scenario.steps), 3)

        self.assertEqual(scenario.steps[0].clause, 'given')
        self.assertEqual(scenario.steps[0].title, 'scenario-given')
        self.assertEqual(list(scenario.steps[0].table), [
            ['key', 'value'],
            ['abc', '123'],
            ['def', '456'],
            ['ghi']
        ])

        self.assertEqual(scenario.steps[1].clause, 'when')
        self.assertEqual(scenario.steps[1].title, 'scenario-when')
        self.assertEqual(scenario.steps[1].text, 'Text 1\nText 2')

        self.assertEqual(scenario.steps[2].clause, 'then')
        self.assertEqual(scenario.steps[2].title, 'scenario-then')

    def test_scenario_outline(self):
        scenario = self.feature.scenarios[1]
        self.assertEqual(type(scenario), ScenarioOutline)

        expanded = scenario.expand_examples()
        self.assertEqual(len(expanded), 2)

        self.assertEqual(expanded[0].steps[0].clause, 'given')
        self.assertEqual(expanded[0].steps[0].title, 'key1 is value1-given')
        self.assertEqual(expanded[0].steps[0].text, 'Text key1 is value1')

        self.assertEqual(expanded[0].steps[1].clause, 'when')
        self.assertEqual(expanded[0].steps[1].title, 'key1 is value1-when')

        self.assertEqual(expanded[0].steps[2].clause, 'then')
        self.assertEqual(expanded[0].steps[2].title, 'key1 is value1-then')

        self.assertEqual(expanded[1].steps[0].clause, 'given')
        self.assertEqual(expanded[1].steps[0].title, 'key2 is value2-given')
        self.assertEqual(expanded[1].steps[0].text, 'Text key2 is value2')

        self.assertEqual(expanded[1].steps[1].clause, 'when')
        self.assertEqual(expanded[1].steps[1].title, 'key2 is value2-when')

        self.assertEqual(expanded[1].steps[2].clause, 'then')
        self.assertEqual(expanded[1].steps[2].title, 'key2 is value2-then')

    def test_table(self):
        table = self.feature.scenarios[0].steps[0].table

        self.assertEqual(len(table), 4)

        self.assertEqual(list(table), [
            ['key', 'value'],
            ['abc', '123'],
            ['def', '456'],
            ['ghi']
        ])

        self.assertEqual(list(table.dicts), [
            {'key': 'abc', 'value': '123'},
            {'key': 'def', 'value': '456'},
            {'key': 'ghi', 'value': None}
        ])
