
import math
import re
import logging
from simpleeval import simple_eval, NameNotDefined, OperatorNotDefined, FunctionNotDefined

logger = logging.getLogger(__name__)

class Calculator:
    def __init__(self):
        # Define the safe environment for simpleeval
        self.functions = {
            'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
            'asin': math.asin, 'acos': math.acos, 'atan': math.atan,
            'sqrt': math.sqrt, 'log': math.log, 'log10': math.log10,
            'exp': math.exp, 'abs': abs, 'round': round,
            'min': min, 'max': max, 'factorial': math.factorial,
            'degrees': math.degrees, 'radians': math.radians,
            'ceil': math.ceil, 'floor': math.floor
        }
        self.names = {
            'pi': math.pi,
            'e': math.e,
            'tau': math.tau
        }

    def _preprocess(self, query):
        """
        Preprocesses the query to handle custom syntax like 5! -> factorial(5).
        """
        # Replace 5!, x!, (a+b)! with factorial(...)
        # We look for:
        # 1. digits/floats: \d+(?:\.\d+)?
        # 2. identifiers: [a-zA-Z_][a-zA-Z0-9_]*
        # 3. parenthesized groups: \([^)]+\)
        # Followed by ! but NOT followed by = (to avoid !=)
        
        # Note: This is a basic regex and might not handle nested parenthesis perfectly for (expr)!
        # but covers common cases.
        pattern = r'(\d+(?:\.\d+)?|[a-zA-Z_][a-zA-Z0-9_]*|\([^)]+\))!(?!=)'
        return re.sub(pattern, r'factorial(\1)', query)

    def evaluate(self, query):
        """
        Safely evaluates a math expression.
        Returns the result as a number (int or float) or raises an exception.
        """
        if not query:
            return None

        # Preprocess the query
        query = self._preprocess(query)
        
        # Allow using ^ for power
        query = query.replace('^', '**')

        try:
            result = simple_eval(
                query,
                functions=self.functions,
                names=self.names
            )
            return result
        except (NameNotDefined, OperatorNotDefined, FunctionNotDefined, SyntaxError, TypeError, ZeroDivisionError, ValueError) as e:
            # Re-raise known safe exceptions to be handled by the caller
            raise e
        except Exception as e:
            # Log unexpected errors
            logger.error(f"Unexpected error evaluating query '{query}': {e}", exc_info=True)
            raise e

    def format_result(self, result):
        """
        Formats the result for display.
        Removes trailing .0 for integers.
        """
        if isinstance(result, (int, float)) and not isinstance(result, bool): # bool is subclass of int in python
             # Check if it's effectively an integer
             if float(result).is_integer():
                return str(int(result))
             return f"{result:g}"
        return str(result)
