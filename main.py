from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from agent import Agent
from langgraph.checkpoint.sqlite import SqliteSaver

memory = SqliteSaver.from_conn_string(":memory:")

_ = load_dotenv()

tool = TavilySearchResults(max_results=2)

prompt = """You are a smart research assistant. Use the search engine to look up information. \
You are allowed to make multiple calls (either together or in sequence). \
Only look up information when you are sure of what you want. \
If you need to look up some information before asking a follow up question, you are allowed to do that!
"""
model = ChatOpenAI(model="gpt-4o")
abot = Agent(model, [tool], system=prompt, checkpointer=memory)

messages = [HumanMessage(content="Where the weather is warmer in Kyiv or Kharkiv?")]
thread = {"configurable": {"thread_id": "1"}}

for event in abot.graph.stream({"messages": messages}, thread):
    for v in event.values():
        print(v['messages'][0].content)

