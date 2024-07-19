from famtrust.utils import CustomDefaultRouter

from .views import FamilyGroupsViewSet, MembershipsViewSet

router = CustomDefaultRouter()
router.register(
    prefix="family-groups",
    viewset=FamilyGroupsViewSet,
    basename="family-group",
)
router.register(
    prefix="memberships", viewset=MembershipsViewSet, basename="membership"
)

urlpatterns = router.urls
