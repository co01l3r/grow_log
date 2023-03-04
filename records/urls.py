from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.records, name='records'),
    path('record/<str:pk>/', views.record, name='record'),
    path('new/', views.create_or_edit_record, name='create_record'),
    path('edit/<str:pk>/', views.create_or_edit_record, name='edit_record'),
    path('delete/<str:pk>/', views.delete_record, name='delete_record'),
    path('record/phase_summary/<str:pk>/', views.phase_summary, name='phase_summary'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
