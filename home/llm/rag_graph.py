from langgraph.graph import START, StateGraph, MessagesState, END
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.checkpoint.memory import MemorySaver
from langchain_community.chains.graph_qa.prompts import CYPHER_GENERATION_PROMPT
from langchain.chains import GraphCypherQAChain
from langchain_community.graphs import Neo4jGraph

from home.constants.chat_models import *
from home.models.patient import Patient


def fetch_user_info():
    patient = Patient.objects.first()
    return patient.last_name + " " + patient.last_name


class RAGGraph:
    def __init__(self):
        self.model = model_claude_3_5_sonnet
        memory = MemorySaver()
        self.graph = self.build_graph().compile(checkpointer=memory)

    def query_knowledge_graph(self, state: MessagesState):
        graph = Neo4jGraph()
        chain = GraphCypherQAChain.from_llm(graph=graph, llm=self.model, verbose=True, validate_cypher=True,
                                            allow_dangerous_requests=True, top_k=5,
                                            cypher_prompt=CYPHER_GENERATION_PROMPT)
        response = chain.invoke({"query": state['messages']})

        return {'messages': [AIMessage(response['result'])]}

    def build_graph(self) -> StateGraph:
        builder = StateGraph(MessagesState)
        builder.add_node("query_knowledge_graph", self.query_knowledge_graph)

        builder.add_edge(START, "query_knowledge_graph")
        builder.add_edge("query_knowledge_graph", END)

        return builder

    def rag_inference(self, input_text: str, thread_id: str):
        config = {"configurable": {"thread_id": thread_id}}
        messages = [HumanMessage(content=
                                 "Here is a summary chat information of " + fetch_user_info() + ":\n"
                                 + input_text +
                                 "\nGet Medical information analysis of the following person.")]

        result = self.graph.invoke({"messages": messages}, config)
        assistant_response = result['messages'][-1].content

        return assistant_response
