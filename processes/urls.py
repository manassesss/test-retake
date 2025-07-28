from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProcessViewSet

router = DefaultRouter()
router.register(r'processes', ProcessViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
] 