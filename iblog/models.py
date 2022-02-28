from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.
class USERBLOG(models.Model):
    id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=25)
    author=models.CharField(max_length=14,default="")
    description=models.TextField()
    timeStamp=models.DateTimeField(default=datetime.now)
    tag= models.CharField(max_length=20, default="")
    user=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.title + " by " + self.author
