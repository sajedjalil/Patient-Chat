from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, StateGraph, MessagesState, END
from langgraph.prebuilt import tools_condition, ToolNode
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, RemoveMessage
from typing import Literal, List

from home.constants import constants
from home.constants.chat_models import model_claude_3_haiku
from home.constants.constants import summary_prompt, summarize_trigger_count
from home.llm.function_tools.tools import Tools
from home.models.patient import Patient

tool_list = [
    Tools.request_medication_change,
    Tools.make_appointment,
    Tools.request_appointment_change
]


class State(MessagesState):
    summary: str


class LLMGraph:
    def __init__(self):
        self.model = model_claude_3_haiku
        self.model = self.model.bind_tools(tool_list)
        memory = MemorySaver()
        self.graph = self.build_graph().compile(checkpointer=memory)

    def ai_agent(self, state: State):
        sys_msg = SystemMessage(content=constants.llm_prompt_text)
        return {"messages": [self.model.invoke([sys_msg] + state["messages"])]}

    def build_summarize_subgraph(self) -> StateGraph:
        builder = StateGraph(State)
        builder.add_node("summarize_conversation", self.summarize_conversation)
        builder.add_conditional_edges(START, self.if_need_summarization)
        builder.add_edge("summarize_conversation", END)
        return builder

    def build_tool_call_subgraph(self) -> StateGraph:
        builder = StateGraph(State)
        builder.add_node("ai_agent", self.ai_agent)
        builder.add_node("tools", ToolNode(tool_list))

        builder.add_edge(START, "ai_agent")
        builder.add_conditional_edges("ai_agent", tools_condition)
        builder.add_edge("tools", "ai_agent")

        return builder

    def build_graph(self) -> StateGraph:
        builder = StateGraph(State)
        builder.add_node("summarization_subgraph", self.build_summarize_subgraph().compile())
        builder.add_node("tool_call_subgraph", self.build_tool_call_subgraph().compile())

        builder.add_edge(START, "tool_call_subgraph")
        builder.add_edge("tool_call_subgraph", "summarization_subgraph")
        builder.add_edge("summarization_subgraph", END)

        return builder

    def chat_inference(self, user_message: str, history: List[dict], thread_id: str):
        config = {"configurable": {"thread_id": thread_id}}
        messages = self.convert_history_to_messages(history)
        messages.append(HumanMessage(content=user_message))

        result = self.graph.invoke({"messages": messages}, config)
        assistant_response = result['messages'][-1].content

        summary = self.graph.get_state(config).values.get("summary", None)
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
