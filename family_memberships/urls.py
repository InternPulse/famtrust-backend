
from famtrust.utils import CustomDefaultRouter
from .views import FamilyGroupViewSet, MembershipViewSet

"""
 Create an instance of CustomDefaultRouter
"""
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
    viewset=MembershipViewSet,
    basename="membership",
)



"""
 Generate the URL patterns from the router
"""
urlpatterns = router.urls
