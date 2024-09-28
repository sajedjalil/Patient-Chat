from django.db import models


class ChatHistory(models.Model):
    patient_id = models.IntegerField()
    chat_id = models.IntegerField()
    is_user = models.BooleanField()
    text = models.TextField()
    summary = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = 'chat_history'
