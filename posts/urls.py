from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'posts', views.PostViewSet)
router.register(r'tags', views.TagViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'posttypes', views.PostTypeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('recent-posts/', views.RecentPostsView.as_view(), name='recent-posts'),
    path('posts-by-tag/<slug:tag_slug>/', views.PostsByTagView.as_view(), name='posts-by-tag'),
    path('posts-by-category/<slug:cat_slug>/', views.PostsByCategoryView.as_view(), name='posts-by-category'),

]
