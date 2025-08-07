from django.core.exceptions import ValidationError
from django.test import TestCase

from manager.forms import validate_serial_number


class FormsTest(TestCase):
    def test_internal_serial_number_validation_with_short_number(self):
        with self.assertRaises(ValidationError):
            validate_serial_number("12345")

    def test_internal_serial_number_validation_with_long_number(self):
        with self.assertRaises(ValidationError):
            validate_serial_number("ABC12345678")

    def test_internal_serial_number_validation_with_no_letters(self):
        with self.assertRaises(ValidationError):
            validate_serial_number("12312345")

    def test_internal_serial_number_validation_with_no_digits(self):
        with self.assertRaises(ValidationError):
            validate_serial_number("ZXCQWERTY")

    def test_internal_serial_number_validation_with_valid_data(self):
        self.assertTrue(validate_serial_number("ABC1234567"))
