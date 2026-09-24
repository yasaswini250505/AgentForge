# tools/search_tool.py
# Simulated search tool — returns relevant mock results based on query.
# Demonstrates: inheritance, class-level data (knowledge base), static methods

from logging import log

from core.base_tool import BaseTool


class SearchTool(BaseTool):
    """
    Simulates a web search. Uses a built-in knowledge base to return
    context-relevant results. In a real system, this would call an API.
    """

    # Class-level knowledge base (simulated search index)
    _KNOWLEDGE_BASE = {
        "python"           : "Python is a high-level, interpreted language known for readability. Latest version: 3.12.",
        "oop"              : "Object-Oriented Programming uses classes, objects, inheritance, encapsulation, and polymorphism.",
        "fastapi"          : "FastAPI is a modern Python web framework for building APIs, based on type hints.",
        "langchain"        : "LangChain is a framework for building applications with large language models (LLMs).",
        "machine learning" : "ML enables computers to learn patterns from data without being explicitly programmed.",
        "data engineering" : "Data Engineering involves building pipelines to collect, store, and process large data.",
        "sql"              : "SQL (Structured Query Language) is used to manage and query relational databases.",
        "api"              : "API (Application Programming Interface) allows different systems to communicate.",
        "recursion"        : "Recursion is a function calling itself with a smaller input until a base case is reached.",
        "big o"            : "Big O notation describes algorithm efficiency. O(1) constant, O(n) linear, O(log n) logarithmic.",
        "agent"            : "An AI agent perceives its environment, reasons, and takes actions to achieve goals.",
        "default"          : "No specific result found. Please search for: python, oop, fastapi, langchain, sql, or api.",
    }

    @property
    def name(self):
        return "web_search"

    @property
    def description(self):
        return "Search for information. Input: topic or question. Returns relevant information."
    
    def run(self, query):
        """Search for the query in the knowledge base."""
        query_lower = query.lower()
        result = self._find_best_match(query_lower)
        return f"Search result for '{query}': {result}"
    
    def _find_best_match(self, query):
        """Find the most relevant entry in the knowledge base."""
        # Check for exact keyword match first
        for key, value in self._KNOWLEDGE_BASE.items():
            if key in query:
                return value

        # Check if any word in the query matches a key
        query_words = set(query.split())
        for key, value in self._KNOWLEDGE_BASE.items():
            key_words = set(key.split())
            if query_words & key_words: # intersection
                return value
            
        return self._KNOWLEDGE_BASE["default"]