# 🤖 NANBA CODING ASSISTANT

AI-powered coding assistant using your OpenAI API key.

---

## 🚀 Quick Start

### 1. Add Your OpenAI API Key

```bash
cd /root/.openclaw/workspace
cp .env.example .env
nano .env  # Edit and add your key
```

Get your API key from: https://platform.openai.com/api-keys

### 2. Install Dependencies

```bash
./setup_coding_assistant.sh
```

### 3. Start Coding!

---

## 💻 Usage Examples

### Generate New Code

```bash
# Create a Python function
python3 coding_assistant.py "Create a function to download images from URLs"

# Create in specific language
python3 coding_assistant.py -l javascript "Create a React component for a login form"

# Create with context from existing file
python3 coding_assistant.py -f my_project/utils.py "Add a function to validate emails"
```

### Explain Code

```bash
# Explain what code does
python3 coding_assistant.py -f myscript.py --explain
```

### Review Code

```bash
# Get code review
python3 coding_assistant.py -f myscript.py --review
```

### Save Output

```bash
# Save generated code to file
python3 coding_assistant.py "Create a Flask API" -o app.py
```

---

## 📝 Features

| Feature | Command |
|---------|---------|
| **Generate Code** | `python3 coding_assistant.py "your request"` |
| **Explain Code** | `python3 coding_assistant.py -f file.py --explain` |
| **Review Code** | `python3 coding_assistant.py -f file.py --review` |
| **Context-Aware** | `python3 coding_assistant.py -f file.py "modify this"` |
| **Multi-Language** | `python3 coding_assistant.py -l javascript "..."` |

---

## 🎯 Example Outputs

### Code Generation
```bash
$ python3 coding_assistant.py "Create a Python class for a trading bot"

✅ Generates complete TradingBot class with:
   - __init__ method
   - buy/sell methods
   - Error handling
   - Documentation
```

### Code Explanation
```bash
$ python3 coding_assistant.py -f nanba_momentum_trader.py --explain

📖 Provides:
   - What the code does
   - Key functions explained
   - Usage examples
   - Architecture overview
```

### Code Review
```bash
$ python3 coding_assistant.py -f myscript.py --review

🔍 Identifies:
   - Bugs and errors
   - Security issues
   - Performance problems
   - Best practice violations
```

---

## 💰 Cost

Uses OpenAI API pricing:
- **gpt-4o-mini**: ~$0.15 per 1M tokens (cheap!)
- **gpt-4o**: ~$5 per 1M tokens (more capable)

Default is gpt-4o-mini for cost efficiency.

---

## 🔧 Advanced Usage

### Custom System Prompt
Edit `coding_assistant.py` and modify `SYSTEM_PROMPT`.

### Change Model
Edit the `model=` parameter in the script:
- `gpt-4o-mini` (default, cheap)
- `gpt-4o` (better quality)
- `gpt-3.5-turbo` (fastest)

---

**Ready to code like a pro, boss!** 🐾🚀
