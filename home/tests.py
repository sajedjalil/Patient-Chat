import uuid

from django.test import TestCase

from home.constants.constants import history_two_turns, history_one_turn
from home.langchains.llm_graph import LLMGraph


class LLMTestCase(TestCase):
    def setUp(self):
        self.llm_graph = LLMGraph()

    def test_llm_name(self):
        user_message = "Hi, my name is Sajed. What's your name?"
        ai_response, summary, tools_called = self.llm_graph.chat_inference(user_message, [], "test_" + str(uuid.uuid4()))
        self.assertTrue(ai_response.__contains__("Patient Chat"))
        self.assertEqual(summary, None)
        self.assertEqual(tools_called, list())

    def test_llm_remembers_context_history(self):
        history = history_one_turn
        user_message = "Now tell me what's my name?"
        ai_response, summary, tools_called = self.llm_graph.chat_inference(user_message, history, "test_" + str(uuid.uuid4()))
        self.assertTrue(ai_response.__contains__("Sajed"))
        self.assertNotEqual(summary, None)
        self.assertEqual(tools_called, list())

    def test_llm_tool_call(self):
        history = []
        user_message = "Change my medication lorazepam."
        ai_response, summary, tools_called = self.llm_graph.chat_inference(user_message, history, "test_" + str(uuid.uuid4()))
        self.assertEqual(len(tools_called), 1)
        self.assertNotEqual(summary, None)
        # Tool calls internally increases token counts. We consider tools calling
        # as a separate chat. That's why its trigger summary early. It's simply a design choice. Change the logic of
        # LLMGraph.if_need_summarization() if you want a different design decision.

    def test_llm_tool_call_with_summary(self):
        history = history_two_turns
        user_message = "Change my medication lorazepam and schedule my appointment on Sunday."
        ai_response, summary, tools_called = self.llm_graph.chat_inference(user_message, history, "test_" + str(uuid.uuid4()))
        # Should make two tool calls. One for change medication and another for change appointment schedule.
        self.assertEqual(len(tools_called), 2)
        self.assertNotEqual(summary, None)


