# core/base_tool.py
# Abstract base class for all tools.
# Demonstrates: ABC, @abstractmethod, @clsssmethod, __call__

from abc import ABC, abstractmethod


class BaseTool(ABC):
    """
    Abstract base class — every tool MUST implement name, description, run().
    The __call__ method lets tools be called as functions: tool("input").
    """

    def __init__(self):
        self._call_count = 0
        self._last_input = None
        self._last_output = None

    @property
    @abstractmethod
    def name(self):
        """Unique tool name — used as the key in the registry."""
        pass

    @property
    @abstractmethod
    def description(self):
        """One-line description — shown to agents when choosing tools."""
        pass

    @abstractmethod
    def run(self, input_text):
        """Execute the tool. Must return a string result."""
        pass

    # ── Template method — do not override ─────────────────────────────
    def __call__(self, input_text):
        """
        Makes the tool callable: tool("input").
        Wraps run() with call tracking.
        """
        self._call_count += 1
        self._last_input  = input_text
        result            = self.run(input_text)
        self._last_output = result
        return result

    # ── Shared methods — available to all tools ────────────────────────
    @property
    def call_count(self):
        return self._call_count

    @property
    def stats(self):
        return {
            "name" : self.name,
            "calls" : self._call_count,
            "last_input" : self._last_input,
            "last_output": self._last_output,
        }

    @staticmethod
    def validate_input(input_text):
        """Check that input is a non-empty string."""
        return isinstance(input_text, str) and bool(input_text.strip())

    def __str__(self):
        return f"Tool({self.name!r}): {self.description}"
    
    def __repr__(self):
        return f"{self.__class__.__name__}(calls={self._call_count})"
    
    def __eq__(self, other):
        if not isinstance(other, BaseTool):
            return False
        return self.name == other.name