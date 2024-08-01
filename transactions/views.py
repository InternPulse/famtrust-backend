"""
This module defines all the views (endpoints) for working with transactions.
"""

from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
)
from rest_framework import viewsets

from famtrust import permissions
from transactions import (
    models,
    serializers,
)


@extend_schema(tags=["Transactions"])
class TransactionViewSet(viewsets.ModelViewSet):
    """A collection of endpoints for Transaction operations."""

    http_method_names = ("get", "post", "put", "delete")
    serializer_class = serializers.TransactionSerializer
    permission_classes = [permissions.IsAuthenticatedWithUserService]

    def get_queryset(self):
        """Retrieves all transactions for the current user."""
        user = self.request.ft_user
        return models.Transaction.objects.filter(user_id=user.id)

    def perform_create(self, serializer):
        user = self.request.ft_user
        serializer.validated_data["user_id"] = user.id
        super().perform_create(serializer)

    @extend_schema(
        summary="Create a new transaction",
        responses=OpenApiResponse(
            response=serializers.TransactionSerializer,
            description="Transaction created successfully",
        ),
    )
    def create(self, request, *args, **kwargs):
        """Create a new transaction.

        This endpoint is only accessible to authenticated users. The sole
        purpose of this endpoint is to create new transactions.

        Everyone who is authenticated can create a new transaction.
        """
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Retrieve a list of transactions",
        responses=OpenApiResponse(
            response=serializers.TransactionSerializer(many=True),
            description="List of transactions retrieved successfully",
        ),
    )
    def list(self, request, *args, **kwargs):
        """Retrieve a list of transactions.

        This endpoint is only accessible to authenticated users. The sole
        purpose of this endpoint is to retrieve a list of transactions.

        Everyone who is authenticated can retrieve a list of transactions.
        """
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Retrieve a transaction by ID",
        responses=OpenApiResponse(
            response=serializers.TransactionSerializer,
            description="Transaction retrieved successfully",
        ),
    )
    def retrieve(self, request, *args, **kwargs):
        """Retrieve a transaction by ID.

        This endpoint is only accessible to authenticated users. The sole
        purpose of this endpoint is to retrieve a transaction by its ID.

        Everyone who is authenticated can retrieve a transaction by its ID.
        """
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Update a transaction",
        responses=OpenApiResponse(
            response=serializers.TransactionSerializer,
            description="Transaction updated successfully",
        ),
    )
    def update(self, request, *args, **kwargs):
        """Update a transaction.

        This endpoint is only accessible to authenticated users. The sole
        purpose of this endpoint is to update an existing transaction.

        Everyone who is authenticated can update an existing transaction.
        """
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete a transaction by ID",
        responses=OpenApiResponse(
            response=serializers.TransactionSerializer,
            description="Transaction deleted successfully",
        ),
    )
    def destroy(self, request, *args, **kwargs):
        """Delete a transaction by ID.

        This endpoint is only accessible to authenticated users. The sole
        purpose of this endpoint is to delete an existing transaction.

        Everyone who is authenticated can delete an existing transaction.
        """
        return super().destroy(request, *args, **kwargs)
