# agents/router_agent.py
# Router agent — receives a task and delegates to the right agent.
# Demonstrates: composition (holds a dict of agents), polymorphism,
#               duck typing (any agent with .run() works), class methods

from core.base_agent import BaseAgent
from utils.logger import LoggingMixin


class RouterAgent(LoggingMixin, BaseAgent):
    """
    Orchestrator agent. Analyses the user input and routes it to
    the best specialised agent. Demonstrates polymorphism + duck typing.
    """
    
    # Routing keywords — maps keywords to agent types
    _ROUTING_TABLE = {
        "chat" : ["hello","hi","hey","chat","talk","tell me","explain"],
        "analyst" : ["analyse","analyze","statistics","average","mean","data",
        "numbers","calculate statistics"],
        "search" : ["search","find","what is","who is","define","lookup"],
    }

    def __init__(self, name, model="gpt-4o"):
        super().__init__(name, model)
        self._sub_agents = {} # {agent_type: agent_instance}
        self._route_log = []
        self._info(f"RouterAgent '{name}' ready")

    @property
    def agent_type(self):
        return "router"

    def register_agent(self, agent_type, agent):
        """
        Register a sub-agent for a given type.
        Duck typing — any object with .run() works.
        """
        if not hasattr(agent, "run"):
            raise TypeError("Registered agent must have a run() method")
        self._sub_agents[agent_type] = agent
        self._info(f"Registered agent", {"type": agent_type})
        return self

    def run(self, user_input):
        """Route input to the best available agent."""
        agent_type = self._determine_route(user_input)
        self._route_log.append({"input" : user_input[:40], "routed_to" : agent_type})
        if agent_type not in self._sub_agents:
            self._warn(f"No agent for type '{agent_type}'")
            # Fallback: try any available agent
            if self._sub_agents:
                agent_type = list(self._sub_agents.keys())[0]
                self._info(f"Falling back to '{agent_type}'")
            else:
                return f"No agents registered. Please register agents first."
            
        selected_agent = self._sub_agents[agent_type]
        self._info(f"Routing to agent", {
            "type": agent_type,
            "agent": getattr(selected_agent, "name", "unknown")
        })

        # Polymorphism: run() works differently per agent type
        return selected_agent.run(user_input)
    
    def routing_summary(self):
        """Summary of all routing decisions made."""
        counts = {}
        for entry in self._route_log:
            t = entry["routed_to"]
            counts[t] = counts.get(t, 0) + 1
        return {
            "total_routed"     : len(self._route_log),
            "routes"           : counts,
            "registered_types" : list(self._sub_agents.keys()),
        }

    # ── Private routing logic ──────────────────────────────────────────
    def _determine_route(self, text):
        """Score each agent type and return the best match."""
        text_lower = text.lower()
        scores = {t: 0 for t in self._ROUTING_TABLE}

        for agent_type, keywords in self._ROUTING_TABLE.items():
            for kw in keywords:
                if kw in text_lower:
                    scores[agent_type] += 1
        # Check for numbers → likely analyst task
        has_numbers = any(c.isdigit() for c in text)
        if has_numbers and "statistics" in text_lower:
            scores["analyst"] += 3

        best = max(scores, key=scores.get)
        return best if scores[best] > 0 else "chat"
    
    def __str__(self):
        agents = list(self._sub_agents.keys())
        return f"RouterAgent({self.name!r}, routes={agents})"