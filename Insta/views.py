from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Post # view needs both template and model

class HelloWorld(TemplateView):
    template_name = 'test.html' # tempalte_name is an attribute of TemplateView, can set it to be any html file name under templates folder

    # TemplateView details: https://ccbv.co.uk/projects/Django/3.0/django.views.generic.base/TemplateView/

class PostsView(ListView):
    model = Post
    template_name = 'index.html'

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

class PostCreateView(CreateView):
    model = Post
    template_name = 'post_create.html'
    fields = '__all__'                      # fields user to provide

class PostUpdateView(UpdateView):
    model = Post
    template_name = 'post_update.html'
    fields = ['title']                      # can only update title

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy("helloworld") # define redirect url when deleted successfully
    # use reverse_lazy when defining success url for delete, NOT reverse. reverse will give you cycle error