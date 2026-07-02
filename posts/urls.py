from django.urls import path
from . import views

urlpatterns = [
    # web pages
    path('', views.post_list, name='post_list'),
    path('news/new/', views.create_news, name='create_news'),

    path('news/<uuid:id>/', views.post_detail, name='post_detail'),

    path('support/', views.support, name='support'),

    # api
    path('api/posts/', views.post_collection, name='api_posts'),
]
