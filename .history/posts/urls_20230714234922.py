from django.urls import path
from .views import PostListView, RecentPostListView#, #PostRetrieveUpdateDeleteView

urlpatterns = [
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/recent/', RecentPostListView.as_view(), name='recent-post-list'),
    # path('posts/<int:id>/', PostRetrieveUpdateDeleteView.as_view(), name='post-detail'),
]
