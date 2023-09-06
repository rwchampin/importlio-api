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
    PostTypeListView,
    PostsByDateView,
    PostsByDateRangeView,
    PostsByMonthView,
    PostsByYearView,
    PostsDraftListView,
    PostUpdateAPIView,
    SimplePostCreateAPIView,
    PostDeleteAPIView,
    PostStatusListView,
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
    path('posts/post-status/list/', PostStatusListView.as_view(), name='post-status-list'),
    # Endpoints for retrieving posts by tag and category
    path('posts/tags/<slug:slug>/', PostsByTagView.as_view(), name='posts-by-tag'),
    path('posts/categories/<slug:slug>/', PostsByCategoryView.as_view(), name='posts-by-category'),
    path('posts/post-types/<slug:slug>/', PostsByPostTypeView.as_view(), name='posts-by-post-type'),
    
    path('posts/date/<int:year>/<int:month>/<int:day>/', PostsByDateView.as_view(), name='posts-by-date'),
    
    path('posts/date-range/<int:start_year>/<int:start_month>/<int:start_day>/<int:end_year>/<int:end_month>/<int:end_day>/', PostsByDateRangeView.as_view(), name='posts-by-date-range'),
    
    path('posts/month/<int:year>/<int:month>/', PostsByMonthView.as_view(), name='posts-by-month'),
    
    path('posts/year/<int:year>/', PostsByYearView.as_view(), name='posts-by-year'),
    
    path('posts/status/drafts/', PostsDraftListView.as_view(), name='posts-draft-list'),
    path('posts/<int:pk>/update/', PostUpdateAPIView.as_view(), name='post-update'),

    path('posts/simple/create/', SimplePostCreateAPIView.as_view(), name='simple-post-create'),
    
    path('posts/<int:pk>/delete/', PostDeleteAPIView.as_view(), name='post-delete'),
    
]




