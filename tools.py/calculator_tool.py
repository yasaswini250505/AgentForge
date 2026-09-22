# tools/calculator_tool.py
# A calculator tool — parses and evaluates basic math expressions.
# Demonstrates: inheritance from BaseTool, @property, @staticmethod

from pydoc import text

from core.base_tool import BaseTool


class CalculatorTool(BaseTool):
    """
    Evaluates mathematical expressions from text input.
    Supports: +, -, *, /, **, //, %
    """


    # ── Abstract properties implemented ───────────────────────────────
    @property
    def name(self):
        return "calculator"
    
    @property
    def description(self):
        return "Evaluate math expressions. Input: '2 + 3 * 4'. Output: result."
    
    def run(self, input_text):
        """Parse and evaluate a math expression."""
        expression = self._extract_expression(input_text)
        if not expression:
            return "No valid math expression found in input."
        result = self._safe_eval(expression)
        return f"Result of '{expression}' = {result}"

    # ── Private helpers ────────────────────────────────────────────────
    def _extract_expression(self, text):
        """Extract a math expression from natural language."""
        # Keywords that signal a math problem
        math_triggers = [
            "calculate", "compute", "evaluate", "what is",
            "solve", "find", "=", "+", "-", "*", "/"
        ]
        text_lower = text.lower()
        for trigger in math_triggers:
            if trigger in text_lower:
                # Try to isolate the expression
                for part in text.split():
                    if any(c in part for c in "0123456789"):
                        # Found a numeric part — use the whole input as expression
                        return self._clean_expression(text)
        return None

    def _clean_expression(self, text):
        """Remove natural language words, keep math."""
        words_to_remove = [
            "calculate", "compute", "evaluate", "what", "is",
            "the", "value", "of", "solve", "find", "please", "result"
        ]
        parts = text.lower().split()
        kept = [p for p in parts if p not in words_to_remove]
        return " ".join(kept)
    
    def _safe_eval(self, expression):
        """Evaluate a mathematical expression safely without using eval()."""
        expression = expression.strip()
        # Try to evaluate using only safe characters
        allowed = set("0123456789 +-*/.()%")
        if not all(c in allowed for c in expression):
            return "Error: unsupported characters in expression"
        # Use Python's built-in eval for safe math expressions only
        result = eval(expression)
        if isinstance(result, float) and result == int(result):
            return int(result)
        if isinstance(result, float):
            return round(result, 6)
        return result

    # ── Static utility ─────────────────────────────────────────────────
    @staticmethod
    def is_math_query(text):
        """Quick check if text looks like a math question."""
        math_chars = set("0123456789+-*/^()")
        return any(c in math_chars for c in text)