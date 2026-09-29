# tools/calculator_tool.py
# A calculator tool — parses and evaluates basic math expressions.
# Demonstrates: inheritance from BaseTool, @property, @staticmethod

import ast
import operator

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
        operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.FloorDiv: operator.floordiv,
            ast.Mod: operator.mod,
            ast.Pow: operator.pow,
            ast.UAdd: operator.pos,
            ast.USub: operator.neg,
        }

        def evaluate(node):
            if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
                return node.value
            if isinstance(node, ast.UnaryOp) and type(node.op) in operators:
                return operators[type(node.op)](evaluate(node.operand))
            if isinstance(node, ast.BinOp) and type(node.op) in operators:
                return operators[type(node.op)](evaluate(node.left), evaluate(node.right))
            raise ValueError("unsupported characters or syntax in expression")

        try:
            tree = ast.parse(expression.strip(), mode="eval")
            result = evaluate(tree.body)
        except (SyntaxError, ValueError, TypeError, ZeroDivisionError, OverflowError) as exc:
            return f"Error: {exc}"
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