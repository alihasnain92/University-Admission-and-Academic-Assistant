# backend/admission_assistant/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'admissions', views.AdmissionViewSet)
router.register(r'documents', views.DocumentViewSet)
router.register(r'payments', views.PaymentViewSet)
router.register(r'entry-tests', views.EntryTestViewSet)

urlpatterns = [
    path('', views.api_root, name='api-root'),
    path('query/', views.process_query, name='process-query'),
    path('', include(router.urls)),
]