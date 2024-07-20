from famtrust.utils import CustomDefaultRouter

from .views import (
    AccountViewSet,
    FamilyAccountViewSet,
    FundRequestViewSet,
    SubAccountViewSet,
    TransactionViewSet,
)

router = CustomDefaultRouter()
router.register(
    prefix="sub-accounts", viewset=SubAccountViewSet, basename="sub-account"
)
router.register(
    prefix="transactions", viewset=TransactionViewSet, basename="transaction"
),
router.register(
    prefix="family-accounts",
    viewset=FamilyAccountViewSet,
    basename="family-account",
)
router.register(prefix="accounts", viewset=AccountViewSet, basename="account")
router.register(
    prefix="fund-requests",
    viewset=FundRequestViewSet,
    basename="fund-request",
)
urlpatterns = router.urls
