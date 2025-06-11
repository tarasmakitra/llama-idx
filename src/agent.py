from llama_index.core.agent import ReActAgent
from llama_index.core.memory import Memory
from llama_index.tools.yahoo_finance import YahooFinanceToolSpec

from models import llm
from knowledge_tool import GeneralKnowledgeTool
from query_tool import create_query_engine_tool


def create_react_agent(file_name: str) -> ReActAgent:
    yahoo_tools = YahooFinanceToolSpec()
    general_knowledge_tools = GeneralKnowledgeTool(llm=llm)
    query_engine_tool = create_query_engine_tool(file_name=file_name)

    tools = [
        query_engine_tool,
        *yahoo_tools.to_tool_list(),
        *general_knowledge_tools.to_tool_list(),
    ]

    memory = Memory(token_limit=10000)

    return ReActAgent(llm=llm, tools=tools, verbose=True, memory=memory)
