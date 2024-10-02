from langchain.chains import GraphCypherQAChain
from langchain_community.chains.graph_qa.prompts import CYPHER_GENERATION_PROMPT
from langchain_community.graphs import Neo4jGraph
from langchain_core.documents import Document
from langchain_experimental.graph_transformers import LLMGraphTransformer

from home.constants.chat_models import *
from home.constants.constants import rag_prompt_text
from home.models.patient import Patient


class RAGGraph:
    """
    A class to manage and interact with a knowledge graph using RAG (Retrieval-Augmented Generation) approach.

    Attributes:
    - patient: The first patient object from the database.
    - graph_query_model: The language model used for querying the knowledge graph.
    - llm_graph_transformer: The transformer to convert text into graph documents.
    - neo4j_graph: The Neo4j graph database instance.

    Methods:
    - rag_store_and_query(user_message): Stores the user message extracted knowledge to Neo4J graph and queries the graph.
    - __query_knowledge_graph(user_message): Queries the knowledge graph using the user message.
    - __save_to_neo4j(user_message): Saves the user message extracted knowledge to Neo4J graph.
    - fetch_user_fullname(): Fetches the full name of the first patient from the database.
    """

    def __init__(self):
        self.patient = Patient.objects.first()
        self.graph_query_model = model_claude_3_5_sonnet # model for query
        self.llm_graph_transformer = LLMGraphTransformer(llm=model_claude_3_5_sonnet) # Model for graph data entry
        self.neo4j_graph = Neo4jGraph()

    def rag_store_and_query(self, user_message) -> str:
        """
        Stores the user message extracted knowledge to Neo4J graph and queries the graph for medical insights.

        Parameters:
        - user_message (str): The user message to be stored and queried.

        Returns:
        - str: The response from the knowledge graph query.
        """
        self.__save_to_neo4j(user_message)  # Stores the user message extracted knowledge to Neo4J graph
        # Queries user related data from Neo4J graph for medical insights
        response = self.__query_knowledge_graph(user_message)
        return response

    def __query_knowledge_graph(self, user_message):
        """
        Queries the knowledge graph using the user message.

        Parameters:
        - user_message (str): The user message to be used for querying.

        Returns:
        - str: The response from the knowledge graph query.
        """
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
        """
        Saves the user message extracted knowledge to Neo4J graph.

        Parameters:
        - user_message (str): The user message to be stored in the graph.
        """
        context_prompt = ('The following message is from a patient having the following information : ' +
                          self.patient.__str__())
        documents = [Document(page_content=context_prompt + user_message)]
        graph_documents = self.llm_graph_transformer.convert_to_graph_documents(documents)
        self.neo4j_graph.add_graph_documents(graph_documents)
        self.neo4j_graph.refresh_schema()

    @staticmethod
    def fetch_user_fullname():
        """
        Fetches the full name of the first patient from the database.

        Returns:
        - str: The full name of the first patient.
        """
        patient = Patient.objects.first()
        return patient.last_name + " " + patient.last_name
