
import unittest
import math
from calculator_logic import Calculator
from simpleeval import NameNotDefined, FunctionNotDefined

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def test_basic_arithmetic(self):
        self.assertEqual(self.calc.evaluate("2 + 2"), 4)
        self.assertEqual(self.calc.evaluate("10 / 2"), 5.0)
        self.assertEqual(self.calc.evaluate("3 * 7"), 21)
        self.assertEqual(self.calc.evaluate("2^3"), 8)

    def test_math_functions(self):
        self.assertEqual(self.calc.evaluate("sqrt(16)"), 4.0)
        self.assertAlmostEqual(self.calc.evaluate("sin(pi/2)"), 1.0)
        self.assertAlmostEqual(self.calc.evaluate("cos(0)"), 1.0)
        self.assertAlmostEqual(self.calc.evaluate("min(1, 2, 3)"), 1)
        self.assertAlmostEqual(self.calc.evaluate("max(1, 2, 3)"), 3)
        self.assertAlmostEqual(self.calc.evaluate("abs(-5)"), 5)

    def test_new_math_functions(self):
        self.assertEqual(self.calc.evaluate("factorial(5)"), 120)
        self.assertEqual(self.calc.evaluate("5!"), 120)
        self.assertEqual(self.calc.evaluate("degrees(pi)"), 180.0)
        self.assertEqual(self.calc.evaluate("(2+3)!"), 120)
        
        # Test that != is not broken
        self.assertEqual(self.calc.evaluate("1 != 2"), True)
        self.assertEqual(self.calc.evaluate("1 != 1"), False)
        
    def test_error_handling(self):
        with self.assertRaises(ZeroDivisionError):
            self.calc.evaluate("1/0")
        
        with self.assertRaises((SyntaxError, NameNotDefined, FunctionNotDefined)):
             self.calc.evaluate("invalid syntax")

    def test_security(self):
        # Try to access dangerous things
        with self.assertRaises((NameNotDefined, FunctionNotDefined)):
            self.calc.evaluate("__import__('os').system('ls')")
        
        with self.assertRaises((NameNotDefined, FunctionNotDefined)):
             self.calc.evaluate("open('test_logic.py')")

    def test_formatting(self):
        self.assertEqual(self.calc.format_result(5.0), "5")
        self.assertEqual(self.calc.format_result(5.5), "5.5")
        # basic check for float formatting, :g usually handles small errors or large numbers nicely
        self.assertTrue(len(self.calc.format_result(1/3)) < 15) 

if __name__ == '__main__':
    unittest.main()
