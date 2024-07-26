from django.urls import path, include
from rest_framework.routers import DefaultRouter
from famtrust.utils import CustomDefaultRouter
from .views import FamilyGroupViewSet, FamilyMembershipViewSet

router = CustomDefaultRouter()



"""
Register the FamilyGroupViewSet with the router
"""
router.register(
    prefix="family-groups",
    viewset=FamilyGroupViewSet,
    basename="family-group",
)



"""
Register the MembershipViewSet with the router
"""
router.register(
    prefix="family-memberships",
    viewset=FamilyMembershipViewSet,
    basename="family-membership",
)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
