from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'posts', views.PostViewSet)
router.register(r'tags', views.TagViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'post-types', views.PostTypeViewSet)
router.register(r'post-ideas', views.PostTopicIdeasViewSet)

urlpatterns = [
   
    path('posts/recent/', views.RecentPostsView.as_view(), name='recent-posts'),
    path('posts/tags/<slug:tag>/', views.PostsByTagView.as_view(), name='posts-by-tag'),
    path('posts/categories/<slug:category>/', views.PostsByCategoryView.as_view(), name='posts-by-category'),
    path('posts/post-types/<slug:post_type>/', views.PostsByPostTypeView.as_view(), name='posts-by-post-type'),
    
    path('posts/update/<slug:slug>/', views.PostUpdateView.as_view(), name='post-update'),
    path('posts/count/', views.post_count, name='post_count'),
    path('', include(router.urls)),
]
