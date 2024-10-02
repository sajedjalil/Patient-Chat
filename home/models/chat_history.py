from django.db import models


class ChatHistory(models.Model):
    """
    This class represents the chat history model. It stores information about each chat message.

    Attributes:
    patient_id (int): The unique ID of the patient associated with the chat message.
    thread_id (str): The ID of the chat thread. Unique across all users and all conversations.
    is_user (bool): Indicates whether the message is sent by the user (True) or the bot (False).
    text (str): The content of the chat message.
    summary (str): The summary of the chat message. Can be null or blank.
    timestamp (datetime): The timestamp of when the chat message was sent.

    Methods:
    None
    """

    patient_id = models.IntegerField()
    thread_id = models.CharField(max_length=50)
    is_user = models.BooleanField()
    text = models.TextField()
    summary = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    # Mapping for database table name
    class Meta:
        db_table = 'chat_history'
