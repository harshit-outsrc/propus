import unittest
import unittest.mock
import json

from propus.helpers.etl import (
    TRUE_VALUES,
    FALSE_VALUES,
    NULL_VALUES,
    clean_phone,
    clean_ssn,
    get_bool,
    get_bool_or_none,
    get_int,
    get_int_or_none,
    get_string,
    get_string_or_none,
    decode_json,
    batch_generator,
    fetch_county,
)
from propus.helpers.exceptions import JSONDecodeError


class NoStringRepresentation:
    def __str__(self):
        return


class TestETL(unittest.TestCase):
    def setUp(self):
        self.test_cases_batch_generator = [
            # Batch size smaller than list length
            ([1, 2, 3, 4, 5, 6, 7, 8], 3, [[1, 2, 3], [4, 5, 6], [7, 8]]),
            # Batch size equal to list length
            ([1, 2, 3, 4, 5], 5, [[1, 2, 3, 4, 5]]),
            # Empty input list
            ([], 3, []),
        ]

    def test_clean_phone(self):
        with self.assertRaises(ValueError):
            clean_phone(dict(foo="bar"))
        with self.assertRaises(ValueError):
            clean_phone("foo-bar")
        with self.assertRaises(ValueError):
            clean_phone("(987)654-32101")
        with self.assertRaises(ValueError):
            clean_phone("(987)654-321")
        self.assertEqual(clean_phone("987-654-3210"), "9876543210")
        self.assertEqual(clean_phone("987.654.3210"), "9876543210")
        self.assertEqual(clean_phone("(987) 654-3210"), "9876543210")
        self.assertEqual(clean_phone("(987)654-3210"), "9876543210")
        self.assertEqual(clean_phone("+1-987-654-3210"), "9876543210")

    def test_clean_ssn(self):
        with self.assertRaises(ValueError):
            clean_ssn(dict(foo="bar"))
        with self.assertRaises(ValueError):
            clean_ssn(98765432)
        with self.assertRaises(ValueError):
            clean_ssn("98765432")
        with self.assertRaises(ValueError):
            clean_ssn(9876543210)
        with self.assertRaises(ValueError):
            clean_ssn("9876543210")
        with self.assertRaises(ValueError):
            clean_ssn("Not a SSN")
        self.assertEqual(clean_ssn("987-65-4321"), "987654321")
        self.assertEqual(clean_ssn("987.65.4321"), "987654321")
        self.assertEqual(clean_ssn(987654321), "987654321")
        self.assertEqual(clean_ssn(4321), "XXXXX4321")
        self.assertEqual(clean_ssn("XXX-XX-4321"), "XXXXX4321")
        self.assertIsNone(clean_ssn("000-00-0000"))

    def test_get_bool(self):
        for t in TRUE_VALUES:
            self.assertTrue(get_bool(t))

        for f in FALSE_VALUES:
            self.assertFalse(get_bool(f))

        for x in NULL_VALUES:
            with self.assertRaises(ValueError):
                get_bool(x)

        for y in "ABCDE98765":
            with self.assertRaises(ValueError):
                get_bool(y)

    def test_get_bool_or_none(self):
        for t in TRUE_VALUES:
            self.assertTrue(get_bool_or_none(t))

        for f in FALSE_VALUES:
            self.assertFalse(get_bool_or_none(f))

        for x in NULL_VALUES:
            self.assertIsNone(get_bool_or_none(x))

        for y in "ABCDE98765":
            with self.assertRaises(ValueError):
                get_bool(y)

    def test_get_int(self):
        self.assertEqual(get_int("1"), 1)
        self.assertEqual(get_int(1), 1)
        self.assertEqual(get_int("-1"), -1)
        self.assertEqual(get_int(-1), -1)
        self.assertEqual(get_int("9876543210"), 9876543210)
        self.assertEqual(get_int(9876543210), 9876543210)
        self.assertEqual(get_int(3.14), 3)

        for x in NULL_VALUES:
            with self.assertRaises(ValueError):
                get_int(x)

        for y in "ABCDE":
            with self.assertRaises(ValueError):
                get_int(y)

        for z in ["3.14", "-3.14", "Not an int", dict(foo="bar")]:
            with self.assertRaises(ValueError):
                get_int(z)

    def test_get_int_or_none(self):
        self.assertEqual(get_int_or_none("1"), 1)
        self.assertEqual(get_int_or_none(1), 1)
        self.assertEqual(get_int_or_none("-1"), -1)
        self.assertEqual(get_int_or_none(-1), -1)
        self.assertEqual(get_int_or_none("9876543210"), 9876543210)
        self.assertEqual(get_int_or_none(9876543210), 9876543210)
        self.assertEqual(get_int_or_none(3.14), 3)

        for x in NULL_VALUES:
            self.assertIsNone(get_int_or_none(x))

        for y in "ABCDE":
            with self.assertRaises(ValueError):
                get_int_or_none(y)

        for z in ["3.14", "-3.14", "Not an int", dict(foo="bar")]:
            with self.assertRaises(ValueError):
                get_int_or_none(z)

    def test_get_string(self):
        for a in "ABCDE":
            self.assertEqual(get_string(a), a)

        for x in [9, 8, 7, 6, 5, dict(foo="bar"), ["foo", "bar"], int, dict, list]:
            self.assertNotEqual(get_string(x), x)

        not_a_string = NoStringRepresentation()
        with self.assertRaises(TypeError):
            get_string(not_a_string)

    def test_get_string_or_none(self):
        for a in "ABCDE":
            self.assertEqual(get_string_or_none(a), a)

        for x in [9, 8, 7, 6, 5, dict(foo="bar"), ["foo", "bar"], int, dict, list]:
            self.assertNotEqual(get_string_or_none(x), x)

        for y in NULL_VALUES:
            self.assertIsNone(get_string_or_none(y))

        not_a_string = NoStringRepresentation()
        with self.assertRaises(TypeError):
            get_string_or_none(not_a_string)

    def test_decode_json(self):
        error_caught = False
        try:
            # Below JSON is invalid, strings must be enclosed in double quotes (") rather than single quotes (').
            decode_json("{\"invalid\":'json'}")
        except JSONDecodeError as err:
            self.assertEqual(str(err), "Invalid JSON: {\"invalid\":'json'}")
            error_caught = True
        self.assertTrue(error_caught)

        test_data = {"a": "b", "c": 1234}
        self.assertEqual(decode_json(json.dumps(test_data)), test_data)

    def test_batch_generator(self):
        for input_list, batch_size, expected_output in self.test_cases_batch_generator:
            with self.subTest(input_list=input_list, batch_size=batch_size):
                result = list(batch_generator(input_list, batch_size))
                self.assertEqual(result, expected_output)

    def test_fetch_county(self):
        tests = [
            [{"city": "ELK GROVE"}, "Sacramento"],
            [{"city": "folsom"}, "Sacramento"],
            [{"zip_code": "95018"}, "Santa Cruz"],
            [{"city": "ElDorAdo Hi Lls"}, "El Dorado"],
        ]
        for test in tests:
            self.assertEqual(fetch_county(**test[0]), test[1])


if __name__ == "__main__":
    unittest.main()
