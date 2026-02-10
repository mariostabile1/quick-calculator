
import unittest
import math
from calculator_logic import Calculator
from simpleeval import NameNotDefined, FunctionNotDefined, FeatureNotAvailable

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

    def test_security(self):
        # Try to access dangerous things
        with self.assertRaises((NameNotDefined, FunctionNotDefined)):
            self.calc.evaluate("__import__('os').system('ls')")
        
        with self.assertRaises((NameNotDefined, FunctionNotDefined, SyntaxError)):
             self.calc.evaluate("open('test_logic.py')")

        # Test class injection
        # simpleeval raises FeatureNotAvailable for __attributes
        with self.assertRaises((NameNotDefined, FunctionNotDefined, SyntaxError, AttributeError, FeatureNotAvailable)):
            self.calc.evaluate("().__class__.__bases__[0].__subclasses__()")
            
        with self.assertRaises((NameNotDefined, FunctionNotDefined, SyntaxError, FeatureNotAvailable)):
            self.calc.evaluate("10 .__class__")
            
        # Test attributes
        with self.assertRaises((NameNotDefined, FunctionNotDefined, SyntaxError)):
            self.calc.evaluate("math.sin(1)") # user should not use 'math.' prefix if we didn't expose 'math' name
            
        # Test very large numbers (DoS prevention - limited by simpleeval MAX_POWER usually, but Python handles large ints)
        # simpleeval defaults: MAX_POWER=100000. 2**10000 is fine.
        # We just check it doesn't crash.
        self.assertTrue(self.calc.evaluate("2^100") > 0)

    def test_formatting(self):
        self.assertEqual(self.calc.format_result(5.0), "5")
        self.assertEqual(self.calc.format_result(5.5), "5.5")
        # basic check for float formatting, :g usually handles small errors or large numbers nicely
        self.assertTrue(len(self.calc.format_result(1/3)) < 15) 

if __name__ == '__main__':
    unittest.main()
