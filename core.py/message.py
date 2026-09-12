# core/message.py
# Message class — the data unit passed between agents and tools.
# Demonstrates: __str__, __repr__, __eq__, __add__, __len__,
#               __bool__, __contains__, @classmethod, @staticmethod


class Message:
    """
    Represents a single message in the agent system.
    Supports concatenation, comparison and iteration.
    """

    ROLES = {"user", "assistant", "system", "tool"}
    _id_counter = 0

    def __init__(self, role, content, metadata=None):
        if role not in Message.ROLES:
            raise ValueError(f"role must be one of {Message.ROLES}, got {role!r}")
        Message._id_counter += 1
        self.id        = Message._id_counter
        self.role      = role
        self.content   = str(content)
        self.metadata  = metadata or {}
        self._tokens   = self.content.split()


    # ── Class methods — alternative constructors ───────────────────────
    @classmethod
    def user(cls, content, **meta):
        """Shortcut: Message.user('Hello back')"""
        return cls("user", content, meta)

    @classmethod
    def assistant(cls, content, **meta):
        """Shortcut: Message.assistant('Hello back')"""
        return cls("assistant", content, meta)

    @classmethod
    def system(cls, content):
        """Shortcut: Message.system('You are a helpful assistant')"""
        return cls("system", content)

    @classmethod
    def tool_result(cls, tool_name, result):
        """Shortcut: Message.tool_result('calculator', '42')"""
        return cls("tool", result, {"tool": tool_name})

    @classmethod
    def from_dict(cls, d):
        """Re-hydrate a message from a dict."""
        return cls(d["role"], d["content"], d.get("metadata", {}))


    # ── Static methods ─────────────────────────────────────────────────
    @staticmethod
    def is_valid_role(role):
        return role in Message.ROLES

    @staticmethod
    def total_created():
        return Message._id_counter


    # ── Properties ─────────────────────────────────────────────────────
    @property
    def id(self):
        return self._id

    @property
    def word_count(self):
        return len(self._tokens)

    @property
    def is_from_user(self):
        return self.role == "user"

    @property
    def preview(self):
        """First 40 chars of content."""
        if len(self.content) <= 40:
            return self.content
        return self.content[:37] + "..."


    # ── Dunder methods ─────────────────────────────────────────────────
    def __str__(self):
        return f"[{self.role.upper()}] {self.content}"

    def __repr__(self):
        return f"Message(role={self.role!r}, content={self.content[:30]!r})"

    def __len__(self):
        """len(msg) = number of words."""
        return self.word_count

    def __bool__(self):
        """bool(msg) = True if content is not empty."""
        return bool(self.content.strip())

    def __eq__(self, other):
        if not isinstance(other, Message):
            return False
        return self.role == other.role and self.content == other.content

    def __add__(self, other):
        """msg1 + msg2 = new message with cpmbines content."""
        if not isinstance(other, Message):
            raise TypeError(f"Cannot add Message and {type(other).__name__}")
        combined = self.content + " " + other.content
        return Message(self.role, combined, {**self.metadata, **other.metadata})

    def __contains__(self, word):
        """'hello' in msg → checks if word in content."""
        return word.lower() in self.content.lower()

    def __iter__(self):
        """for word in msg → iterates over words."""
        return iter(self._tokens)

    def to_dict(self):
        return {
            "id"       : self.id,
            "role"     : self.role,
            "content"  : self.content,
            "metadata" : self.metadata
        }