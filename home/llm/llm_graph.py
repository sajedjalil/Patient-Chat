from langchain_anthropic import ChatAnthropic
from langgraph.graph import START, StateGraph, MessagesState
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import tools_condition, ToolNode
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, RemoveMessage

import logging

from home.db_schema.chat_history import ChatHistory
from home.llm import prompt
from home.llm.tools import Tools
from django.utils import timezone

logger = logging.getLogger(__name__)


class State(MessagesState):
    summary: str


class LLMGraph:
    def __init__(self):
        self.model = ChatAnthropic(model="claude-3-haiku-20240307")
        self.tool_list = [Tools.request_medication_change, Tools.make_appointment, Tools.request_appointment_change]
        self.graph = self.build_graph()

    def build_graph(self) -> CompiledStateGraph:
        builder = StateGraph(State)
        builder.add_node("assistant", self.assistant)
        builder.add_node("tools", ToolNode(self.tool_list))

        builder.add_edge(START, "assistant")
        builder.add_conditional_edges("assistant", tools_condition)
        builder.add_edge("tools", "assistant")

        return builder.compile()

    def assistant(self, state: State):
        # Prompt message
        sys_msg = SystemMessage(content=prompt.prompt_text)
        model_with_tools = self.model.bind_tools(self.tool_list)
        return {"messages": [model_with_tools.invoke([sys_msg] + state["messages"])]}

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

        assistant_response = result['messages'][-1].content

        # Create user message entry
        ChatHistory.objects.create(
            patient_id=1,
            chat_id=1,
            is_user=True,
            text=user_message,
            timestamp=timezone.now()
        )

        # Create assistant message entry
        ChatHistory.objects.create(
            patient_id=1,
            chat_id=1,
            is_user=False,
            text=assistant_response,
            timestamp=timezone.now()
        )

        return assistant_response
