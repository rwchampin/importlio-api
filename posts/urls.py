from django.urls import path
from .views import PostListView,PostCreateAPIView, RecentPostListView, PostDetailView, PostsByCategoryView, PostsByTagView, TagListView, CategoryListView

urlpatterns = [
        path('posts/create/', PostCreateAPIView.as_view(), name='post-create'),
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/recent/', RecentPostListView.as_view(), name='recent-post-list'),
    path('posts/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    path('api/posts/', PostsByCategoryView.as_view(), name='posts-by-category'),
    path('api/posts/', PostsByTagView.as_view(), name='posts-by-tag'),
    path('posts/<int:pk>/likes/add/', PostDetailView.as_view(), name='post-like-add'),
    path('posts/<int:pk>/likes/remove/', PostDetailView.as_view(), name='post-like-remove'),
    path('posts/tags/', TagListView.as_view(), name='tag-list'),
    path('posts/categories/', CategoryListView.as_view(), name='category-list'),
]
