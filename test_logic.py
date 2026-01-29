import math
import unittest

def calculate(query):
    safe_dict = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
    safe_dict['abs'] = abs
    safe_dict['round'] = round
    safe_dict['min'] = min
    safe_dict['max'] = max
    
    try:
        query = query.replace('^', '**')
        return eval(query, {"__builtins__": None}, safe_dict)
    except Exception as e:
        return str(e)

class TestCalculator(unittest.TestCase):
    def test_basic_arithmetic(self):
        self.assertEqual(calculate("2 + 2"), 4)
        self.assertEqual(calculate("10 / 2"), 5.0)
        self.assertEqual(calculate("3 * 7"), 21)
        self.assertEqual(calculate("2^3"), 8)

    def test_math_functions(self):
        self.assertEqual(calculate("sqrt(16)"), 4.0)
        self.assertAlmostEqual(calculate("sin(pi/2)"), 1.0)
        self.assertAlmostEqual(calculate("cos(0)"), 1.0)

    def test_error_handling(self):
        result = calculate("1/0")
        self.assertTrue("division by zero" in result)
        
        result = calculate("invalid syntax")
        self.assertTrue("invalid syntax" in result or "name 'invalid' is not defined" in result)

    def test_security(self):
        # Try to access dangerous things
        result = calculate("__import__('os').system('ls')")
        self.assertNotEqual(result, 0) # Should fail
        self.assertTrue("name '__import__' is not defined" in str(result) or "object is not subscriptable" in str(result))

if __name__ == '__main__':
    unittest.main()
