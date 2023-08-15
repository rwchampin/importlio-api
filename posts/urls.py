from django.urls import path
from .views import (
    PostListView,
    PostCreateAPIView,
    RecentPostListView,
    PostDetailView,
    PostsByCategoryView,
    PostsByTagView,
    PostsByPostTypeView,
    TagListView,
    CategoryListView,
    PostTypeListView
)

urlpatterns = [
    path('posts/create/', PostCreateAPIView.as_view(), name='post-create'),
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/recent/', RecentPostListView.as_view(), name='recent-post-list'),
    path('posts/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    # path('posts/<int:pk>/likes/add/', PostDetailView.as_view(), name='post-like-add'),
    # path('posts/<int:pk>/likes/remove/', PostDetailView.as_view(), name='post-like-remove'),
    # List endpoints for tags and categories
    path('posts/tags/list/', TagListView.as_view(), name='tag-list'),
    path('posts/categories/list/', CategoryListView.as_view(), name='category-list'),
    path('posts/post-types/list/', PostTypeListView.as_view(), name='post-type-list'),
    
    # Endpoints for retrieving posts by tag and category
    path('posts/tags/<slug:slug>/', PostsByTagView.as_view(), name='posts-by-tag'),
    path('posts/categories/<slug:slug>/', PostsByCategoryView.as_view(), name='posts-by-category'),
    path('posts/post-types/<slug:slug>/', PostsByPostTypeView.as_view(), name='posts-by-post-type'),
]




