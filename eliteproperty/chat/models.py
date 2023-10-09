from django.db import models
from accounts.models import Account

class Message(models.Model):
    sender = models.ForeignKey(Account, related_name="sent_messages", on_delete=models.CASCADE)
    recipient = models.ForeignKey(Account, related_name="received_messages", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    room_id = models.CharField(max_length=10, unique=True, default=None)

    def __str__(self):
        return f"Message from {self.sender} to {self.recipient}"

    def save(self, *args, **kwargs):
        self.room_id = f"{self.sender.id}{self.recipient.id}"
        super(Message, self).save(*args, **kwargs)