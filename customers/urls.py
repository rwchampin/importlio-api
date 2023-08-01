from django.urls import path
from .views import (
    CustomerListCreateView,
    CustomerDetailView,
    CompanyListCreateView,
    CompanyDetailView,
    DealListCreateView,
    DealDetailView,
    TaskListCreateView,
    TaskDetailView,
    NoteListCreateView,
    NoteDetailView,
    ContactListCreateView,
    ContactDetailView,
)

urlpatterns = [
    path('customers/', CustomerListCreateView.as_view(), name='customer-list-create'),
    path('customers/<int:pk>/', CustomerDetailView.as_view(), name='customer-detail'),
    path('companies/', CompanyListCreateView.as_view(), name='company-list-create'),
    path('companies/<int:pk>/', CompanyDetailView.as_view(), name='company-detail'),
    path('deals/', DealListCreateView.as_view(), name='deal-list-create'),
    path('deals/<int:pk>/', DealDetailView.as_view(), name='deal-detail'),
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('notes/', NoteListCreateView.as_view(), name='note-list-create'),
    path('notes/<int:pk>/', NoteDetailView.as_view(), name='note-detail'),
    path('contacts/', ContactListCreateView.as_view(), name='contact-list-create'),
    path('contacts/<int:pk>/', ContactDetailView.as_view(), name='contact-detail'),
]
