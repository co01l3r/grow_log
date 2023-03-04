from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.records, name='records'),
    path('record/<str:pk>/', views.record, name='record'),
    path('new/', views.new_cycle, name='new_cycle'),
    path('record/phase_summary/<str:pk>/', views.phase_summary, name='phase_summary'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
