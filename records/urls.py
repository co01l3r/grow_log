from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.records, name='records'),
    path('record/<str:pk>/', views.record, name='record'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)