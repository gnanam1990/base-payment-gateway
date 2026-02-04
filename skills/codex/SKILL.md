# SKILL.md - Codex API Integration

## Name
codex

## Description
OpenAI Codex API integration for advanced code generation, explanation, and review. Uses OpenAI's GPT models optimized for coding tasks.

## Usage

### Generate Code
```python
from skills.codex import CodexAssistant

codex = CodexAssistant()
code = codex.generate(
    prompt="Create a Python function to calculate RSI",
    language="python"
)
```

### Explain Code
```python
explanation = codex.explain(code, language="python")
```

### Review Code
```python
review = codex.review(code, language="python")
```

### Modify Existing Code
```python
modified = codex.modify(
    file_path="script.py",
    instruction="Add error handling to the download function"
)
```

## Environment Variables
- `OPENAI_API_KEY` - Required. Your OpenAI API key

## Installation
```bash
pip install openai python-dotenv
```

## API Reference

### Methods

#### generate(prompt, language="python", context=None)
Generate code from description.
- **prompt**: Description of what to create
- **language**: Programming language
- **context**: Optional existing code for reference
- **Returns**: Generated code string

#### explain(code, language="python")
Explain what code does.
- **code**: Code to explain
- **language**: Programming language
- **Returns**: Detailed explanation

#### review(code, language="python")
Review code for issues.
- **code**: Code to review
- **language**: Programming language
- **Returns**: Review with bugs, security, performance issues

#### modify(file_path, instruction)
Modify existing code file.
- **file_path**: Path to code file
- **instruction**: What changes to make
- **Returns**: Modified code

## Models Used
- `gpt-4o-mini` - Default (fast, cheap)
- `gpt-4o` - High quality (more expensive)
- `gpt-3.5-turbo` - Fastest option

## Examples

### Example 1: Generate Trading Indicator
```python
code = codex.generate(
    "Create a function to calculate Bollinger Bands",
    language="python"
)
```

### Example 2: Explain Complex Code
```python
with open('trading_bot.py', 'r') as f:
    code = f.read()
    
explanation = codex.explain(code)
print(explanation)
```

### Example 3: Review for Bugs
```python
review = codex.review(my_code)
if 'error' in review.lower() or 'bug' in review.lower():
    print("Issues found!")
```

## Best Practices
1. Always provide clear, specific prompts
2. Use context when modifying existing code
3. Review generated code before using
4. Keep API key in .env, never commit it
5. Use gpt-4o-mini for cost efficiency

## Cost Estimates
- Simple function: ~$0.005
- Complex class: ~$0.02
- Code review: ~$0.01
- File modification: ~$0.03

## Troubleshooting

### "API key not found"
Set OPENAI_API_KEY environment variable or create .env file

### "Rate limit exceeded"
Add delay between requests or upgrade OpenAI plan

### "Context too long"
Split into smaller chunks or use file modification method
