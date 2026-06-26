from django.shortcuts import render
from .models import Post

# Create your views here.
# user based views & class based views

def post_list(request):
    # get data submitted from the form

    posts = Post.objects.all() # [<Post: Post 1>, <Post: Post 2>]

    return render(request,
                   'posts/list.html',
                   {'posts': posts})

