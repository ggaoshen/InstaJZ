from django.db import models
from imagekit.models import ProcessedImageField # need to add imagekit to app directory, otw can't import
from django.urls import reverse
from django.contrib.auth.models import AbstractUser # customized user base class

# Create your models here.
class InstaUser(AbstractUser):
    # profile_pic is in addition to what AbstractUser already defines, like username, pw, etc. 
    profile_pic = ProcessedImageField(
        upload_to = 'static/images/profiles',
        format = 'JPEG', 
        options = {'quality': 100}, 
        blank = True, 
        null = True
    ) # need to specify AUTH_USER_MODEL in settings.py

    def get_connections(self):
        connections = UserConnection.objects.filter(creator=self)
        return connections
    
    def get_followers(self):
        followers = UserConnection.objects.filter(following=self)
        return followers
    
    def is_followed_by(self, user): # am I followed by given user?
        followers = UserConnection.objects.filter(following=self) # my follower list
        return followers.filter(creator=user).exists() # is there a follower whose creator is the given user?

    def get_absolute_url(self):
        return reverse("user_detail", args=[str(self.id)]) # get url for post, with pk=self.id
    
    def __str__(self):
        return self.username


class UserConnection(models.Model): # relationship between creator and follower
    created = models.DateTimeField(auto_now_add=True, editable=False)
    creator = models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE,
        related_name="friendship_creator_set")
    following = models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE,
        related_name="friend_set")

    def __str__(self):
        return self.creator.username + ' follows ' + self.following.username

    # related_name example:
    # connection1 -> A follows B
    # connection2 -> A follows C
    # connection3 -> D follows A
    # A.friendship_creator_set -> (c1, c2)
    # A.friendship_set -> (c3)

    class Meta: # override metadata of UserConnection object  
        unique_together = ('creator', 'following') # user-followeduser pair must be unique


class Post(models.Model):
    author = models.ForeignKey(InstaUser, on_delete=models.CASCADE, related_name='my_posts')
    title = models.TextField(blank=True, null=True) # title can be blank or null
    image = ProcessedImageField(
        upload_to = 'static/images/posts',
        format = 'JPEG', 
        options = {'quality': 100}, 
        blank = True, 
        null = True
    )
    posted_on = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )

    def get_absolute_url(self): # THIS DEFINES REDIRECT PATH
        # return reverse("helloworld") # get the real url of urls.py's urlpatterns where name="helloworld"
        return reverse("post_detail", args=[str(self.id)]) # get url for post, with pk=self.id
    
    def get_like_count(self): # self.likes gets all likes in a post
        return self.likes.count()

    def get_comment_count(self):
        return self.comments.count()
    
    def __str__(self):
        return self.title


class PostTwo(models.Model):
    title = models.TextField(blank=True, null=True) # title can be blank or null
    image = ProcessedImageField(
        upload_to = 'static/images/posts',
        format = 'JPEG', 
        options = {'quality': 100}, 
        blank = True, 
        null = True
    )


class Like(models.Model): # this needs to link post and instauser. who liked your post
    post = models.ForeignKey(
        Post, 
        on_delete = models.CASCADE,  # delete like object when foreign key is deleted
        related_name = 'likes' # get all like instances related to given post 
    )

    user = models.ForeignKey(
        InstaUser, 
        on_delete = models.CASCADE, 
        related_name = 'likes'
    )

    # related_name example:
    # like1 = wentailai like post1
    # like2 = test like post2
    # post1.likes -> (like1, like2)
    # wentailai.likes -> (like1)   

    class Meta: # override metadata of Like object
        unique_together = ('post', 'user') # each user can only like 1 post. user-post pair must be unique

    def __str__(self): # this gives you a string representation of the object, instead of "Like object (1)". Instead: Like: shengao likes first post
        return 'Like: ' + self.user.username + ' likes ' + self.post.title


class Comment(models.Model): # similar to Like object
    user = models.ForeignKey(
        InstaUser, 
        on_delete = models.CASCADE, 
        related_name = 'comments'
    )

    post = models.ForeignKey(
        Post, 
        on_delete = models.CASCADE,  # delete like object when foreign key is deleted
        related_name = 'comments' # get all like instances related to given post 
    ) 

    comment = models.CharField(max_length=100)
    posted_on = models.DateTimeField(auto_now_add=True, editable=False)