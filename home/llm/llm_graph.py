from langchain_anthropic import ChatAnthropic
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, StateGraph, MessagesState, END
from langgraph.prebuilt import tools_condition, ToolNode
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, RemoveMessage
from typing import Literal, List
import logging

from home.llm import constants
from home.llm.constants import summary_prompt, summarize_trigger_count
from home.llm.tools import Tools

logger = logging.getLogger(__name__)


class State(MessagesState):
    summary: str


class LLMGraph:
    def __init__(self):
        self.model = ChatAnthropic(model="claude-3-haiku-20240307")
        self.tool_list = [
            Tools.request_medication_change,
            Tools.make_appointment,
            Tools.request_appointment_change
        ]
        memory = MemorySaver()
        self.graph = self.build_graph().compile(checkpointer=memory)

    def ai_agent(self, state: State):
        sys_msg = SystemMessage(content=constants.prompt_text)
        model_with_tools = self.model.bind_tools(self.tool_list)
        return {"messages": [model_with_tools.invoke([sys_msg] + state["messages"])]}

    def build_summarize_subgraph(self) -> StateGraph:
        builder = StateGraph(State)
        builder.add_node("summarize_conversation", self.summarize_conversation)
        builder.add_conditional_edges(START, self.if_need_summarization)
        builder.add_edge("summarize_conversation", END)
        return builder

    def build_graph(self) -> StateGraph:
        builder = StateGraph(State)
        builder.add_node("ai_agent", self.ai_agent)
        builder.add_node("tools", ToolNode(self.tool_list))
        builder.add_node("summarization_subgraph", self.build_summarize_subgraph().compile())

        builder.add_edge(START, "ai_agent")
        builder.add_edge("ai_agent", "summarization_subgraph")
        builder.add_conditional_edges("ai_agent", tools_condition)
        builder.add_edge("tools", "ai_agent")
        builder.add_edge("summarization_subgraph", END)

        return builder

    def inference(self, user_message: str, history: List[dict], thread_id: str):
        config = {"configurable": {"thread_id": thread_id}}
        messages = self.convert_history_to_messages(history)
        messages.append(HumanMessage(content=user_message))

        result = self.graph.invoke({"messages": messages}, config)
        assistant_response = result['messages'][-1].content

        summary = self.graph.get_state(config).values.get("summary", "")
        return assistant_response, summary

    def summarize_conversation(self, state: State):
        messages = state["messages"] + [HumanMessage(content=summary_prompt)]
        response = self.model.invoke(messages)

        delete_messages = [RemoveMessage(id=m.id) for m in state["messages"][:-2]]
        return {"summary": response.content, "messages": delete_messages}

    @staticmethod
    def if_need_summarization(state: State) -> Literal["summarize_conversation", "__end__"]:
        if len(state["messages"]) >= summarize_trigger_count:
            return "summarize_conversation"
        else:
            return "__end__"

    @staticmethod
    def convert_history_to_messages(history: List[dict]) -> List[HumanMessage | AIMessage]:
        return [
            HumanMessage(content=msg['content']) if msg['role'] == 'user'
            else AIMessage(content=msg['content'])
            for msg in history
        ]
