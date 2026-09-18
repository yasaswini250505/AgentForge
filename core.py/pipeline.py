# core/pipeline.py
# Pipeline  — chains multiple agents in sequence.
# Demonstrates: composition, __or__ (pipe operator), __iter__,
#               __len__, __str__, polymorphism

from operator import index
from tkinter.font import names

from distro import name

from os import name

from core.message import Message


class Pipeline:
    """
    Chains agents in sequence. Output of one becomes input to the next.
    
    Usage:
        pipeline = Pipeline("my-pipeline")
        pipeline.add(agent1).add(agent2).add(agent3)

        # Or use the pipe operator
        pipeline = agent1 | agent2 | agent3
        result = pipeline.run("Starting input")
    """

    def __init__(self, name="pipeline"):
        self.name =  name
        self._stages = [] # list of agents (composition)
        self._log = [] # execution log

    def add(self, agent):
        """Add an agent to the pipeline. Returns self for chaining."""
        if not (hasattr(agent, "run") and callable(agent.run)):
            raise TypeError(f"Pipeline stage must have a callable run() method")
        self._stages.append(agent)
        return self
    
    def run(self, initial_input):
        """
        Run all stages in sequence.
        Output of stage n becomes input to stage n+1.
        """
        self._log = []
        current = initial_input

        print(f"\n Pipeline '{self.name}' starting with {len(self)} stages")
        print(f" Input: {current!r}")
        print(f" {'─'*50}")

        for i, agent in enumerate(self._stages, 1):
        # Duck typing — any object with .run() works as a stage
            stage_name = getattr(agent, "name", f"stage_{i}")
            result = agent.run(current)
            self._log.append({
                "stage" : stage_name,
                "input" : current[:60],
                "output": result[:60],
            })
            print(f" Stage {i} [{stage_name}]:")
            print(f" IN → {current[:55]}")
            print(f" OUT → {result[:55]}")
            current = result
        print(f" {'─'*50}")
        return current
        
    def log(self):
        return self._log

    # ── Operator overloading ──────────────────────────────────────────
    def __or__(self, other):
        """pipeline | agent → adds agent to pipeline and returns self."""
        self.add(other)
        return self
    
    def __ror__(self, other):
        """agent | pipeline → adds agent to FRONT of pipeline."""
        self._stages.insert(0, other)
        return self
    
    # ── Dunder methods ────────────────────────────────────────────────
    def __len__(self):
        return len(self._stages)
    
    def __iter__(self):
        return iter(self._stages)
    
    def __getitem__(self, index):
        return self._stages[index]
    
    def __str__(self):
        names = " → ".join(
            getattr(s, "name", s.__class__.__name__)
            for s in self._stages
        )
        return f"Pipeline('{self.name}': {names})"
    
    def __repr__(self):
        return f"Pipeline(name={self.name!r}, stages={len(self)})"