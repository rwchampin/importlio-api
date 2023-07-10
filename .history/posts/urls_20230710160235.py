from django.urls import path
from .views import PostListView, PostRetrieveUpdateDeleteView

urlpatterns = [
    path('posts/', PostListView.as_view(), name='post-list'),
    # path('posts/<int:id>/', PostRetrieveUpdateDeleteView.as_view(), name='post-detail'),
]
