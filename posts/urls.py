from django.urls import path
from .views import (
    PostListView,
    PostCreateAPIView,
    RecentPostListView,
    PostDetailView,
    PostsByCategoryView,
    PostsByTagView,
    TagListView,
    CategoryListView,
    PostTypeListView
)

urlpatterns = [
    path('posts/create/', PostCreateAPIView.as_view(), name='post-create'),
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/recent/', RecentPostListView.as_view(), name='recent-post-list'),
    path('posts/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:pk>/likes/add/', PostDetailView.as_view(), name='post-like-add'),
    path('posts/<int:pk>/likes/remove/', PostDetailView.as_view(), name='post-like-remove'),
    path('posts/tags/', PostsByTagView.as_view(), name='posts-by-tag'),  # Updated here
    path('posts/categories/', PostsByCategoryView.as_view(), name='posts-by-category'),  # Updated here
    path('posts/tags/list/', TagListView.as_view(), name='tag-list'),
    path('posts/categories/list/', CategoryListView.as_view(), name='category-list'),
    path('posts/post-types/list/', PostTypeListView.as_view(), name='post-type-list'),
]
