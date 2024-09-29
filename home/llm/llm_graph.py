from langchain_anthropic import ChatAnthropic
from langgraph.graph import START, StateGraph, MessagesState, END
from langgraph.prebuilt import tools_condition, ToolNode
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, RemoveMessage
from typing import Literal, List
from django.utils import timezone
import logging

from home.db_schema.chat_history import ChatHistory
from home.llm import prompt
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
        self.graph = self.build_graph().compile()

    def assistant(self, state: State):
        sys_msg = SystemMessage(content=prompt.prompt_text)
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
        builder.add_node("assistant", self.assistant)
        builder.add_node("tools", ToolNode(self.tool_list))
        builder.add_node("summarization_subgraph", self.build_summarize_subgraph().compile())

        builder.add_edge(START, "summarization_subgraph")
        builder.add_edge("summarization_subgraph", "assistant")
        builder.add_conditional_edges("assistant", tools_condition)
        builder.add_edge("tools", "assistant")

        return builder

    def inference(self, user_message: str, history: List[dict]) -> str:
        messages = self.convert_history_to_messages(history)
        messages.append(HumanMessage(content=user_message))

        result = self.graph.invoke({"messages": messages})
        logger.debug(result)

        assistant_response = result['messages'][-1].content

        return assistant_response

    def summarize_conversation(self, state: State):
        summary = state.get("summary", "")
        summary_message = self.get_summary_message(summary)

        messages = state["messages"] + [HumanMessage(content=summary_message)]
        response = self.model.invoke(messages)

        delete_messages = [RemoveMessage(id=m.id) for m in state["messages"][:-2]]
        return {"summary": response.content, "messages": delete_messages}

    @staticmethod
    def if_need_summarization(state: State) -> Literal["summarize_conversation", "__end__"]:
        if len(state["messages"]) >= 6:
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

    @staticmethod
    def get_summary_message(summary: str) -> str:
        if summary:
            return f"This is summary of the conversation to date: {summary}\n\n" \
                   "Extend the summary by taking into account the new messages above:"
        return "Create a summary of the conversation above:"

