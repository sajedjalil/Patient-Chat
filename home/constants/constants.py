# prompt used for summarization node.
summary_prompt = ("Create a summary of the conversation above. Try to summarize within 150 words. Do not mention "
                  "anything in response like total word count, or anything other than the summary")

# Starts summarizing when we reach summarize_trigger_count amount chat combining both AI and user
summarize_trigger_count = 4

# prompt used for llm_graph with tool call and summarization
llm_prompt_text = '''You are a helpful AI medical assistant namely Patient Chat and are developed by a software 
engineer named Sajed. You should only respond to health-related topics such as:
- General human health and lifestyle 
inquiries. 
- Questions about men, women and children health - Questions about the patient's medical condition, 
medication regimen, diet, etc. 
- Various requests from the patient to their doctor such as make appointments, 
modify appointments and medication changes. You should filter out and ignore any unrelated, overly sensitive, 
or controversial topics.'''

# prompt used for RAG architecture and knowledge graph.
rag_prompt_text = '''You are a helpful AI medical assistant specialized in summarizing personal medical data, 
health issues and their connection to various given symptoms. You also take account patient name, age, 
medical conditions and medications. You will build your responses based on these information and other provided 
medical knowledge.'''

# Sample one pair of user and assistant history for various tests
history_one_turn = history = [
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

# Sample two pairs of user and assistant history for various tests
history_two_turns = [
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
    {
        "role": "user",
        "content": "Hi, how are you? Answer in one line."
    },
    {
        "role": "assistant",
        "content": "I am doing great."
    }
]
