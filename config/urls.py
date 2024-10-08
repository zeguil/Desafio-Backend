from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# configuração do swagger
schema_view = get_schema_view(
    openapi.Info(
        title='Sistema de Gerenciamento de Tarefas',
        default_version='v1',
        description='Uma API REST para um sistema de gerenciamento de tarefas',
        terms_of_service=' ',
        contact=openapi.Contact(email='joseguilhermelins@gmail.com'),
        license=openapi.License(name='BSD License'),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0)),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0)),
    path('token/', TokenObtainPairView.as_view(), name='token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include('tasks.urls')),
    path('admin/', admin.site.urls),
]
