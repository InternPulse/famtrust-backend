from famtrust.urls import router
from .views import AccountsViewSet, TransactionsViewSet

router.register("accounts", AccountsViewSet, basename="account")
router.register("transactions", TransactionsViewSet, basename="transaction")

urlpatterns = router.urls
