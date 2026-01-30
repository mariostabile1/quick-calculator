# Quick Calculator Extension for Ulauncher

A simple yet powerful scientific calculator for Ulauncher.

## Features
- **Fast Access**: Trigger with `qc` keywords.
- **Scientific Functions**: Supports `sqrt`, `sin`, `cos`, `tan`, `log`, `pi`, `e`, and more (from Python's `math` module).
- **Smart Error Handling**: Provides clear messages for syntax errors or invalid math.
- **Robust Validation**: Ignores non-mathematical input (like text) to keep your results clean.
- **Clipboard Integration**: Press `Enter` to copy the calculated result.

## Usage
Type `qc` followed by your mathematical expression.

Examples:
- `qc 2 + 2` -> `4`
- `qc sqrt(16)` -> `4`
- `qc sin(pi)` -> `0` (or approx)
- `qc 2^10` -> `1024` (The `^` operator is automatically converted to power `**`)

## Installation
Clone this repository into your Ulauncher extensions directory:
```bash
git clone https://github.com/mariostabile1/quick-calculator.git ~/.local/share/ulauncher/extensions/com.github.mariostabile1.quick-calculator
```
or add the extension via ULauncher Preferences → Extensions → Add extension.
Than eestart Ulauncher.
