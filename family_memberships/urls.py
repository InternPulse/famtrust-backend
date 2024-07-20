# from famtrust.utils import CustomDefaultRouter

# from .views import FamilyGroupsViewSet, MembershipsViewSet

# router = CustomDefaultRouter()
# router.register(
#     prefix="family-groups",
#     viewset=FamilyGroupsViewSet,
#     basename="family-group",
# )
# router.register(
#     prefix="memberships", viewset=MembershipsViewSet, basename="membership"
# )

# urlpatterns = router.urls
from django.urls import path
from .views import *

# Namespace for the URLs
app_name = 'family_memberships'

# URL patterns for the API endpoints
urlpatterns = [
    # Endpoint for listing all family groups
    path('family-groups/', FamilyGroupListAPIView.as_view(), name='family-group-list'),
    # Endpoint for creating a new family group
    path('family-groups/create/', FamilyGroupCreateAPIView.as_view(), name='family-group-create'),
    # Endpoint for retrieving, updating, and deleting a specific family group by its ID
    path('family-groups/<uuid:pk>/', FamilyGroupDetailAPIView.as_view(), name='family-group-detail'),
    # Endpoint for listing all memberships
    path('memberships/', MembershipListAPIView.as_view(), name='membership-list'),
    # Endpoint for creating a new membership
    path('memberships/create/', MembershipCreateAPIView.as_view(), name='membership-create'),
    # Endpoint for retrieving, updating, and deleting a specific membership by its ID
    path('memberships/<uuid:pk>/', MembershipDetailAPIView.as_view(), name='membership-detail'),
]