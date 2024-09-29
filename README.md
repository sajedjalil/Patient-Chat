# Patient-Chat
An chat application that uses Langchain, Langgraph and knowledge graph.


## database
- Install postgresql from https://www.postgresql.org/download/
- Create the necessary database running the .sh files from db_scripts folder
- To run the files use ```chmod +x create_db_tables.sh insert_data.sh```
- Then run ```./create_db_tables.sh```
- Lastly, run ```./insert_data.sh```
- Configure the database connection parameters in settings.py

## Testing
- Run tests by ```python manage.py test```


