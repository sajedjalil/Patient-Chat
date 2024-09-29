from django.test import TestCase

from home.llm.llm_graph import LLMGraph


class LLMTestCase(TestCase):
    def setUp(self):
        self.llm_graph = LLMGraph()

    def test_llm_name(self):
        user_message = "Hi, my name is Sajed. What's your name?"
        ai_response = self.llm_graph.inference(user_message, [])

        self.assertTrue(ai_response.__contains__("Patient Chat"))

    def test_llm_remembers_context_history(self):

        history = [
            {
                "role": "user",
                "content": "Hi, my name is Sajed. What's your name?"
            },
            {
                "role": "assistant",
                "content": "Hello Sajed, how can I assist you today? I'm an AI medical assistant and I'm happy to "
                           "help with any health-related inquiries or requests you may have. Please let me know how I "
                           "can be of service."
            },
        ]
        user_message = "Now tell me what's my name?"
        ai_response = self.llm_graph.inference(user_message, history)

        print(ai_response)
        self.assertTrue(ai_response.__contains__("Sajed"))
