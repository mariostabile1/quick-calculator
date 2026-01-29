# Quick Calculator Ulauncher Extension

A simple yet powerful scientific calculator for Ulauncher.

## Features
- **Fast Access**: Trigger with `qc` keywords.
- **Scientific Functions**: Supports `sqrt`, `sin`, `cos`, `tan`, `log`, `pi`, `e`, and more (from Python's `math` module).
- **Clipboard Integration**: Press `Enter` to copy the result to the clipboard.
- **Real-time Evaluation**: Shows results as you type.

## Usage
Type `qc` followed by your mathematical expression.

Examples:
- `qc 2 + 2` -> `4`
- `qc sqrt(16)` -> `4.0`
- `qc sin(pi)` -> `1.22e-16` (approx 0)
- `qc 2^10` -> `1024` (Note: standard python `**` power operator works too, and bitwise `^` is supported as bitwise XOR if using standard python syntax, but usually people want power. *Note: The current implementation uses Python syntax, so `**` is power and `^` is XOR.*)

## Installation
Clone this repository into your Ulauncher extensions directory:
```bash
git clone https://github.com/yourusername/quick-calculator.git ~/.local/share/ulauncher/extensions/com.github.yourusername.quick-calculator
```
Restart Ulauncher.
