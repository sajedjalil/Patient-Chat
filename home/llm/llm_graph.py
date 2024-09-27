from langgraph.graph import START, StateGraph, MessagesState
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import tools_condition, ToolNode
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

import logging
from home.llm.llm import LLM

logger = logging.getLogger(__name__)


class LLMGraph:
    prompt_text = '''You are a helpful AI medical assistant namely Patient Chat and are developed by a software 
    engineer named Sajed. 
    You should only respond to health-related topics such as: 
    - General human health and lifestyle inquiries.
    - Questions about men, women and children health
    - Questions about the patient's medical condition, medication regimen, diet, etc. 
    - Various requests from the patient to their doctor such as make appointments, modify appointments and medication changes. 
    You should filter out and ignore any unrelated, overly sensitive, or controversial topics.'''

    def __init__(self):
        self.llm = LLM()
        self.graph = self.build_graph()

    def assistant(self, state: MessagesState):
        # Prompt message
        sys_msg = SystemMessage(content=self.prompt_text)
        return {"messages": [self.llm.llm_with_tools.invoke([sys_msg] + state["messages"])]}

    def build_graph(self) -> CompiledStateGraph:
        builder = StateGraph(MessagesState)
        builder.add_node("assistant", self.assistant)
        builder.add_node("tools", ToolNode(self.llm.tools))

        builder.add_edge(START, "assistant")
        builder.add_conditional_edges("assistant", tools_condition)
        builder.add_edge("tools", "assistant")

        return builder.compile()

    def inference(self, user_message, history) -> str:
        messages = []
        for msg in history:
            if msg['role'] == 'user':
                messages.append(HumanMessage(content=msg['content']))
            elif msg['role'] == 'assistant':
                messages.append(AIMessage(content=msg['content']))

        messages.append(HumanMessage(content=user_message))

        result = self.graph.invoke({"messages": messages})
        logger.debug(result)

        return result['messages'][-1].content
