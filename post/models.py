from django.db import models
from user.models import User  
class Post(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=700)
    author = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    date_add = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ['title', 'author']
    