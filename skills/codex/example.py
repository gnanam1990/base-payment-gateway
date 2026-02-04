#!/usr/bin/env python3
"""
🧪 Codex Skill Test/Example
===========================
Example usage of the Codex API skill
"""

import sys
sys.path.insert(0, '/root/.openclaw/workspace')

from skills.codex import CodexAssistant, generate_code, explain_code

# Example 1: Generate a function
print("=" * 60)
print("Example 1: Generate Code")
print("=" * 60)

code = generate_code(
    "Create a function to calculate Fibonacci sequence",
    language="python"
)
print(code)

# Example 2: Explain code
print("\n" + "=" * 60)
print("Example 2: Explain Code")
print("=" * 60)

sample_code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
"""

explanation = explain_code(sample_code)
print(explanation)

# Example 3: Using the class directly
print("\n" + "=" * 60)
print("Example 3: Full Class Usage")
print("=" * 60)

codex = CodexAssistant()

# Generate with context
existing_utils = """
def calculate_sma(prices, period=20):
    return sum(prices[-period:]) / period
"""

new_indicator = codex.generate(
    prompt="Add a function to calculate EMA (Exponential Moving Average)",
    language="python",
    context=existing_utils
)
print(new_indicator)

# Example 4: Review code
print("\n" + "=" * 60)
print("Example 4: Code Review")
print("=" * 60)

buggy_code = """
def divide(a, b):
    return a / b

result = divide(10, 0)
"""

review = codex.review(buggy_code)
print(review)

print("\n" + "=" * 60)
print("✅ All examples completed!")
print("=" * 60)
