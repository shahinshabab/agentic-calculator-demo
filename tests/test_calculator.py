import unittest

from calculator import CalculatorError, calculate


class CalculatorTests(unittest.TestCase):
    def test_operator_precedence(self):
        self.assertEqual(calculate("2 + 3 * 4"), 14)

    def test_parentheses(self):
        self.assertEqual(calculate("(24 + 6) / 3"), 10)

    def test_decimal_result(self):
        self.assertAlmostEqual(calculate("10 / 4"), 2.5)

    def test_negative_number(self):
        self.assertEqual(calculate("-8 + 3"), -5)

    def test_division_by_zero_is_rejected(self):
        with self.assertRaises(CalculatorError):
            calculate("2 / 0")

    def test_python_code_is_rejected(self):
        with self.assertRaises(CalculatorError):
            calculate("__import__('os').system('id')")

    def test_extreme_exponent_is_rejected(self):
        with self.assertRaises(CalculatorError):
            calculate("2 ** 100")


if __name__ == "__main__":
    unittest.main()

