from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'posts', views.PostViewSet)
router.register(r'posts-preview', views.PostPreviewViewSet)
router.register(r'tags', views.TagViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'post-types', views.PostTypeViewSet)
router.register(r'post-ideas', views.PostTopicIdeasViewSet)
router.register(r'post-outlines', views.PostOutlineViewSet)

urlpatterns = [
    path('posts/rewrite/', views.rewrite_post, name='post-rewrite'),
    path('posts/make-posts/', views.make_posts, name='make-posts'),
    path('posts/tags/<slug:tag>/', views.PostsByTagView.as_view(), name='posts-by-tag'),
    path('posts/categories/<slug:category>/', views.PostsByCategoryView.as_view(), name='posts-by-category'),
    path('posts/post-types/<slug:post_type>/', views.PostsByPostTypeView.as_view(), name='posts-by-post-type'),
    
    path('', include(router.urls)),
]
