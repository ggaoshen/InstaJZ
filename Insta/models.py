from django.db import models
from imagekit.models import ProcessedImageField # need to add imagekit to app directory, otw can't import
from django.urls import reverse

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

    def get_absolute_url(self):
        # return reverse("helloworld") # get the real url of urls.py's urlpatterns where name="helloworld"
        return reverse("post_detail", args=[str(self.id)]) # get url for post, with pk=self.id


class PostTwo(models.Model):
    title = models.TextField(blank=True, null=True) # title can be blank or null
    image = ProcessedImageField(
        upload_to = 'static/images/posts',
        format = 'JPEG', 
        options = {'quality': 100}, 
        blank = True, 
        null = True
    )