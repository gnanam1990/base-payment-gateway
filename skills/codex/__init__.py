"""
🤖 Codex API Skill
==================
OpenAI Codex integration for code generation and analysis

Usage:
    from skills.codex import CodexAssistant
    
    codex = CodexAssistant()
    code = codex.generate("Create a REST API in Flask")
"""

import os
from typing import Optional

try:
    from openai import OpenAI
except ImportError:
    raise ImportError("Install openai: pip install openai")


class CodexAssistant:
    """
    AI coding assistant powered by OpenAI Codex/GPT models
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        """
        Initialize Codex Assistant
        
        Args:
            api_key: OpenAI API key (or from env)
            model: Model to use (gpt-4o-mini, gpt-4o, gpt-3.5-turbo)
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError(
                "OpenAI API key required. Set OPENAI_API_KEY env var "
                "or pass api_key parameter"
            )
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        
        self.system_prompt = """You are an expert software developer. 
Provide clean, well-documented, production-ready code.
Include comments explaining complex logic. Follow best practices."""
    
    def generate(self, prompt: str, language: str = "python", 
                 context: Optional[str] = None) -> str:
        """
        Generate code from description
        
        Args:
            prompt: What to create
            language: Programming language
            context: Optional existing code
            
        Returns:
            Generated code
        """
        messages = [
            {"role": "system", "content": self.system_prompt}
        ]
        
        if context:
            messages.append({
                "role": "user",
                "content": f"Existing code context:\n```{language}\n{context}\n```"
            })
        
        messages.append({
            "role": "user",
            "content": f"Create {language} code for: {prompt}\n\n"
                      f"Provide only the code, no explanations outside code blocks."
        })
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=2000
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating code: {e}"
    
    def explain(self, code: str, language: str = "python") -> str:
        """
        Explain what code does
        
        Args:
            code: Code to explain
            language: Programming language
            
        Returns:
            Detailed explanation
        """
        prompt = f"""Explain this {language} code in detail:

```{language}
{code}
```

Provide:
1. Overview of what it does
2. Key functions/components explained
3. How to use it
4. Any important notes or caveats"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful coding tutor."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=1500
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error explaining code: {e}"
    
    def review(self, code: str, language: str = "python") -> str:
        """
        Review code for issues
        
        Args:
            code: Code to review
            language: Programming language
            
        Returns:
            Review with issues and recommendations
        """
        prompt = f"""Review this {language} code for issues:

```{language}
{code}
```

Check for:
- Bugs or logical errors
- Security vulnerabilities
- Performance problems
- Best practice violations
- Code style issues

Provide specific recommendations with line references if possible."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a senior code reviewer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error reviewing code: {e}"
    
    def modify(self, file_path: str, instruction: str) -> str:
        """
        Modify existing code file
        
        Args:
            file_path: Path to code file
            instruction: What changes to make
            
        Returns:
            Modified code
        """
        try:
            with open(file_path, 'r') as f:
                existing_code = f.read()
        except Exception as e:
            return f"Error reading file: {e}"
        
        # Detect language from extension
        ext = file_path.split('.')[-1].lower()
        lang_map = {
            'py': 'python', 'js': 'javascript', 'ts': 'typescript',
            'go': 'go', 'rs': 'rust', 'java': 'java', 'cpp': 'cpp',
            'c': 'c', 'rb': 'ruby', 'php': 'php'
        }
        language = lang_map.get(ext, 'python')
        
        prompt = f"""Modify this {language} code according to the instruction.

Instruction: {instruction}

Existing code:
```{language}
{existing_code}
```

Provide the complete modified code."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=2500
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error modifying code: {e}"
    
    def refactor(self, code: str, language: str = "python", 
                 goal: str = "improve readability") -> str:
        """
        Refactor code for better quality
        
        Args:
            code: Code to refactor
            language: Programming language
            goal: What to improve (readability, performance, etc.)
            
        Returns:
            Refactored code
        """
        prompt = f"""Refactor this {language} code to {goal}:

```{language}
{code}
```

Provide the improved version with comments explaining changes."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=2000
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error refactoring code: {e}"
    
    def test_generate(self, code: str, language: str = "python") -> str:
        """
        Generate unit tests for code
        
        Args:
            code: Code to test
            language: Programming language
            
        Returns:
            Generated test code
        """
        prompt = f"""Generate comprehensive unit tests for this {language} code:

```{language}
{code}
```

Include tests for:
- Normal cases
- Edge cases
- Error conditions

Use appropriate testing framework for {language}."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=2000
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating tests: {e}"


# Convenience functions for quick usage
def generate_code(prompt: str, language: str = "python") -> str:
    """Quick code generation"""
    assistant = CodexAssistant()
    return assistant.generate(prompt, language)


def explain_code(code: str, language: str = "python") -> str:
    """Quick code explanation"""
    assistant = CodexAssistant()
    return assistant.explain(code, language)


def review_code(code: str, language: str = "python") -> str:
    """Quick code review"""
    assistant = CodexAssistant()
    return assistant.review(code, language)
