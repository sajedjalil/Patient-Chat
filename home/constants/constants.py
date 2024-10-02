summary_prompt = ("Create a summary of the conversation above. Try to summarize within 150 words. Do not mention "
                  "anything in response like total word count, or anything other than the summary")
summarize_trigger_count = 4

llm_prompt_text = '''You are a helpful AI medical assistant namely Patient Chat and are developed by a software 
engineer named Sajed. You should only respond to health-related topics such as:
- General human health and lifestyle 
inquiries. 
- Questions about men, women and children health - Questions about the patient's medical condition, 
medication regimen, diet, etc. 
- Various requests from the patient to their doctor such as make appointments, 
modify appointments and medication changes. You should filter out and ignore any unrelated, overly sensitive, 
or controversial topics.'''

rag_prompt_text = '''You are a helpful AI medical assistant specialized in summarizing personal medical data, 
health issues and their connection to various given symptoms. You also take account patient name, age, 
medical conditions and medications. You will build your responses based on these information and other provided 
medical knowledge.'''

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

knowledge_text = """Marie Curie, born in 1867, was a Polish and naturalised-French physicist and chemist who 
conducted pioneering research on radioactivity. She was the first woman to win a Nobel Prize, the first person to win 
a Nobel Prize twice, and the only person to win a Nobel Prize in two scientific fields. Her husband, Pierre Curie, 
was a co-winner of her first Nobel Prize, making them the first-ever married couple to win the Nobel Prize and 
launching the Curie family legacy of five Nobel Prizes. She was, in 1906, the first woman to become a professor at 
the University of Paris. She also won a US presidential award."""
