# agents/chat_agent.py
# Conversational agent — handles general questions.
# Demonstrates: inheritance from BaseAgent, polymorphism, composition,
# mixin (LoggingMixin + BaseAgent), super()

from xml.parsers.expat import model

from distro import name

from core.base_agent import BaseAgent
from core.message import Message
from utils.logger import LoggingMixin


class ChatAgent(LoggingMixin, BaseAgent):
    """
    A general-purpose conversational agent.
    Inherits from both LoggingMixin and BaseAgent (multiple inheritance).
    """

    GREETINGS = {"hi","hello","hey","greetings","good morning","good evening"}

    def __init__(self, name, model="gpt-4o", personality="helpful"):
        super().__init__(name, model)
        self.personality = personality
        self._info(f"ChatAgent '{name}' initialised", {"personality" : personality})

    @property
    def agent_type(self):
        return "chat"

    def run(self, user_input):
        """
        Process user input and generate a contextual response.
        This is where polymorphism lives — each agent type responds differently.
        """
        self._debug(f"Processing input", {"len": len(user_input)})
        lower = user_input.lower().strip()

        # Greeting detection
        if any(g in lower for g in self.GREETINGS):
            return self._greet(user_input)

        # Question detection
        if lower.endswith("?") or lower.startswith(("what","how","why","when","who","where")):
            return self._answer_question(user_input)
        
        # Tool usage
        if self._tools:
                best_tool = self._pick_tool(lower)
                if best_tool:
                    self._info(f"Using tool", {"tool": best_tool})
                    result = self.use_tool(best_tool, user_input)
                    return f"I used the {best_tool} tool to help you: {result}"
        
        # Default response
        return self._default_response(user_input)

    # ── Private response generators ────────────────────────────────────
    def _greet(self, user_input):
        context = ""
        if len(self.memory) > 0:
            context = " Welcome back!"
        return (f"Hello! I'm {self.name}, your {self.personality} assistant.{context} "
                f"How can I help you today?")
    
    def _answer_question(self, question):
        # Check if we can use a tool
        for tool_name, tool in self._tools.items():
            if any(kw in question.lower()
                    for kw in ["calculate","compute","search","find","reverse","sentiment"]):
                result = self.use_tool(tool_name, question)
                return f"Great question! Here is what I found: {result}"
            
        # Use memory context if available
        recent = self.memory.last(3)
        context = f" (Based on our {len(self.memory)} previous messages)" if recent else ""
        return f"That is a thoughtful question{context}. Let me think about: {question!r}"
         
    def _pick_tool(self, text):
        """Choose the best tool for the input."""
        if any(c in text for c in "0123456789") and any(c in text for c in "+- */"):
            if "calculator" in self._tools:
                return "calculator"
        if "reverse" in text or "sentiment" in text or "word" in text:
            if "text_analyser" in self._tools:
                return "text_analyser"
        if "search" in text or "what is" in text or "tell me about" in text:
            if "web_search" in self._tools:
                return "web_search"
        return None

    def _default_response(self, text):
        """Generate a default response when no specific action is needed."""
        turn = self.run_count
        return (f"I understand you said: {text!r}. "
                f"This is our message #{turn}. "
                f"I have {len(self._tools)} tool(s) available: "
                f"{self.tool_names}.")