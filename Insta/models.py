from django.db import models
from imagekit.models import ProcessedImageField # need to add imagekit to app directory, otw can't import

# Create your models here.
class Post(models.Model):
    title = models.TextField(blank=True, null=True) # title can be blank or null
    image = ProcessedImageField(
        upload_to = 'static/images/posts',
        format = 'JPEG', 
        options = {'quality': 100}, 
        blank = True, 
        null = True
    )

class PostTwo(models.Model):
    title = models.TextField(blank=True, null=True) # title can be blank or null
    image = ProcessedImageField(
        upload_to = 'static/images/posts',
        format = 'JPEG', 
        options = {'quality': 100}, 
        blank = True, 
        null = True
    )