import unittest

from double_metaphone import Threshold, DoubleMetaphoneMatcher


class TestThreshold(unittest.TestCase):

    def test_from_string_with_implemented_enum(self):
        self.assertIs(Threshold.from_string('weak'), Threshold.WEAK)

    def test_from_string_with_unimplemented_enum(self):
        with self.assertRaises(NotImplementedError) as _:
            Threshold.from_string('HIGH')

    def test_from_string_with_non_string(self):
        with self.assertRaises(NotImplementedError) as _:
            Threshold.from_string(1)

    def test_from_int_with_implemented_enum(self):
        self.assertIs(Threshold.from_int(2), Threshold.STRONG)

    def test_from_int_with_unimplemented_enum(self):
        with self.assertRaises(NotImplementedError) as _:
            Threshold.from_int(7)

    def test_from_int_with_non_int(self):
        with self.assertRaises(NotImplementedError) as _:
            Threshold.from_int(7)


class TestDoubleMetaphoneMatcher(unittest.TestCase):

    def setUp(self):
        self.matcher = DoubleMetaphoneMatcher()

    def test_is_double_metaphone_match_with_different_names_producing_true_result(self):
        name1 = 'John'
        name2 = 'Jane'

        output = self.matcher.is_double_metaphone_match(name1, name2)

        self.assertTrue(output)

    def test_is_double_metaphone_match_with_different_names_producing_false_result(self):
        name1 = 'Johannes'
        name2 = 'John'

        output = self.matcher.is_double_metaphone_match(name1, name2)

        self.assertFalse(output)

    def test_is_double_metaphone_match_with_same_name(self):
        name1 = 'Jane'
        name2 = 'jane'

        output = self.matcher.is_double_metaphone_match(name1, name2)

        self.assertTrue(output)

    def test_is_double_metaphone_match_with_none_parameter(self):
        with self.assertRaises(ValueError) as _:
            self.matcher.is_double_metaphone_match(None, 'Foo')

    def test_ensure_threshold_is_enum_with_threshold_as_enum(self):
        threshold = Threshold.NORMAL

        output = self.matcher._ensure_threshold_is_enum(threshold)

        self.assertIs(output, threshold)

    def test_ensure_threshold_is_enum_with_threshold_as_string(self):
        expected = Threshold.NORMAL

        threshold = 'normal'
        output = self.matcher._ensure_threshold_is_enum(threshold)

        self.assertIs(output, expected)

    def test_ensure_threshold_is_enum_with_threshold_as_int(self):
        expected = Threshold.NORMAL

        threshold = 1
        output = self.matcher._ensure_threshold_is_enum(threshold)

        self.assertIs(output, expected)

    def test_ensure_threshold_is_enum_with_threshold_as_unimplemented_enum(self):
        with self.assertRaises(ValueError) as _:
            self.matcher._ensure_threshold_is_enum('foo')

    def test_double_metaphone_with_ascii_normalized_name(self):
        expected = ('JN', 'AN')

        name = 'John'
        output = self.matcher._double_metaphone(name)

        self.assertEqual(output, expected)

    def test_double_metaphone_with_accentuated_name(self):
        expected = ('JJN', 'AAN')

        name = 'Jæne'
        output = self.matcher._double_metaphone(name)

        self.assertEqual(output, expected)

    def test_compare_metaphones_with_different_metaphones_for_weak_threshold(self):
        metaphone1 = ('JRE', 'JTE')
        metaphone2 = ('ALS', 'AL0')
        threshold = Threshold.STRONG

        output = self.matcher._compare_metaphones(metaphone1, metaphone2, threshold)

        self.assertFalse(output)

    def test_compare_metaphones_with_different_metaphones_for_normal_threshold(self):
        metaphone1 = ('JRE', 'JTE')
        metaphone2 = ('ALS', 'AL0')
        threshold = Threshold.NORMAL

        output = self.matcher._compare_metaphones(metaphone1, metaphone2, threshold)

        self.assertFalse(output)

    def test_compare_metaphones_with_different_metaphones_for_strong_threshold(self):
        metaphone1 = ('JRE', 'JTE')
        metaphone2 = ('AFS', 'JRE')
        threshold = Threshold.STRONG

        output = self.matcher._compare_metaphones(metaphone1, metaphone2, threshold)

        self.assertFalse(output)

    def test_compare_metaphones_with_equal_metaphones_for_weak_threshold(self):
        metaphone1 = ('JRE', 'FOO')
        metaphone2 = ('ABC', 'FOO')
        threshold = Threshold.WEAK

        output = self.matcher._compare_metaphones(metaphone1, metaphone2, threshold)

        self.assertTrue(output)

    def test_compare_metaphones_with_equal_metaphones_for_normal_threshold(self):
        metaphone1 = ('JRE', 'FOO')
        metaphone2 = ('BAR', 'JRE')
        threshold = Threshold.NORMAL

        output = self.matcher._compare_metaphones(metaphone1, metaphone2, threshold)

        self.assertTrue(output)

    def test_compare_metaphones_with_equal_metaphones_for_strong_threshold(self):
        metaphone1 = ('JRE', 'FOO')
        metaphone2 = ('JRE', '')
        threshold = Threshold.STRONG

        output = self.matcher._compare_metaphones(metaphone1, metaphone2, threshold)

        self.assertTrue(output)


if __name__ == "__main__":
    unittest.main()
