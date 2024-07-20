from famtrust.utils import CustomDefaultRouter

from .views import FamilyGroupsViewSet, MembershipsViewSet

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

urlpatterns = router.urls
