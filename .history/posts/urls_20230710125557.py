from django.urls import path
from .views import PostListCreateView, PostRetrieveUpdateDeleteView

urlpatterns = [
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('posts/<int:id>/', PostRetrieveUpdateDeleteView.as_view(), name='post-detail'),
]
