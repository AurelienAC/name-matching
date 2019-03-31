import unittest

from component_matcher import NameLookupDirectory


class Test_NameLookupDirectory(unittest.TestCase):

    def setUp(self):
        self.lookup = NameLookupDirectory._NameLookupDirectory()

        self.names = ['Led Zeppelin', 'John Doe', 'Jane Doe', 'Janis Doe']
        self.name_ids = [0, 1, 2, 3]

        self.name_metaphones = [('LTSPLN', ''), ('TJN', ''),
                                ('TJN', ''), ('TJNS', '')]

    def test_generate_name_combinations_with_three_components(self):
        expected = [('Jane', 'J', 'Doe',), ('Jane', 'J',), ('Jane', 'Doe',),
                    ('J', 'Doe',), ('Jane',), ('J',), ('Doe',)]

        name = 'Jane J Doe'
        output = self.lookup._generate_name_combinations(name)

        self.assertEqual(output, expected)

    def test_generate_name_combinations_with_one_component(self):
        expected = [('John',)]

        name = 'John'
        output = self.lookup._generate_name_combinations(name)

        self.assertEqual(output, expected)

    def test_add_name_id_using_metaphone_for_strong_component(self):
        metaphone = ('METAPHONESTRONG', 'METAPHONEWEAK')
        name_id = 777
        key = 0

        self.lookup._add_name_id_using_metaphone(metaphone, name_id, key)
        strong_matches = self.lookup.strong_matches()

        integrity_test = metaphone[0] in strong_matches and name_id in strong_matches[metaphone[0]]

        self.assertTrue(integrity_test)

    def test_add_name_id_using_metaphone_for_weak_component(self):
        metaphone = ('METAPHONESTRONG', 'METAPHONEWEAK')
        name_id = 777
        key = 1

        self.lookup._add_name_id_using_metaphone(metaphone, name_id, key)
        weak_matches = self.lookup.weak_matches()

        integrity_test = metaphone[1] in weak_matches and name_id in weak_matches[metaphone[1]]

        self.assertTrue(integrity_test)

    def test_add_combinations_to_directory_and_check_if_all_metaphones_are_present(self):
        self.lookup.add_names(self.names, self.name_ids)

        strong_matches = self.lookup.strong_matches()
        weak_matches = self.lookup.weak_matches()

        for metaphones in self.name_metaphones:
            self.assertTrue(metaphones[0] in strong_matches)
            self.assertTrue(metaphones[1] in weak_matches)


if __name__ == "__main__":
    unittest.main()
