from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# Crie um router para as visualizações do DRF
router = DefaultRouter()
router.register(r'transfers', views.TransferViewSet)
router.register(r'payment-requests', views.PaymentRequestViewSet)

urlpatterns = [
    # URL para as visualizações tradicionais
    path('transaction-report/', views.transaction_report, name='transaction_report'),
    path('payment-request-list/', views.payment_request_list, name='payment_request_list'),
    path('create-payment-request/', views.create_payment_request, name='create_payment_request'),
    path('payment-request-details/<uuid:id>/', views.payment_request_details, name='payment_request_details'),

    # URL para as visualizações do DRF
    path('api/', include(router.urls)),

    # URLs do drf-spectacular para documentação da API
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
