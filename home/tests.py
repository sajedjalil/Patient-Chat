import uuid

from django.test import TestCase

from home.constants.constants import history_two_turns, history_one_turn, knowledge_text
from home.llm.llm_graph import LLMGraph
from home.llm.rag_graph import RAGGraph
from home.services.knowledge_graph import KnowledgeGraph


class LLMTestCase(TestCase):
    def setUp(self):
        self.llm_graph = LLMGraph()

    def test_llm_name(self):
        user_message = "Hi, my name is Sajed. What's your name?"
        ai_response, summary = self.llm_graph.chat_inference(user_message, [], "test_" + str(uuid.uuid4()))
        self.assertTrue(ai_response.__contains__("Patient Chat"))

    def test_llm_remembers_context_history(self):
        history = history_one_turn
        user_message = "Now tell me what's my name?"
        ai_response, summary = self.llm_graph.chat_inference(user_message, history, "test_" + str(uuid.uuid4()))
        self.assertTrue(ai_response.__contains__("Sajed"))

    def test_llm_tool_call(self):
        history = []
        user_message = "Change my medicine lorazepam."
        ai_response, summary = self.llm_graph.chat_inference(user_message, history, "test_" + str(uuid.uuid4()))
        self.assertGreater(len(ai_response), 50)

    def test_llm_tool_call_with_summary(self):
        history = history_two_turns
        user_message = "Change my medicine lorazepam."
        ai_response, summary = self.llm_graph.chat_inference(user_message, history, "test_" + str(uuid.uuid4()))
        self.assertGreater(len(summary), 0)

