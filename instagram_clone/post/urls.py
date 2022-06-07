from post.views import  NewPost, like, IndexView, PostDetailsView
from django.urls import path
from django.contrib.auth.decorators import login_required

urlpatterns =[
    # path('', index, name='index'),
    path('', login_required(IndexView.as_view()), name='index'),
    path('newpost/', NewPost, name='newpost'),
    path('<int:pk>',login_required(PostDetailsView.as_view()), name='postdetails'),
    path('<uuid:post_id>/like', like, name='postlike'),
]