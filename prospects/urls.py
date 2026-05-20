from django.urls import path

from . import views

app_name = 'prospects'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('create/', views.prospect_form, name='prospect_create'),
    path('edit/<int:pk>/', views.prospect_form, name='prospect_edit'),
    path('delete/<int:pk>/', views.prospect_delete, name='prospect_delete'),
]
