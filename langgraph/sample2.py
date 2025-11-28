from langgraph.prebuilt import create_react_agent
from gateagent import Client        ## Change1: Import GateAgent Client
from langchain.callbacks import LangChainTracer  # or use Langfuse CallbackHandler

client = Client(api_key="YOUR_KEY") ## Change2: Replace with your API key
tracer = LangChainTracer(client=client, project_name="my-audit-project")

# create a simple agent via LangGraph
agent = create_react_agent(
    model="openai:chatgpt-3.5-turbo",
    tools=[ ... ],         # your tool wrappers (e.g. Confluence API, Sheets API)  
    prompt="You are a helpful assistant"
)

# run the agent, passing tracer in callbacks
result = agent.invoke(
    {"messages": [{"role": "user", "content": "Do X"}]},
    config={"callbacks": [tracer]}
)
