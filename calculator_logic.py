
import math
import re
import logging
import ast
import operator as _op
from simpleeval import (
    SimpleEval,
    DEFAULT_OPERATORS,
    NameNotDefined,
    OperatorNotDefined,
    FunctionNotDefined,
    FeatureNotAvailable,
    InvalidExpression,
)

logger = logging.getLogger(__name__)


class MathOnlyEval(SimpleEval):
    """Evaluator with attribute (method) access and string operations disabled.

    The calculator's grammar is arithmetic plus the whitelisted math
    functions. simpleeval's MAX_STRING_LENGTH guard covers only string
    literals and the * and + operators, so method calls such as
    "x".ljust(N) would allocate attacker-chosen amounts of memory with
    no bound; the attribute path is closed off entirely.
    """

    def _eval_attribute(self, node):
        raise FeatureNotAvailable(
            "Attribute access is not available in this calculator."
        )

    def _eval_joinedstr(self, node):
        raise FeatureNotAvailable(
            "f-strings are not available in this calculator."
        )

    def _eval_formattedvalue(self, node):
        raise FeatureNotAvailable(
            "String formatting is not available in this calculator."
        )


# simpleeval's DEFAULT_OPERATORS maps ast.Mod to the raw operator.mod.
# For a string left operand that is CPython %-formatting, whose width
# field sets the OUTPUT size ('%999999999d' % 1 -> ~1 GB string) with no
# guard (unlike safe_mult / safe_add for * and +). Reject string/bytes
# left operands; numeric modulo is unaffected.
def _safe_mod(a, b):
    if isinstance(a, (str, bytes)):
        raise FeatureNotAvailable("String formatting with % is not allowed")
    return _op.mod(a, b)


# simpleeval's safe_power bounds only the OPERANDS of ** (both at 4,000,000),
# never the result or the compute cost: 4000000**4000000 passes the guard and
# burns ~32 s of CPU for a ~26-million-digit result that can never be
# displayed anyway. Chained with +, the per-node cost stacks linearly with
# query length. Bound the result size, which transitively bounds both memory
# and compute; ValueError is in the known-safe tuples.
_MAX_POWER_RESULT_BITS = 10000  # ~3,000 decimal digits; ample for a calculator


def _safe_power(a, b):
    if abs(a) > 4000000 or abs(b) > 4000000:
        raise ValueError("Power operands out of supported range")
    if abs(a) > 1 and abs(b) * math.log2(abs(a)) > _MAX_POWER_RESULT_BITS:
        raise ValueError("Power result too large")
    return a ** b


def _safe_mult(a, b):
    if isinstance(a, (str, bytes)) or isinstance(b, (str, bytes)):
        raise FeatureNotAvailable("String repetition with * is not allowed")
    if isinstance(a, int) and isinstance(b, int):
        if a != 0 and b != 0 and (a.bit_length() + b.bit_length()) > _MAX_POWER_RESULT_BITS:
            raise ValueError("Multiplication result too large")
    return _op.mul(a, b)


# math.factorial is a C call with no size guard: factorial(99999999) runs
# as a single uninterruptible C call that blocks the single-threaded event
# loop and ramps memory. Bound the argument to 1500 (~4,115 decimal digits,
# safely within Python's 4,300-digit int-to-str conversion limit).
_MAX_FACTORIAL_ARG = 1500


def _safe_factorial(n):
    if isinstance(n, bool) or not isinstance(n, int) or not (0 <= n <= _MAX_FACTORIAL_ARG):
        raise ValueError("factorial() argument out of supported range")
    return math.factorial(n)


# Built-in round(x, ndigits) computes 10**(-ndigits) in C when x is an int
# and ndigits < 0, which causes unbounded CPU/memory consumption for large
# negative ndigits (e.g. round(1, -10**9)).
_MAX_ROUND_DIGITS = 1000


def _safe_round(number, ndigits=None):
    if ndigits is None:
        return round(number)
    if isinstance(ndigits, bool) or not isinstance(ndigits, int) or abs(ndigits) > _MAX_ROUND_DIGITS:
        raise ValueError("round() ndigits argument out of supported range")
    return round(number, ndigits)


class Calculator:
    def __init__(self):
        # Define the safe environment for simpleeval
        self.functions = {
            'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
            'asin': math.asin, 'acos': math.acos, 'atan': math.atan,
            'sqrt': math.sqrt, 'log': math.log, 'log10': math.log10, 'log2': math.log2,
            'exp': math.exp, 'abs': abs, 'round': _safe_round, 'pow': math.pow,
            'min': min, 'max': max, 'factorial': _safe_factorial,
            'degrees': math.degrees, 'radians': math.radians,
            'ceil': math.ceil, 'floor': math.floor
        }
        self.names = {
            'pi': math.pi,
            'e': math.e,
            'tau': math.tau
        }
        self.operators = {
            **DEFAULT_OPERATORS,
            ast.Mod: _safe_mod,
            ast.Pow: _safe_power,
            ast.Mult: _safe_mult,
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
        factorial_pattern = r'(\d+(?:\.\d+)?|[a-zA-Z_][a-zA-Z0-9_]*|\([^)]+\))!(?!=)'
        query = re.sub(factorial_pattern, r'factorial(\1)', query)

        # Handle logN(x) syntax, e.g. log3(27) -> log(27, 3)
        # We look for log followed by digits, then (expr)
        # Regex uses ([^)]+) to match content inside parens up to the first closing parenthesis.
        # This prevents it from greedily consuming parentheses of outer functions (e.g. floor(log10(100))).
        # Limitation: The argument to logN cannot contain ")" (no nested function calls inside logN).
        log_pattern = r'log(\d+)\(([^)]+)\)'
        if re.search(log_pattern, query):
             def replace_log(match):
                 base = match.group(1)
                 expr = match.group(2)
                 return f"log({expr}, {base})"
             query = re.sub(log_pattern, replace_log, query)
        
        return query

    def evaluate(self, query):
        """
        Safely evaluates a math expression.
        Returns the result as a number (int or float) or raises an exception.
        """
        if not query:
            return None

        # A math calculator has no legitimate use for string literals,
        # and every string-valued expression (string constants,
        # %-formatting, f-strings, string method calls) requires a quote
        # character. simpleeval's MAX_STRING_LENGTH guard does not bound
        # format-spec expansion, so reject quoted input before any
        # rewriting or evaluation happens.
        if '"' in query or "'" in query:
            raise ValueError("String literals are not allowed in calculator queries")

        # Preprocess the query
        query = self._preprocess(query)
        
        # Allow using ^ for power
        query = query.replace('^', '**')

        try:
            evaluator = MathOnlyEval(
                functions=self.functions,
                names=self.names,
                operators=self.operators
            )
            result = evaluator.eval(query)
            return result
        except (InvalidExpression, SyntaxError, TypeError, ZeroDivisionError, ValueError, OverflowError) as e:
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
        if isinstance(result, bool):
            return str(result)
        if isinstance(result, int):
            return str(result)
        if isinstance(result, float):
            if math.isfinite(result) and result.is_integer():
                return str(int(result))
            return f"{result:g}"
        return str(result)
