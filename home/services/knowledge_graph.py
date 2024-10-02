from langchain_community.chains.graph_qa.prompts import CYPHER_GENERATION_PROMPT
from langchain_community.graphs import Neo4jGraph
from langchain_core.documents import Document
from langchain.chains import GraphCypherQAChain
from langchain_experimental.graph_transformers import LLMGraphTransformer

from home.constants.chat_models import *


class KnowledgeGraph:

    def __init__(self):
        self.graph = Neo4jGraph()
        self.llm_transformer = LLMGraphTransformer(llm=model_claude_3_5_sonnet)
        self.cypher_llm = model_claude_3_haiku
        self.qa_llm = model_claude_3_5_sonnet

    def query_graph(self, text) -> str:
        chain = GraphCypherQAChain.from_llm(graph=self.graph, cypher_llm=self.cypher_llm, qa_llm=self.qa_llm,
                                            verbose=False, validate_cypher=True, allow_dangerous_requests=True, top_k=10,
                                            return_intermediate_steps=False, cypher_prompt=CYPHER_GENERATION_PROMPT)
        response = chain.invoke({"query": text})
        return response['result']

    def add_knowledge_to_graph(self, text):
        documents = [Document(page_content=text)]
        graph_documents = self.llm_transformer.convert_to_graph_documents(documents)
        self.graph.add_graph_documents(graph_documents)

        self.graph.refresh_schema()  # Refreshes the Neo4j graph schema information.
