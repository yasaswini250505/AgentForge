# utils/logger.py
# LoggingMixin — adds structured logging to any class.
# Demonstrates: mixin pattern (multiple inheritance), class variables,
#               @staticmethod, @classmethod


class LoggingMixin:
    """
    Mixin that adds logging to any class.
    Usage: class MyAgent(LoggingMixin, BaseAgent): ...
    No __init__ — mixins should not conflict with other constructors.
    """

    _all_logs = [] # class-level — shared across ALL logged objects
    LOG_LEVELS = {"DEBUG":0, "INFO":1, "WARN":2, "ERROR":3}

    def _log(self, level, message, data=None):
        """Internal log method — always available via mixin."""
        level = level.upper()
        min_level = getattr(self, "_log_level", 0)

        if self.LOG_LEVELS.get(level, 0) < min_level:
            return
        
        entry = {
        "source" : self.__class__.__name__,
        "level" : level,
        "message": message,
        "data" : data,
        }
        LoggingMixin._all_logs.append(entry)

        icons = {"DEBUG":"🔍","INFO":"ℹ ","WARN":"⚠ ","ERROR":"❌"}
        icon = icons.get(level, "•")
        data_str = f" | {data}" if data else ""
        print(f" {icon} [{self.__class__.__name__}] {message}{data_str}")

    def _debug(self, msg, data=None): self._log("DEBUG", msg, data)
    def _info(self, msg, data=None): self._log("INFO", msg, data)
    def _warn(self, msg, data=None): self._log("WARN", msg, data)
    def _error(self, msg, data=None): self._log("ERROR", msg, data)

    @classmethod
    def all_logs(cls):
        return list(cls._all_logs)

    @classmethod
    def logs_by_level(cls, level):
        return [l for l in cls._all_logs if l["level"] == level.upper()]
    
    @classmethod
    def clear_logs(cls):
        cls._all_logs = []

    @staticmethod
    def format_log(entry):
        return f"[{entry['level']}] {entry['source']}: {entry['message']}"