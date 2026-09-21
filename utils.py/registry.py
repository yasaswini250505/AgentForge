# utils/registry.py
# Global registry for tools and agents.
# Demonstrates: class variables, @classmethod, __contains__,
#               __iter__, __len__, __getitem__


class Registry:
    """
    Global registry for tools and agents.
    Supports duck typing — anything with .name works.
    """

    def __init__(self, registry_type="generic"):
        self.registry_type = registry_type
        self._items = {}

    def register(self, item):
        """Register any item that has a .name attribute."""
        if not hasattr(item, "name"):
            raise ValueError("Item must have a 'name' attribute")
        name = item.name if not callable(item.name) else item.name
        self._items[name] = item
        return item # allows use as decorator: @registry.register

    def get(self, name, default=None):
        return self._items.get(name, default)

    def all_names(self):
        return list(self._items.keys())

    def all_items(self):
        return list(self._items.values())

    def remove(self, name):
        if name in self._items:
            del self._items[name]

    # ── Dunder methods ────────────────────────────────────────────────

    def __contains__(self, name):
        return name in self._items

    def __getitem__(self, name):
        if name not in self._items:
            raise KeyError(f"{self.registry_type} '{name}' not found. " f"Available: {self.all_names()}")
        return self._items[name]

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items.values())

    def __str__(self):
        names = ", ".join(self._items.keys())
        return f"Registry({self.registry_type})[{len(self)}]: {names}"

    def __repr__(self):
        return f"Registry(type={self.registry_type!r}, count={len(self)})"