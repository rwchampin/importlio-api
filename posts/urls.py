from django.urls import path
from .views import PostListView, RecentPostListView, PostDetailView, PostsByCategoryView, PostsByTagView

urlpatterns = [
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/recent/', RecentPostListView.as_view(), name='recent-post-list'),
    path('posts/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    path('api/posts/', PostsByCategoryView.as_view(), name='posts-by-category'),
    path('api/posts/', PostsByTagView.as_view(), name='posts-by-tag'),
]
