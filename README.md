# Quick Calculator Extension for Ulauncher

A simple yet powerful scientific calculator for Ulauncher, now safer and more robust.

Give a ⭐ if you like the extension.

## Features
- **Fast Access**: Trigger with `qc` keywords.
- **Secure Evaluation**: Uses `simpleeval` to safely calculate expressions without executing arbitrary code.
- **Scientific Functions**: Supports a wide range of math functions including:
    - **Trigonometry**: `sin`, `cos`, `tan`, `asin`, `acos`, `atan`
    - **Mathematics**: `sqrt`, `log` (ln), `log10`, `log2`, `exp`, `factorial`, `abs`, `round`, `min`, `max`, `pow`
    - **Constants**: `pi`, `e`, `tau`
    - **Utilities**: `degrees`, `radians`, `ceil`, `floor`
- **Smart Error Handling**: Provides clear messages for syntax errors or invalid math operations.
- **Clipboard Integration**: Press `Enter` to copy the calculated result.

## Usage

Type `qc` followed by your mathematical expression.

### Arithmetic & Basics
- `qc 2 + 2` -> `4`
- `qc 10 / 3` -> `3.33333`
- `qc 2^10` -> `1024` (Power)
- `qc sqrt(16)` -> `4` (Square root)
- `qc abs(-50)` -> `50` (Absolute value)
- `qc 15 % 4` -> `3` (Modulo)

### Trigonometry
- `qc sin(pi/2)` -> `1`
- `qc cos(0)` -> `1`
- `qc tan(pi/4)` -> `1`
- `qc degrees(pi)` -> `180`
- `qc radians(180)` -> `3.14159...`

### Factorials & Combinatorics
- `qc 5!` -> `120`
- `qc factorial(5)` -> `120`
- `qc (3+2)!` -> `120`
*(Note: `!` must be immediately after the number or parenthesis)*

### Constants & Logarithms
- `qc pi` -> `3.14159...`
- `qc e` -> `2.71828...`
- `qc log(e)` -> `1` (Natural log)
- `qc log10(100)` -> `2`
- `qc log2(8)` -> `3`
- `qc log3(27)` -> `3` (Supports `logN(x)` syntax for any base `N`)

### Rounding
- `qc round(3.6)` -> `4`
- `qc floor(3.9)` -> `3`
- `qc ceil(3.1)` -> `4`

## Installation

### Prerequisites

This extension requires the `simpleeval` Python library for secure calculations.

**Why?** Ulauncher (v5+) uses your system's Python 3 environment to run extensions, but it **does not** automatically install dependencies. You must install them manually.

**How to Install:**

Run the following command in your terminal:

```bash
pip3 install --user simpleeval
```

> **Note**: The `--user` flag is recommended to install the library for your current user without affecting the system-wide Python installation.

Alternatively, if you prefer using `pip`:
```bash
pip install --user simpleeval
```

If you encounter issues, verify that `simpleeval` is installed for the same Python version that Ulauncher is using (usually `/usr/bin/python3`).

### Install Extension
Clone this repository into your Ulauncher extensions directory:

```bash
git clone https://github.com/mariostabile1/quick-calculator.git ~/.local/share/ulauncher/extensions/com.github.mariostabile1.quick-calculator
```

Or add the extension via ULauncher Preferences → Extensions → Add extension.

**Restart Ulauncher** after installation.

## Development

To run tests locally:

1.  Create a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
2.  Install dependencies:
    ```bash
    pip install simpleeval
    ```
3.  Run tests:
    ```bash
    python3 test_logic.py
    ```
