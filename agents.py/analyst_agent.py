# # agents/analyst_agent.py
# Data analysis agent — analyses lists of numbers.
# Demonstrates: inheritance, static methods, encapsulation, properties

from email.mime import text
import math
from xml.parsers.expat import model

from distro import name
from core.base_agent import BaseAgent
from utils.logger    import LoggingMixin


class AnalystAgent(LoggingMixin, BaseAgent):
    """
    Specialised agent for numerical data analysis.
    Extracts numbers from text, computes statistics.
    """

    def __init__(self, name, model="gpt-4o"):
        super().__init__(name, model)
        self._reports = []
        self._info(f"AnalystAgent '{name}' ready")

    @property
    def agent_type(self):
        return "analyst"
    
    @property
    def report_count(self):
        return len(self._reports)
    
    def run(self, user_input):
        """Extract and analyse numbers from user input."""
        numbers = self._extract_numbers(user_input)

        if not numbers:
            self._warn("No numbers found in input")
            return f"I couldn't find numbers to analyse in: {user_input!r}"
        
        stats  = self._compute_stats(numbers)
        report = self._build_report(numbers, stats)
        self._reports.append(report)
        self._info(f"Analysis complete", {"numbers": len(numbers)})
        return report

    def get_reports(self):
        """Return all analysis reports."""
        return list(self._reports)

    # ── Private methods ────────────────────────────────────────────────
    def _extract_numbers(self, text):
        """Pull all numbers from a text string."""
        numbers = []
        for word in text.replace(",", " ").split():
            clean = word.strip(".,!?;:()")
            if clean.lstrip("-").replace(".", "").isdigit():
                numbers.append(float(clean))
        return numbers
    
    def _compute_stats(self, numbers):
        """Compute full descriptive statistics."""
        n = len(numbers)
        total = sum(numbers)
        mean = total / n
        sorted_n = sorted(numbers)
        mid = n // 2
        median = (sorted_n[mid] if n % 2 
                  else (sorted_n[mid-1] + sorted_n[mid]) / 2)
        variance = sum((x - mean)**2 for x in numbers) / n
        std_dev = math.sqrt(variance)

        freq = {}
        for x in numbers:
            freq[x] = freq.get(x, 0) + 1
        mode = max(freq, key=freq.get)

        return {
            "count" : n,
            "sum" : round(total, 4),
            "mean" : round(mean, 4),
            "median" : round(median, 4),
            "mode" : mode,
            "std_dev": round(std_dev, 4),
            "min" : sorted_n[0],
            "max" : sorted_n[-1],
            "range" : sorted_n[-1] - sorted_n[0],
        }

    def _build_report(self, numbers, stats):
        lines = [
            f"Analysis of {stats['count']} values: {numbers}",
            f" Sum : {stats['sum']}",
            f" Mean : {stats['mean']}",
            f" Median : {stats['median']}",
            f" Mode : {stats['mode']}",
            f" Std Dev : {stats['std_dev']}",
            f" Min/Max : {stats['min']} / {stats['max']}",
            f" Range : {stats['range']}",
        ]
        return "\n".join(lines)
    
    @staticmethod
    def is_data_query(text):
        """Quick check if text looks like a data analysis request."""
        triggers = ["analyse","analyze","statistics","mean","average","data","numbers"]
        return any(t in text.lower() for t in triggers)