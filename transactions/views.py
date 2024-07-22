from drf_spectacular.utils import (
    extend_schema,
)
from rest_framework import viewsets


@extend_schema(tags=["Transactions"], auth=[])
class TransactionViewSet(viewsets.ModelViewSet):
    """A collection of endpoints for Transaction operations."""
