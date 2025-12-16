from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langsmith import traceable
from langchain_core.tracers.langchain import LangChainTracer

# Import from our new package
from gateagent import InteractionTracer, Client

client = Client(api_key="******")

# --------------------
# Tools
# --------------------

callbacks = [
    InteractionTracer(
        client = client,
        project_name="math-agent-playground",
        default_metadata={
            "agent": "math-agent-v1",
            "environment": "local",
        },
    ),
    # If using LangSmith/Langfuses as well
    LangChainTracer(project_name="math-agent-playground"),
]

@tool
def add_numbers(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


@tool
def multiply_numbers(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


tools = [add_numbers, multiply_numbers]
tool_map = {t.name: t for t in tools}


# --------------------
# LLM with tools bound
# --------------------

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
).bind_tools(tools)


# --------------------
# Prompt
# --------------------

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a math assistant. Always use tools to compute results."),
        ("human", "{input}"),
    ]
)


# --------------------
# Runnable chain
# --------------------

chain = prompt | llm


# --------------------
# Tool execution (explicit, traceable)
# --------------------

@traceable(run_type="tool")
def execute_tool(tool_name: str, args: dict, config: dict = None):
    return tool_map[tool_name].invoke(args, config=config)


# --------------------
# Runner
# --------------------

@traceable(
    run_type="chain",
    name="math-agent",
)
def run(input_text: str):
    response = chain.invoke(
        {"input": input_text},
        config={
            "callbacks": callbacks,
            "run_name": "math-agent-llm",
            "tags": ["math", "tool-calling"],
            "metadata": {
                "agent": "math-agent-v1",
                "environment": "local",
            },
        },
    )

    if response.tool_calls:
        tool_call = response.tool_calls[0]
        return execute_tool(
            tool_call["name"],
            tool_call["args"],
            config={"callbacks": callbacks}
        )

    return response.content 


# --------------------
# Main
# --------------------

if __name__ == "__main__":
    import os
    if not os.environ.get("OPENAI_API_KEY"):
        print("Set OPENAI_API_KEY to run this example.")
    else:
        print(run("Add 4 and 50"))