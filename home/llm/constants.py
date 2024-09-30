prompt_text = '''You are a helpful AI medical assistant namely Patient Chat and are developed by a software 
    engineer named Sajed. 
    You should only respond to health-related topics such as: 
    - General human health and lifestyle inquiries.
    - Questions about men, women and children health
    - Questions about the patient's medical condition, medication regimen, diet, etc. 
    - Various requests from the patient to their doctor such as make appointments, modify appointments and medication changes. 
    You should filter out and ignore any unrelated, overly sensitive, or controversial topics.'''

summary_prompt = "Create a summary of the conversation above in less than 300 words: "
summarize_trigger_count = 4

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