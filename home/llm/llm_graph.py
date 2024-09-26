from langgraph.graph import START, StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import tools_condition, ToolNode

from langgraph.graph import MessagesState
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from home.llm.llm import LLM


class LLMGraph:
    prompt_text = '''
        You are a helpful AI medical assistant. You should only respond to health-related topics such as:
        - General human health and lifestyle inquiries.
        - Questions about the patient’s medical condition, medication regimen, diet, etc.
        - Various requests from the patient to their doctor such as make appointments, modify appointments and medication changes.
        You should filter out and ignore any unrelated, sensitive, or controversial topics.
    '''

    def __init__(self):
        self.llm = LLM()
        self.graph = self.build_graph()


    def assistant(self, state: MessagesState):
        # Prompt message
        sys_msg = SystemMessage(content=self.prompt_text)
        return {"messages": [self.llm.llm_with_tools.invoke([sys_msg] + state["messages"])]}

    def build_graph(self) -> CompiledStateGraph:
        builder = StateGraph(MessagesState)

        # Define nodes: these do the work
        builder.add_node("assistant", self.assistant)
        builder.add_node("tools", ToolNode(self.llm.tools))

        # Define edges: these determine how the control flow moves
        builder.add_edge(START, "assistant")
        builder.add_conditional_edges(
            "assistant",
            # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
            # If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END
            tools_condition,
        )
        builder.add_edge("tools", "assistant")

        return builder.compile()

    def inference(self, user_message) -> str:
        messages = [HumanMessage(content=user_message)]
        messages = self.graph.invoke({"messages": messages})
        for m in messages['messages']:
            m.pretty_print()

        print()
        return messages['messages'][-1].content
