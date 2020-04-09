from annoying.decorators import ajax_request # need to pipenv install djanjo-annoying
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post, Like, Comment, InstaUser, UserConnection # view needs both template and model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from Insta.forms import CustomUserCreationForm

class HelloWorld(TemplateView):
    template_name = 'test.html' # template_name is an attribute of TemplateView, can set it to be any html file name under templates folder

    # TemplateView details: https://ccbv.co.uk/projects/Django/3.0/django.views.generic.base/TemplateView/

class PostsView(ListView): # reason this returns a list of objects is because there's default get_queryset() giving you all objects
    model = Post
    template_name = 'index.html'
    login_url = 'login'

    def get_queryset(self): # default gives you all posts from all users. Overriding this filters for posts only from people you've followed
        # return Post.objects() # this is default implementation for get_queryset. override to filter for posts
        
        if not self.request.user.is_authenticated:
            return 
        
        current_user = self.request.user
        following = set()
        for conn in UserConnection.objects.filter(creator=current_user).select_related('following'):
            following.add(conn.following)
        return Post.objects.filter(author__in=following)

class ExploreView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'explore.html'
    login_url = 'login'

    def get_queryset(self):
        return Post.objects.all().order_by('-posted_on')[:20]

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

class UserDetailView(LoginRequiredMixin, DetailView):
    model = InstaUser
    template_name = 'user_detail.html'
    login_url = 'login'

class PostCreateView(LoginRequiredMixin, CreateView): # mixin is a base class for certain utility/tool
    model = Post
    template_name = 'post_create.html'
    fields = '__all__'                      # fields user to provide
    login_url = 'login'                     # redirect url if not logged in

class PostUpdateView(UpdateView):
    model = Post
    template_name = 'post_update.html'
    fields = ['title']                      # can only update title

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = InstaUser
    template_name = 'user_update.html'
    fields = ['username', 'profile_pic']
    login_url = 'login'

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy("posts") # define redirect url when deleted successfully
    # use reverse_lazy when defining success url for delete, NOT reverse. reverse will give you cycle error

class SignUp(CreateView):
    template_name = 'signup.html'
    success_url = reverse_lazy("login")
    # form_class = UserCreationForm # unlike create/update/delete, you use the model=Post and fields (which defines a form), here you need to specify the form (model and fields)
    form_class = CustomUserCreationForm # update to use custom user



@ajax_request # this is from annoying.decorators library. addLike function only reacts to ajax request. doesn't need to define
def addLike(request):
    post_pk = request.POST.get('post_pk')
    post = Post.objects.get(pk=post_pk)
    try:
        like = Like(post=post, user=request.user) # create new like
        like.save() # save the new like into db. return error if post already liked by the user, since we set user-post to be unique in Like model
        result = 1
    except Exception as e: # means the object already exist in db (already liked). then we need to remove the like upon clicking
        like = Like.objects.get(post=post, user=request.user)
        like.delete()
        result = 0

    return {
        'result': result,
        'post_pk': post_pk
    }


@ajax_request
def addComment(request):
    comment_text = request.POST.get('comment_text')
    post_pk = request.POST.get('post_pk')
    post = Post.objects.get(pk=post_pk)
    commenter_info = {}

    try:
        comment = Comment(comment=comment_text, user=request.user, post=post)
        comment.save()

        username = request.user.username

        commenter_info = {
            'username': username,
            'comment_text': comment_text
        }

        result = 1
    except Exception as e:
        print(e)
        result = 0

    return {
        'result': result,
        'post_pk': post_pk,
        'commenter_info': commenter_info
    }

@ajax_request
def addFollow(request):
    user_followed_pk = request.POST.get('follow_user_pk')
    user_followed = InstaUser.objects.get(pk=user_followed_pk)
    try:
        follow = UserConnection(creator=request.user, following=user_followed) # create new like
        follow.save() # save the new userconnection into db. return error if request.user already followed user, since we set unique_together
        result = 1
    except Exception as e: # means the object already exist in db (already followed). then we need to remove the following userconnection
        follow = UserConnection.objects.get(creator=request.user, following=user_followed)
        follow.delete()
        result = 0

    return {
        'result': result,
        'user_followed_pk': user_followed_pk
    }
