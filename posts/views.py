from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from posts.serializers import PostSerializer
from .models import Post


# Create your views here.
# user based views & class based views

def post_list(request):
    # newest first
    posts = Post.objects.all().order_by('-created')

    # paginate: 6 stories per page
    paginator = Paginator(posts, 6)
    page = paginator.get_page(request.GET.get('page'))

    return render(request, 'posts/list.html', {'posts': page, 'page': page})


def post_detail(request, id):
    post = get_object_or_404(Post, id = id)
    return render(request, 'posts/detail.html', {'post': post})


def support(request):
    return render(request, 'support.html')


def _unique_slug(title):
    base = slugify(title)[:45].rstrip('-') or 'post'
    slug = base
    i = 2
    while Post.objects.filter(slug=slug).exists():
        slug = f'{base}-{i}'
        i += 1
    return slug


def create_news(request):
    # Only editors may publish news. Being a superuser is NOT enough.
    if not request.user.is_authenticated or not request.user.is_editor:
        messages.error(request, 'Only editors can publish news.')
        return redirect('post_list')

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        body = request.POST.get('body', '').strip()

        if not title or not body:
            messages.error(request, 'Title and body are required.')
        else:
            Post.objects.create(title=title, slug=_unique_slug(title), body=body)
            messages.success(request, 'News published successfully.')
            return redirect('post_list')

        # failed submit: keep what the editor already typed
        return render(request, 'posts/create.html',
                      {'title': title, 'body': body})

    return render(request, 'posts/create.html')


@api_view(['GET', 'POST']) # decorators
@authentication_classes([TokenAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def post_collection(request: Request):
    if request.method == 'POST':
        data: dict = request.data

        # create a new post
        title = data.get('title')
        body = data.get('body')

        if not title or not body:
            return Response({'detail': 'title and body are required.'},
                            status=status.HTTP_400_BAD_REQUEST)

        post = Post.objects.create(title=title, slug=_unique_slug(title),
                                   body=body)

        return Response(PostSerializer(post).data,
                        status=status.HTTP_201_CREATED)

    posts = Post.objects.all() # [<Post: Post 1>, <Post: Post 2>]

    serializer = PostSerializer(posts, many=True)

    return Response(serializer.data)