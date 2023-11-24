from django.urls import path, re_path
from .views import *
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

# Configuração do drf-yasg para a documentação Swagger
schema_view = get_schema_view(
   openapi.Info(
      title="API Documentation",
      default_version='v1',
      description="API description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@yourapi.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(AllowAny,),
)

urlpatterns = [
    # ... outras urls ...

    # URLs tradicionais
    path('home/', home_view, name='home'),
    path('register/email/', register_email_view, name='register_email'),
    path('register/token/', register_token_view, name='register_token'),
    path('registration/success/', registration_success_view, name='registration_success'),
    path('login/', login_view, name='login'),
    path('login/token/', token_and_password_login_view, name='token_and_password_login'),

    # URLs da API
    path('api/register/', UserRegistrationAPIView.as_view(), name='api_register'),
    path('api/register/token/', TokenRegistrationAPIView.as_view(), name='api_register_token'),
    path('api/login/', LoginAPIView.as_view(), name='api_login'),
    path('api/referral-link/', ReferralLinkView.as_view(), name='referral-link'),

    # URLs do Swagger
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # ... outras urls ...
]
