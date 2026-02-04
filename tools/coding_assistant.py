#!/usr/bin/env python3
"""
🤖 NANBA CODING ASSISTANT
=========================
AI-powered coding assistant using OpenAI API

Usage:
    python3 coding_assistant.py "Create a Python function to calculate fibonacci"
    python3 coding_assistant.py --file script.py "Add error handling to this code"
    
Environment:
    Set OPENAI_API_KEY in your environment or .env file
"""

import os
import sys
import argparse
from pathlib import Path

try:
    from openai import OpenAI
except ImportError:
    print("❌ Installing openai package...")
    os.system("pip install openai -q")
    from openai import OpenAI

# Load API key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    # Try to load from .env
    try:
        from dotenv import load_dotenv
        load_dotenv()
        OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    except:
        pass

if not OPENAI_API_KEY:
    print("❌ OPENAI_API_KEY not found!")
    print("Set it in environment or create .env file:")
    print("  echo 'OPENAI_API_KEY=your_key_here' > .env")
    sys.exit(1)

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """You are an expert software developer and coding assistant.
Provide clean, well-documented, production-ready code.
Include comments explaining complex logic.
Follow best practices for the requested language."""

def generate_code(prompt, language="python", context=None):
    """Generate code using OpenAI API"""
    
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
    ]
    
    if context:
        messages.append({"role": "user", "content": f"Context:\n```\n{context}\n```"})
    
    messages.append({"role": "user", "content": f"Language: {language}\n\nRequest: {prompt}"})
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # or gpt-4o if available
            messages=messages,
            temperature=0.7,
            max_tokens=2000
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

def explain_code(code, language="python"):
    """Explain what code does"""
    
    prompt = f"""Explain this {language} code in detail:

```
{code}
```

Provide:
1. What the code does
2. Key functions/components
3. How to use it
4. Any potential issues"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful coding tutor."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=1500
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

def review_code(code, language="python"):
    """Review code for issues"""
    
    prompt = f"""Review this {language} code for:
- Bugs or errors
- Security issues
- Performance problems
- Best practice violations
- Code style issues

```
{code}
```

Provide specific recommendations with line references."""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a senior code reviewer. Be thorough and specific."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=2000
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

def main():
    parser = argparse.ArgumentParser(description='AI Coding Assistant')
    parser.add_argument('prompt', help='What you want to create/modify')
    parser.add_argument('--file', '-f', help='File to read as context')
    parser.add_argument('--language', '-l', default='python', help='Programming language')
    parser.add_argument('--explain', '-e', action='store_true', help='Explain code instead of generating')
    parser.add_argument('--review', '-r', action='store_true', help='Review code for issues')
    parser.add_argument('--output', '-o', help='Save output to file')
    
    args = parser.parse_args()
    
    context = None
    if args.file and os.path.exists(args.file):
        with open(args.file, 'r') as f:
            context = f.read()
        print(f"📄 Loaded context from: {args.file}\n")
    
    print("🤖 Nanba Coding Assistant")
    print("=" * 50)
    
    if args.explain and context:
        print("🔍 Explaining code...\n")
        result = explain_code(context, args.language)
    elif args.review and context:
        print("🔍 Reviewing code...\n")
        result = review_code(context, args.language)
    else:
        print(f"💻 Generating {args.language} code...\n")
        result = generate_code(args.prompt, args.language, context)
    
    print(result)
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(result)
        print(f"\n✅ Saved to: {args.output}")

if __name__ == "__main__":
    main()
