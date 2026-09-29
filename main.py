# main.py — AgentForge entry point
# Run with: python main.py
# Demonstrates everything: OOP, composition, polymorphism, pipeline,
#                          duck typing, magic methods, mixins

from core.message   import Message
from core.pipeline  import Pipeline
from utils.registry import Registry

from tools.calculator_tool import CalculatorTool
from tools.text_tool       import TextTool
from tools.search_tool     import SearchTool

from agents.chat_agent     import ChatAgent
from agents.analyst_agent  import AnalystAgent
from agents.router_agent   import RouterAgent


def demo_messages():
    print("\n" + "="*60)
    print("DEMO 1 — Message class (dunders + operator overloading)")
    print("="*60)

    m1 = Message.user("Hello, AgentForge!")
    m2 = Message.assistant("Hello! How can I help?")
    m3 = Message.system("You are a helpful assistant.")
    m4 = Message.tool_result("calculator", "42")

    print(f"\nCreated messages:")
    print(f"  {m1}")
    print(f"  {m2}")

    print(f"\nDunder methods:")
    print(f"  len(m1)       = {len(m1)} words")
    print(f"  bool(m1)      = {bool(m1)}")
    print(f"  m1 == m1      = {m1 == m1}")
    print(f"  m1 == m2      = {m1 == m2}")
    print(f"  'Hello' in m1 = {'Hello' in m1}")
    print(f"  'Bye' in m1   = {'Bye' in m1}")

    print(f"\nOperator overloading:")
    combined = m1 + Message.user(" How are you?")
    print(f"  m1 + m2 = {combined}")

    print(f"\nIteration:")
    print(f"  Words in m1: {list(m1)}")

    print(f"\nAlternative constructors (@classmethod):")
    print(f"  {repr(m3)}")
    print(f"  {repr(m4)}")
    print(f"  Total messages created: {Message.total_created()}")

def demo_tools():
    print("\n" + "="*60)
    print("DEMO 2 — Tools (inheritance, __call__, duck typing)")
    print("="*60)

    calc   = CalculatorTool()
    text   = TextTool()
    search = SearchTool()

    print(f"\nTool string representations:")
    print(f"  {calc}")
    print(f"  {text}")
    print(f"  {search}")

    print(f"\nCalling tools (via __call__):")
    print(f"  {calc('calculate 2 + 3 * 4')}")
    print(f"  {calc('what is 100 / 4 + 5')}")
    print(f"  {text('analyse: Python is great and amazing')}")
    print(f"  {text('reverse these words: hello world')}")
    print(f"  {search('tell me about fastapi')}")
    print(f"  {search('what is oop')}")

    print(f"\nTool stats (after calls):")
    for tool in [calc, text, search]:
        print(f"  {tool.name}: called {tool.call_count}x")

    print(f"\nDuck typing — tools stored in Registry:")
    registry = Registry("tools")
    registry.register(calc)
    registry.register(text)
    registry.register(search)
    print(f"  {registry}")
    print(f"  'calculator' in registry: {'calculator' in registry}")
    print(f"  Available: {registry.all_names()}")

def demo_agents():
    print("\n" + "="*60)
    print("DEMO 3 — Agents (composition, polymorphism, mixins)")
    print("="*60)

    # Create tools
    calc   = CalculatorTool()
    text   = TextTool()
    search = SearchTool()

    # Create agents and add tools
    chat_agent = ChatAgent("ChatBot", personality="friendly")
    (chat_agent
     .add_tool(calc)
     .add_tool(text)
     .add_tool(search))
    
    analyst_agent = AnalystAgent("DataBot")

    print(f"\nAgent info:")
    print(f" {chat_agent}")
    print(f" {analyst_agent}")

    print(f"\nAgent magic methods:")
    print(f" len(chat_agent)             = {len(chat_agent)} tools")
    print(f" 'calculator' in chat_agent  = {'calculator' in chat_agent}")
    print(f" 'nonexistent' in chat_agent = {'nonexistent' in chat_agent}")

    print(f"\nChat agent conversations:")
    inputs = [
        "Hello there!",
        "Calculate 150 * 3 + 250",
        "What is the sentiment of: Python is amazing and great!",
        "What is python?",
    ]
    for inp in inputs:
        print(f"\n User : {inp}")
        result = chat_agent(inp) # __call__ on agent
        print(f" Agent : {result}")

    print(f"\nAnalyst agent:")
    data_queries = [
        "Analyse this data: 10 20 30 40 50",
        "Statistics for: 3.5 7.2 1.8 9.1 4.4 6.6",
    ]
    for q in data_queries:
        print(f"\n User : {q}")
        result = analyst_agent(q)
        print(f" Agent :\n{result}")

    print(f"\nMemory state:")
    print(f" {chat_agent.memory}")
    summary = chat_agent.memory.summary()
    for k, v in summary.items():
        print(f" {k}: {v}")
    print(f"\nAll registered agents: {ChatAgent.list_all_agents()}")

def demo_router():
    print("\n" + "="*60)
    print("DEMO 4 — RouterAgent (orchestration, polymorphism, duck typing)")
    print("="*60)

    # Build the full system
    chat_agent = ChatAgent("ChatBot2", personality="concise")
    analyst_agent = AnalystAgent("DataBot2")
    chat_agent.add_tool(SearchTool())

    router = RouterAgent("MainRouter")
    router.register_agent("chat", chat_agent)
    router.register_agent("analyst", analyst_agent)

    print(f"\n{router}")

    tasks = [
        "Hello, how are you?",
        "Analyse these numbers: 5 10 15 20 25",
        "Search for langchain",
        "What is the mean of 4 8 12 16?",
        "Tell me about recursion",
    ]

    print(f"\nRouting {len(tasks)} tasks:")
    for task in tasks:
        print(f"\n Input : {task}")
        result = router.run(task)
        print(f" Output : {result[:80]}...")

    summary = router.routing_summary()
    print(f"\n Routing summary: {summary}")

def demo_pipeline():
    print("\n" + "="*60)
    print("DEMO 5 — Pipeline (composition, __or__, chaining)")
    print("="*60)

    # Custom pipeline stages using duck typing
    class TextNormaliser:
        name = "normaliser"
        def run(self, text):
            return " ".join(text.lower().split())
    
    class KeywordExtractor:
        name = "keyword_extractor"
        _stop = {"the","a","an","is","in","on","at","to","and","of","for"}
        def run(self, text):
            words = [w.strip(".,!?") for w in text.split() if w.lower() not in self._stop and len(w) > 3]
            freq  = {}
            for w in words:
                freq[w] = freq.get(w, 0) + 1
            top3 = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:3]
            return "KEYWORDS: " + ", ".join(f"{w}({c})" for w, c in top3)
        
    class Summariser:
        name = "summariser"
        def run(self, text):
            words = text.split()
            return f"SUMMARY ({len(words)} words): {' '.join(words[:8])}..."

    normaliser = TextNormaliser()
    extractor  = KeywordExtractor()
    summariser = Summariser()
    analyst    = AnalystAgent("PipelineAnalyst")

    # Build pipeline with | operator (operator overloading)
    pipeline = Pipeline("text_pipeline")
    pipeline = pipeline | normaliser | extractor

    print(f"\nPipeline: {pipeline}")
    print(f"Stages : {len(pipeline)}")

    result = pipeline.run(
        "Python is an amazing language. Python makes data engineering "
        "and machine learning easy with Python tools."
    )
    print(f"\nFinal result: {result}")

    print(f"\nPipeline log:")
    for entry in pipeline.log():
        print(f" [{entry['stage']}]")
        print(f"   IN  : {entry['input']}")
        print(f"   OUT : {entry['output']}")

def main():
    print("\n" + "🤖 AgentForge — Mini AI Agent Orchestration Framework".center(60))
    print("OOP Portfolio Project".center(60))
    print("="*60)

    demo_messages()
    demo_tools()
    demo_agents()
    demo_router()
    demo_pipeline()

    print("\n" + "="*60)
    print("OOP CONCEPTS DEMONSTRATED")
    print("="*60)

    concepts = [
        ("Abstract Base Classes", "BaseAgent, BaseTool use ABC + @abstractmethod"),
        ("Inheritance", "ChatAgent, AnalystAgent inherit from BaseAgent"),
        ("Multiple Inheritance", "ChatAgent(LoggingMixin, BaseAgent)"),
        ("Composition", "Agent HAS-A Memory, HAS-A Tools dict"),
        ("Encapsulation", "Memory hides __messages with properties"),
        ("Polymorphism", "Router calls agent.run() — different result per type"),
        ("Magic Methods", "Message: __add__ __contains__ __iter__ __len__"),
        ("Operator Overloading", "Pipeline: pipeline | agent adds a stage"),
        ("Class Methods", "Message.user(), Message.from_dict()"),
        ("Static Methods", "BaseTool.validate_input(), SearchTool.available_topics()"),
        ("Properties", "Memory.max_size with getter/setter"),
        ("Duck Typing", "Any object with .run() works as agent or pipeline stage"),
        ("Mixin Pattern", "LoggingMixin added to agents via multiple inheritance"),
        ("__call__", "tool('input') and agent('input') both work directly"),
        ("Chaining", "agent.add_tool(a).add_tool(b) via return self"),
    ]
    for concept, example in concepts:
        print(f"  ✅ {concept:<25}: {example}")
    
if __name__ == "__main__":
    main()