from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

# router.register(r'niches', views.NicheViewSet)
# router.register(r'emails', views.EmailViewSet)
router.register(r'list-previews', views.PreviewMarketingListViewSet)

urlpatterns = [
   
    path('marketing/get-data/', views.get_data),
    path('marketing/create-emails/', views.bulk_create_emails),
     path('marketing/', include(router.urls)),
    # path('marketing/emails/', views.EmailListView.as_view()),
    # path('marketing/niches/', views.NicheListView.as_view()),
    # path('marketing/list/download/', views.download_emails_by_niche),
]
