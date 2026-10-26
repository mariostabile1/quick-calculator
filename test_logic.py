
import unittest
import math
from calculator_logic import Calculator
from simpleeval import NameNotDefined, FunctionNotDefined, FeatureNotAvailable, InvalidExpression

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def test_basic_arithmetic(self):
        self.assertEqual(self.calc.evaluate("2 + 2"), 4)
        self.assertEqual(self.calc.evaluate("10 / 2"), 5.0)
        self.assertEqual(self.calc.evaluate("3 * 7"), 21)
        self.assertEqual(self.calc.evaluate("2^3"), 8)
        self.assertEqual(self.calc.evaluate("10 % 3"), 1)

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
        self.assertEqual(self.calc.evaluate("log2(8)"), 3.0)
        self.assertEqual(self.calc.evaluate("floor(log10(100))"), 2)
        # Test custom logN syntax
        self.assertEqual(self.calc.evaluate("log3(27)"), 3.0)
        self.assertEqual(self.calc.evaluate("log10(100)"), 2.0) # Should still work as native function or regex
        self.assertEqual(self.calc.evaluate("log(8, 2)"), 3.0) # Standard syntax
        
        # Test that != is not broken
        self.assertEqual(self.calc.evaluate("1 != 2"), True)
        self.assertEqual(self.calc.evaluate("1 != 1"), False)
        
    def test_error_handling(self):
        with self.assertRaises(ZeroDivisionError):
            self.calc.evaluate("1/0")
        
        with self.assertRaises((SyntaxError, NameNotDefined, FunctionNotDefined)):
             self.calc.evaluate("invalid syntax")

        with self.assertRaises(OverflowError):
            self.calc.evaluate("exp(1000)")

    def test_security(self):
        # Try to access dangerous things
        with self.assertRaises((NameNotDefined, FunctionNotDefined, ValueError)):
            self.calc.evaluate("__import__('os').system('ls')")
        
        with self.assertRaises((NameNotDefined, FunctionNotDefined, SyntaxError, ValueError)):
             self.calc.evaluate("open('test_logic.py')")

        # Test class injection
        # simpleeval raises FeatureNotAvailable for __attributes
        with self.assertRaises((NameNotDefined, FunctionNotDefined, SyntaxError, AttributeError, FeatureNotAvailable, ValueError)):
            self.calc.evaluate("().__class__.__bases__[0].__subclasses__()")
            
        with self.assertRaises((NameNotDefined, FunctionNotDefined, SyntaxError, FeatureNotAvailable)):
            self.calc.evaluate("10 .__class__")
            
        # Test attributes
        with self.assertRaises((NameNotDefined, FunctionNotDefined, SyntaxError, FeatureNotAvailable)):
            self.calc.evaluate("math.sin(1)") # user should not use 'math.' prefix if we didn't expose 'math' name
            
        # Test very large numbers (DoS prevention - limited by safe_power)
        self.assertTrue(self.calc.evaluate("2^100") > 0)

        # BUG-R2-C1-A2-H1: String method calls / attribute DoS
        with self.assertRaises((ValueError, FeatureNotAvailable)):
            self.calc.evaluate('"x".ljust(4000000000)')

        # BUG-R2-C1-A3-H1: String %-formatting DoS
        with self.assertRaises((ValueError, FeatureNotAvailable)):
            self.calc.evaluate('"%999999999d" % 1')

        # BUG-R2-C1-A3-H2: f-string format-spec DoS
        with self.assertRaises((ValueError, FeatureNotAvailable)):
            self.calc.evaluate('f"{1:>999999999}"')

        # BUG-R2-C1-A3-H3: math.factorial argument DoS
        with self.assertRaises(ValueError):
            self.calc.evaluate("99999999!")

        with self.assertRaises(ValueError):
            self.calc.evaluate("factorial(10**8)")

        with self.assertRaises(ValueError):
            self.calc.evaluate("factorial(factorial(13))")

        # BUG-R2-C1-A3-H5: Chained max-legal power nodes DoS
        with self.assertRaises(ValueError):
            self.calc.evaluate("4000000**4000000")

        with self.assertRaises(ValueError):
            self.calc.evaluate("4000000^4000000 + 4000000^4000000")

        # Hardening: round() with large negative ndigits DoS
        self.assertEqual(self.calc.evaluate("round(3.14159, 2)"), 3.14)
        self.assertEqual(self.calc.evaluate("round(1234, -2)"), 1200)
        with self.assertRaises(ValueError):
            self.calc.evaluate("round(1, -10**9)")

        # Hardening: chained multiplication exceeding bit limit
        with self.assertRaises(ValueError):
            self.calc.evaluate("(2^8000) * (2^8000)")

    def test_formatting(self):
        self.assertEqual(self.calc.format_result(5.0), "5")
        self.assertEqual(self.calc.format_result(5.5), "5.5")
        # basic check for float formatting, :g usually handles small errors or large numbers nicely
        self.assertTrue(len(self.calc.format_result(1/3)) < 15)
        # Large integers formatting (does not raise OverflowError)
        formatted_171 = self.calc.format_result(self.calc.evaluate("171!"))
        self.assertTrue(len(formatted_171) > 300)
        formatted_power = self.calc.format_result(self.calc.evaluate("2^1000"))
        self.assertTrue(len(formatted_power) > 300) 

if __name__ == '__main__':
    unittest.main()
