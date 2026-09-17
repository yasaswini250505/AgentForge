# core/base_agent.py
# Abstract base class for all agents.
# Demonstrates: ABC, composition (has Memory + Tools), properties,
#              @classmethod, polymorphism via run()

from abc import ABC, abstractmethod
from email import message
from json import tool
from core.memory import Memory
from core.message import Message


class BaseAgent(ABC):
    """
    Abstract base for every agent in AgentForge.
    Every agent HAS-A Memory and a collection of Tools.
    Concrete agents implement run() differently — polymorphism.
    """

    _agent_registry = {} # class-level registry of all created agents
    def __init__(self, name, model="gpt-4o", max_memory=20):
        self._name = name
        self._model = model
        self._memory = Memory(max_size=max_memory) # composition
        self._tools = {} # {tool_name: BaseTool}
        self._run_count = 0
        BaseAgent._agent_registry[name] = self

    # ── Abstract methods — every agent must implement ──────────────────
    @abstractmethod
    def run(self, user_input):
        """Process user input and return a response string."""
        pass

    @property
    @abstractmethod
    def agent_type(self):
        """Short label: 'chat', 'analyst', 'router', etc."""
        pass

    # ── Properties ─────────────────────────────────────────────────────
    @property
    def name(self):
        return self._name

    @property
    def model(self):
        return self._model

    @property
    def memory(self):
        return self._memory

    @property
    def run_count(self):
        return self._run_count

    @property
    def tool_names(self):
        return list(self._tools.keys())

    # ── Tool management ────────────────────────────────────────────────
    def add_tool(self, tool):
        """Add a tool to this agent. Duck typing — any object with .name and .run() works."""
        if not (hasattr(tool, "name") and hasattr(tool, "run")):
            raise TypeError(f"Tool must have 'name' and 'run' attributes")
        self._tools[tool.name] = tool
        return self # allow chaining: agent.add_tool(a).add_tool(b)
    
    def remove_tool(self, tool_name):
        if tool_name in self._tools:
            del self._tools[tool_name]
    
    def use_tool(self, tool_name, input_text):
        """Use a tool by name. Returns tool result or error message."""
        if tool_name not in self._tools:
            return f"Tool '{tool_name}' not available. Available: {self.tool_names}"
        return self._tools[tool_name](input_text) # __call__ on tool

    def has_tool(self, tool_name):
        return tool_name in self._tools
    
    # ── Memory helpers ─────────────────────────────────────────────────
    def remember(self, message):
        self._memory.add(message)

    def recall(self, n=5):
        return self._memory.last(n)
    
    def clear_memory(self):
        self._memory.clear()

    # ── Class methods ──────────────────────────────────────────────────
    @classmethod
    def get_agent(cls, name):
        return cls._agent_registry.get(name)

    @classmethod
    def list_all_agents(cls):
        return list(cls._agent_registry.keys())
    
    @classmethod
    def total_agents(cls):
        return len(cls._agent_registry)
    
    # ── Internal helper for subclasses ────────────────────────────────
    def _execute(self, user_input):
        """
        Shared pre/post logic wrapping each run() call.
        Saves to memory, increments counter.
        Subclasses call this instead of run() directly.
        """
        self._run_count += 1
        user_msg = Message.user(user_input)
        self._memory.add(user_msg)
        response = self.run(user_input)
        asst_msg = Message.assistant(response)
        self._memory.add(asst_msg)
        return response

    # ── Dunder methods ─────────────────────────────────────────────────
    def __str__(self):
        return (f"Agent({self.name!r}, type={self.agent_type}, "
    f"model={self.model!r}, tools={self.tool_names})")

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name!r})"
    
    def __call__(self, user_input):
        """Makes agent callable: agent('Hello') === agent._execute('Hello')"""
        return self._execute(user_input)
    
    def __contains__(self, tool_name):
        """'calculator' in agent → checks if tool registered."""
        return tool_name in self._tools
    
    def __len__(self):
        """len(agent) → number of tools registered."""
        return len(self._tools)