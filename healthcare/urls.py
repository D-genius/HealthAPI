"""healthcare URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include ,re_path
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from patients.views import PatientViewSet
from doctors.views import DoctorViewSet, AvailabilityViewSet
from appointments.views import AppointmentViewSet
from users.views import CurrentUserView, ChangePasswordView
from oauth2_provider.urls import base_urlpatterns

app_name = 'healthcare'
schema_view = get_schema_view(
   openapi.Info(
      title="Healthcare API",
      default_version='v1',
      description="patient scheduling app",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="timothydiero254@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
    permission_classes=(permissions.AllowAny,),
)
router = DefaultRouter()
router.register(r'patients', PatientViewSet)
router.register(r'doctors', DoctorViewSet)
router.register(r'availability', AvailabilityViewSet)
router.register(r'appointments', AppointmentViewSet)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('o/', include(('oauth2_provider.urls', 'oauth2_provider'), namespace='oauth2_provider')),
    path('api/me/', CurrentUserView.as_view(), name='current-user'),
    path('api/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('swagger.<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json', label='Main API entry point'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
