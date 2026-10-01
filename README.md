# AgentForge

A lightweight framework for building, registering, and orchestrating AI agents with tools, memory, and pipelines — built entirely with Python OOP from scratch.

AgentForge is a compact, educational, and portfolio-oriented Python project designed to demonstrate core object-oriented programming principles while modeling a simple AI agent framework. The project focuses on clear abstractions, practical composition, and extensibility without depending on external AI services or heavy third-party libraries.

## Why AgentForge?

This project was created to showcase how a minimal agent system can be implemented using pure Python and OOP concepts:

- Agents as reusable objects with clear responsibilities
- Tools as modular capabilities attached to agents
- Memory for conversation history and state tracking
- Routing and orchestration for multi-agent workflows
- Pipeline composition for staged data processing
- Logging and registry patterns for visibility and organization

## Key Features

- Agent abstraction with polymorphic `run()` behavior
- Tool inheritance and callable execution
- Message model with operator overloading and role-aware metadata
- Memory management with configurable limits and summary statistics
- Router-based delegation for task distribution across specialized agents
- Pipeline chaining for sequential transformations
- Registry support for tracking agents and tools
- Logging mixin for structured debug, info, warning, and error output

## Project Structure

```text
AgentForge/
├── agents/
│   ├── analyst_agent.py
│   ├── chat_agent.py
│   └── router_agent.py
├── core/
│   ├── base_agent.py
│   ├── base_tool.py
│   ├── memory.py
│   ├── message.py
│   └── pipeline.py
├── tools/
│   ├── calculator_tool.py
│   ├── search_tool.py
│   └── text_tool.py
├── utils/
│   ├── logger.py
│   └── registry.py
├── .gitignore
├── main.py
├── Output.txt
├── requirements.txt
├── README.md
└── .venv/    # local environment if created
```

## Architectural Overview

### Core Components

- `BaseAgent`: Abstract base class for all agents
- `BaseTool`: Abstract base class for all tools
- `Message`: Encapsulates user/assistant/system/tool-result messages with rich behavior
- `Memory`: Stores agent conversation history and enforces max-length limits
- `Pipeline`: Enables chaining multiple stages using operator-overloaded composition

### Agent Types

- `ChatAgent`: Handles general conversation and tool-assisted responses
- `AnalystAgent`: Focuses on analysis-oriented tasks and quantitative reasoning
- `RouterAgent`: Decides which specialized agent should handle a given task

### Tool Capabilities

- `CalculatorTool`: Evaluates mathematical expressions from natural-language input
- `TextTool`: Performs text analysis, reversal, sentiment scoring, and keywords
- `SearchTool`: Returns mock knowledge-base answers for common topics

## Object-Oriented Concepts Demonstrated

AgentForge intentionally emphasizes standard Python OOP patterns, including:

- Inheritance
- Abstract base classes
- Composition
- Polymorphism
- Encapsulation
- Multiple inheritance with mixins
- Operator overloading
- Duck typing
- Class methods and static methods
- Property-based accessors

## Getting Started

### Prerequisites

- Python 3.8+
- Standard library only

### Installation

```bash
git clone https://github.com/yasaswini250505/AgentForge.git
cd AgentForge
python -m venv .venv
source .venv/bin/activate    # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Run the Demo

```bash
python main.py
```

The project’s entry point demonstrates core behavior across message handling, tool usage, agent interaction, routing logic, and pipeline execution.

## Example Usage

```python
from agents.chat_agent import ChatAgent
from tools.calculator_tool import CalculatorTool
from agents.router_agent import RouterAgent

chat_agent = ChatAgent("ChatBot", personality="friendly")
chat_agent.add_tool(CalculatorTool())

response = chat_agent("Calculate 12 * 8")
print(response)

router = RouterAgent("MainRouter")
router.register_agent("chat", chat_agent)
print(router.run("Hello there!"))
```

## Example Behaviors

- Friendly greeting support
- Question answering with contextual memory
- Mathematical calculation using tools
- Text sentiment and language analysis
- Search-like retrieval from an internal knowledge base
- Task routing based on keyword matching
- Pipeline stages for sequential transformation

## Design Philosophy

AgentForge is intentionally simple and teachable. Each major concept is modeled as a small, understandable class or function, which makes the project suitable for:

- learning Python OOP through implementation
- prototyping lightweight agent workflows
- demonstrating how multi-agent systems can be structured
- building a foundation for more advanced AI framework experimentation

## Notes

This project is intentionally self-contained and does not rely on external LLM APIs or cloud-based services. It is a conceptual framework for understanding how AI agent systems can be modeled using clean Python object design patterns.

## License

This repository does not currently include a license file. If you intend to distribute or reuse it publicly, consider adding an appropriate open-source license.

## Contributing

Contributions are welcome. Possible areas of improvement include:

- adding more specialized agents
- expanding tool capabilities
- improving routing logic
- refactoring for cleaner interfaces
- adding examples and documentation improvements

## Repository

https://github.com/yasaswini250505/AgentForge
