# core/memory.py
# Memory system — stores conversation history for an agent.
# Demonstrates: encapsulation, properties, __len__, __iter__,
#               __getitem__, __contains__, composition with Message


from email.mime import message
from operator import index

from core.message import Message


class Memory:
    """
    Stores an agent's conversation history with a configurable window size.
    Older messaages are automatically trimmed to stay within the window.
    """

    def __init__(self, max_size = 20):
        self.__messages   = []
        self.__max_size   = max_size
        self.__trim_count = 0


    # ── Properties ─────────────────────────────────────────────────────
    @property
    def max_size(self):
        return self.__max_size

    @max_size.setter
    def max_size(self, value):
        if not isinstance(value, int) or value < 1:
            raise ValueError("max_size must be a positive integer")
        self.__max_size = value
        self.__trim()

    @property
    def is_empty(self):
        return len(self.__messages) == 0

    @property
    def trim_count(self):
        """How many messages have been evicted to maintain max_size."""
        return self.__trim_count

    # ── Public Methods ────────────────────────────────────────────────
    def add(self, message):
        """Add a message, trim oldest if over max_size."""
        if not isinstance(message, Message):
            raise TypeError("Expected Message, got {type(message).__name__}")
        self.__messages.append(message)
        self.__trim()

    def add_user(self, content, **meta):
        self.add(Message.user(content, **meta))

    def add_assistant(self, content, **meta):
        self.add(Message.assistant(content, **meta))

    def last(self, n=1):
        """Return last n messages."""
        return self.__messages[-n:]

    def all_messages(self):
        """Return a copy of all messages (not the internal list)."""
        return list(self.__messages)

    def messages_by_role(self, role):
        """Filter messages by role."""
        return [m for m in self.__messages if m.role == role]

    def clear(self):
        """Wipe all memory."""
        self.__messages = []

    def summary(self):
        """Return stats about the memory."""
        total_words = sum(len(m) for m in self.__messages)
        role_counts = {}
        for m in self.__messages:
            role_counts[m.role] = role_counts.get(m.role, 0) + 1
        return {
            "stored" : len(self.__messages),
            "max_size" : self.__max_size,
            "total_words": total_words,
            "trimmed" : self.__trim_count,
            "by_role" : role_counts,
        }


    # ── Private methods ────────────────────────────────────────────────
    def __trim(self):
        """Remove oldest messages to stay within max_size."""
        while len(self.__messages) > self.__max_size:
            self.__messages.pop(0)
            self.__trim_count += 1


    # ── Dunder methods ─────────────────────────────────────────────────
    def __len__(self):
        return len(self.__messages)
    
    def __iter__(self):
        return iter(self.__messages)

    def __contains__(self, message):
        return message in self.__messages

    def __getitem__(self, index):
        return self.__messages[index]
    
    def __str__(self):
        if self.is_empty:
            return "Memory(empty)"
        lines = [f"Memory({len(self)}/{self.__max_size} messages):"]
        for msg in self.__messages[-3:]:
            lines.append(f" {msg.role:>10}: {msg.preview}")
        return "\n".join(lines)

    def __repr__(self):
        return f"Memory(max_size={self.__max_size}, stored={len(self)})"