from langchain.chains import GraphCypherQAChain
from langchain_community.chains.graph_qa.prompts import CYPHER_GENERATION_PROMPT
from langchain_community.graphs import Neo4jGraph
from langchain_core.documents import Document
from langchain_core.messages import AIMessage
from langchain_experimental.graph_transformers import LLMGraphTransformer

from home.constants.chat_models import *
from home.constants.constants import rag_prompt_text
from home.models.patient import Patient


def fetch_user_info():
    patient = Patient.objects.first()
    return patient.last_name + " " + patient.last_name


class RAGGraph:
    def __init__(self):
        self.patient = Patient.objects.first()
        self.graph_query_model = model_claude_3_5_sonnet
        self.llm_graph_transformer = LLMGraphTransformer(llm=model_claude_3_5_sonnet)
        self.neo4j_graph = Neo4jGraph()

    def rag_store_and_query(self, user_message) -> str:
        self.__save_to_neo4j(user_message)  # Stores the user message extracted knowledge to Neo4J graph
        return self.__query_knowledge_graph(user_message)

    def __query_knowledge_graph(self, user_message):
        chain = GraphCypherQAChain.from_llm(graph=self.neo4j_graph, llm=self.graph_query_model, verbose=False,
                                            validate_cypher=True, allow_dangerous_requests=True, top_k=5,
                                            cypher_prompt=CYPHER_GENERATION_PROMPT)

        response = chain.invoke(rag_prompt_text +
                                "Current patient name is: " + self.patient.first_name + " " + self.patient.last_name +
                                "Fetch all related data of the patient and make an analysis. Continue with what you "
                                "have.",
                                return_only_outputs=True)['result']
        return response

    def __save_to_neo4j(self, user_message):
        context_prompt = ('The following message is from a patient having the following information : ' +
                          self.patient.__str__())
        documents = [Document(page_content=context_prompt + user_message)]
        graph_documents = self.llm_graph_transformer.convert_to_graph_documents(documents)
        self.neo4j_graph.add_graph_documents(graph_documents)
        self.neo4j_graph.refresh_schema()
