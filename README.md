# Patient-Chat
A chat application that uses Langchain, Langgraph and knowledge graph.

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


## Changing models
- requirements.txt
- settings.py
- constants.py
- .env

## FUnction calling
- Change appointment date
- Create

