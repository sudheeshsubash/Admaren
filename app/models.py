from django.db import models
from django.contrib.auth.models import User




class Tag(models.Model):
    title = models.CharField(max_length=30,unique=True)
    
    def __str__(self) -> str:
        return self.title
    

class Snippet(models.Model):
    title = models.CharField(max_length=30)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)
    created_user = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.title
    
    