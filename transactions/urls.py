from famtrust.utils import CustomDefaultRouter
from transactions import views

router = CustomDefaultRouter()

router.register(
    prefix="transactions",
    viewset=views.TransactionViewSet,
    basename="transaction",
)

urlpatterns = router.urls
