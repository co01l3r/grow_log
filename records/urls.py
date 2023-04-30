from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.records, name='records'),
    path('record/<uuid:pk>/', views.record, name='record'),
    path('new/', views.create_or_edit_record, name='create_record'),
    path('edit/<uuid:pk>/', views.create_or_edit_record, name='edit_record'),
    path('delete/<uuid:pk>/', views.delete_record, name='delete_record'),
    path('record/phase_summary/<uuid:pk>/', views.phase_summary, name='phase_summary'),

    path('record/<uuid:pk>/new-log/', views.create_log, name='create_log'),
    path('record/<uuid:pk>/edit-log/<int:log_pk>/', views.edit_log, name='edit_log'),
    path('record/<uuid:pk>/delete-log/<int:log_pk>/', views.delete_log, name='delete_log'),

    path('record/<uuid:pk>/log/<int:log_pk>/nutrient-log/', views.create_feeding_log, name='create_feeding_log'),
    path('record/<uuid:pk>/log/<int:log_pk>/delete-nutrient-log/<int:nutrient_log_pk>/', views.delete_nutrient_log,
         name='delete_nutrient_log'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
