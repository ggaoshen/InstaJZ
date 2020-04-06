from django.views.generic import TemplateView, ListView

from .models import Post # view needs both template and model

class HelloWorld(TemplateView):
    template_name = 'test.html' # tempalte_name is an attribute of TemplateView, can set it to be any html file name under templates folder

    # TemplateView details: https://ccbv.co.uk/projects/Django/3.0/django.views.generic.base/TemplateView/

class PostsView(ListView):
    model = Post
    tempalte_name = 'index.html'