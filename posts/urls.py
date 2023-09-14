from django.urls import path
from .views import (
    RecentPostListView,
    PostDetailView,
    PostsByCategoryView,
    PostsByTagView,
    PostsByPostTypeView,
    TagListView,
    CategoryListView,
    PostTypeListView,
    PostStatusListView,
    PostUpdateAPIView,
    PostDeleteAPIView,
    PostListView,
    PostCreateView,
    BlankPostCreateAPIView
)

 
 
urlpatterns = [
      path('tags/', TagListView.as_view(), name='tag-list'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('post-types/', PostTypeListView.as_view(), name='post-type-list'),
    path('post-status/', PostStatusListView.as_view(), name='post-status-list'),
     # POST DETAIL ENDPOINTS
    path('posts/<slug:slug>/', PostDetailView.as_view(), name='post-detail-slug'),

    # POST UPDATE ENDPOINTS
    path('posts/<int:pk>/update/', PostUpdateAPIView.as_view(), name='post-update-pk'),

    # POST DELETE ENDPOINTS
    path('posts/<int:pk>/delete/', PostDeleteAPIView.as_view(), name='post-delete-pk'),

    # Create a blank post
    path('posts/create/blank/', BlankPostCreateAPIView.as_view(), name='post-create-blank'),

    # Create a post
    path('posts/create/new/', PostCreateView.as_view(), name='post-create'),

    # List of recent posts
    path('posts/recent/', RecentPostListView.as_view(), name='recent-post-list'),

    # List of all posts
    path('posts/', PostListView.as_view(), name='post-list'),


  
    # # Endpoints for retrieving posts by tag and category
    # path('posts/tags/<slug:slug>/', PostsByTagView.as_view(), name='posts-by-tag'),
    # path('posts/categories/<slug:slug>/', PostsByCategoryView.as_view(), name='posts-by-category'),
    # path('posts/post-types/<slug:slug>/', PostsByPostTypeView.as_view(), name='posts-by-post-type'),
    # path('posts/post-status/<slug:slug>/', PostsByPostTypeView.as_view(), name='posts-by-post-status'),
    # path('posts/date/<int:year>/<int:month>/<int:day>/', PostsByDateView.as_view(), name='posts-by-date'),
    
    # path('posts/date-range/<int:start_year>/<int:start_month>/<int:start_day>/<int:end_year>/<int:end_month>/<int:end_day>/', PostsByDateRangeView.as_view(), name='posts-by-date-range'),
    
    # path('posts/month/<int:year>/<int:month>/', PostsByMonthView.as_view(), name='posts-by-month'),
    
    # path('posts/year/<int:year>/', PostsByYearView.as_view(), name='posts-by-year'),
    
    # path('posts/status/drafts/', PostsDraftListView.as_view(), name='posts-draft-list'),
    
]




