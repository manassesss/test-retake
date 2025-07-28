from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PartyViewSet, PartyContactViewSet

router = DefaultRouter()
router.register(r'parties', PartyViewSet)
router.register(r'party-contacts', PartyContactViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
] 