import unittest

from name_normalizer import NameNormalizer


class TestNameNormalizer(unittest.TestCase):

    def setUp(self):
        self.normalizer = NameNormalizer()

    def test_normalize_name_with_none_parameter(self):
        expected = ''

        output = self.normalizer.normalize_name(None)

        self.assertEqual(output, expected)

    def test_normalize_name_with_name_needing_normalization(self):
        expected = 'de maximilien trunst'

        name = 'DR. Maximilien De Trünst'
        output = self.normalizer.normalize_name(name)

        self.assertEqual(output, expected)

    def test_normalize_name_with_name_not_needing_normalization(self):
        name = 'doe jane'

        output = self.normalizer.normalize_name(name)

        self.assertEqual(output, name)

    def test_expand_name_abbreviations_with_abbreviated_name(self):
        expected_name = ['Maximilien', 'Herbert']

        name = ['Max', 'Herbert']
        expanded_named = list(self.normalizer._expand_name_abbreviations(name))

        self.assertEqual(expanded_named, expected_name)

    def test_expand_name_abbreviations_with_expanded_name(self):
        name = ['Maximilien', 'Herbert']

        result = list(self.normalizer._expand_name_abbreviations(name))

        self.assertEqual(result, name)

    def test_normalize_unicode_to_ascii_with_accentuated_characters(self):
        expected_name = 'Accentue Bjork'

        name = 'Accentué Björk'
        ascii_name = self.normalizer._normalize_unicode_to_ascii(name)

        self.assertEqual(ascii_name, expected_name)

    def test_normalize_unicode_to_ascii_with_unaccentuated_characters(self):
        name = 'Jane Doe'

        output = self.normalizer._normalize_unicode_to_ascii(name)

        self.assertEqual(output, name)

    def test_remove_titles_with_title_at_start(self):
        expected = ['Jane', 'Doe']

        name = ['Dr.', 'Jane', 'Doe']
        output = list(self.normalizer._remove_titles(name))

        self.assertEqual(output, expected)

    def test_remove_titles_with_title_at_end(self):
        expected = ['Jane', 'Doe']

        name = ['Jane', 'Doe', 'DR.']
        output = list(self.normalizer._remove_titles(name))

        self.assertEqual(output, expected)

    def test_remove_titles_with_no_titles(self):
        name = ['Jane', 'Doe']

        output = list(self.normalizer._remove_titles(name))

        self.assertEqual(output, name)

    def test_split_name_into_components_with_multiple_components(self):
        expected = ['Jane', 'Doe']

        name = 'Jane Doe'
        output = list(self.normalizer._split_name_into_components(name))

        self.assertEqual(output, expected)

    def test_split_name_into_components_with_singular_component(self):
        expected = ['Doe']

        name = 'Doe'
        output = list(self.normalizer._split_name_into_components(name))

        self.assertEqual(output, expected)

    def test_split_name_into_components_with_special_characters(self):
        expected = ['Jean', 'D', 'oe']

        name = 'Jean D\'oe'
        output = list(self.normalizer._split_name_into_components(name))

        self.assertEqual(output, expected)

    def test_to_lower_with_capitalized_letters(self):
        expected = 'john doe'

        name = 'John Doe'
        output = self.normalizer._to_lower(name)

        self.assertEqual(output, expected)

    def test_to_lower_with_all_lower_case_letters(self):
        name = 'jane doe'

        output = self.normalizer._to_lower(name)

        self.assertEqual(output, name)


if __name__ == "__main__":
    unittest.main()
