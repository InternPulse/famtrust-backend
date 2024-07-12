from famtrust.urls import router

from .views import FamilyGroupsViewSet, MembershipsViewSet

router.register("family-groups", FamilyGroupsViewSet, basename="family-group")
router.register("memberships", MembershipsViewSet, basename="membership")

urlpatterns = router.urls
