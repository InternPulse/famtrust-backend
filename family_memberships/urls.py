from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FamilyGroupViewSet, MembershipViewSet

router = CustomDefaultRouter()
router.register(
    prefix="family-groups",
    viewset=FamilyGroupsViewSet,
    basename="family-group",
)
router.register(
    prefix="family-memberships",
    viewset=MembershipsViewSet,
    basename="family-membership",
)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
