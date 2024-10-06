from django.db import models

# Create your models here.

class Article(models.Model):
    topic = models.CharField(max_length=250, unique=True)
    content= models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.topic
    
class MessageHistory(models.Model):
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message