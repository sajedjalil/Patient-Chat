# Patient-Chat
A chat application that uses Langchain, Langgraph and knowledge graph.


## Project Structure
- 📁  Patient_chat
- 📁  home
  - 📁 constants
  - 📁 langchains
  - 📁 function_tools
  - 📁 models
  - 📁 services
- 📁 notebooks
- 📁 static
- 📁 templates


## Long chat optimizations
Front end sends all the history to the backend. But we filter and summarize in the backend and store the summary in the database for future use, using a random ```thread_id``` in Langsmith. This ```thread_id``` is unique across all database users.

## database
- Install postgresql from https://www.postgresql.org/download/
- Create the necessary database running the .sh files from db_scripts folder
- To run the files use ```chmod +x create_db_tables.sh insert_data.sh```
- Then run ```./create_db_tables.sh```
- Lastly, run ```./insert_data.sh```
- Configure the database connection parameters in settings.py

## Knowledge Graph
- Install Neo4j https://neo4j.com/download/ or use the server version
- Specify the environment variables for connection in the .env file

## Testing
- Run tests by ```python manage.py test```


## Changing AI Models
Settings and langchain dependencies for OpenAI, Anthropic and Google Gemini is already added. You just need to put your API key in ```.env``` file. For other libraries like Ollama, Cohere etc. you will need to follow the steps below:
1. (**Required**) Add the model's langchain dependency in ```requirements.txt```e.g., ```langchain_openai```
2. (**Required**) Add the environment variable for the API Key in ```settings.py``` e.g., ```OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')```
3. (**Optional**) To keep the model list together add an entry in ```constants.py```.
4. (**Required**) Add the actual API Key ```.env``` file. e.g., ```OPENAI_API_KEY=your-api-key```

## FUnction calling
- Change appointment date
- Create

