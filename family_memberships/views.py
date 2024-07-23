from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import (
    OpenApiRequest,
    OpenApiResponse,
    extend_schema,
)
from rest_framework import (
    status,
    viewsets,
)

from .models import FamilyGroup, Membership
from .serializers import FamilyGroupSerializer, MembershipSerializer
from famtrust import permissions, utils


@extend_schema(tags=["Family Groups"], auth=[])
class FamilyGroupViewSet(viewsets.ModelViewSet):
    """A collection of endpoints for FamilyGroup operations."""

    http_method_names = ("get", "post", "put", "delete")
    serializer_class = FamilyGroupSerializer
    queryset = FamilyGroup.objects.all().order_by('created_at')  # Order by created_at
    permission_classes = (
        permissions.IsAuthenticatedWithUserService,
    )

    @extend_schema(
        summary="Retrieve all family groups",
        responses=OpenApiResponse(
            response=FamilyGroupSerializer,
            description="Family Groups retrieved successfully",
        ),
    )
    def list(self, request, *args, **kwargs):
        """List all family groups."""
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Retrieve a single family group",
        responses=OpenApiResponse(
            response=FamilyGroupSerializer,
            description="Family Group retrieved successfully",
        ),
    )
    def retrieve(self, request, *args, **kwargs):
        """Retrieve a single family group."""
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Create a new family group",
        responses=OpenApiResponse(
            response=FamilyGroupSerializer,
            description="Family Group created successfully",
        ),
        request=OpenApiRequest(
            request=FamilyGroupSerializer,
        ),
    )
    def create(self, request, *args, **kwargs):
        """Create a new family group."""
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Update an existing family group",
        responses=OpenApiResponse(
            description="Family Group updated successfully",
            response=FamilyGroupSerializer,
        ),
        request=OpenApiRequest(
            request=FamilyGroupSerializer,
        ),
    )
    def update(self, request, *args, **kwargs):
        """Update an existing family group."""
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete an existing family group",
        responses=OpenApiResponse(
            response=None,
            description="Family Group deleted successfully",
        ),
    )
    def destroy(self, request, *args, **kwargs):
        """Deletes an existing family group."""
        return super().destroy(request, *args, **kwargs)


@extend_schema(tags=["Memberships"], auth=[])
class MembershipViewSet(viewsets.ModelViewSet):
    """A collection of endpoints for Membership operations."""

    http_method_names = ("get", "post", "put", "delete")
    serializer_class = MembershipSerializer
    queryset = Membership.objects.all().order_by('joined_at')  # Order by joined_at
    permission_classes = (
        permissions.IsAuthenticatedWithUserService,
    )

    @extend_schema(
        summary="Retrieve all memberships",
        responses=OpenApiResponse(
            response=MembershipSerializer,
            description="Memberships retrieved successfully",
        ),
    )
    def list(self, request, *args, **kwargs):
        """List all memberships."""
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Retrieve a single membership",
        responses=OpenApiResponse(
            response=MembershipSerializer,
            description="Membership retrieved successfully",
        ),
    )
    def retrieve(self, request, *args, **kwargs):
        """Retrieve a single membership."""
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Create a new membership",
        responses=OpenApiResponse(
            response=MembershipSerializer,
            description="Membership created successfully",
        ),
        request=OpenApiRequest(
            request=MembershipSerializer,
        ),
    )
    def create(self, request, *args, **kwargs):
        """Create a new membership."""
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Update an existing membership",
        responses=OpenApiResponse(
            description="Membership updated successfully",
            response=MembershipSerializer,
        ),
        request=OpenApiRequest(
            request=MembershipSerializer,
        ),
    )
    def update(self, request, *args, **kwargs):
        """Update an existing membership."""
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete an existing membership",
        responses=OpenApiResponse(
            response=None,
            description="Membership deleted successfully",
        ),
    )
    def destroy(self, request, *args, **kwargs):
        """Deletes an existing membership."""
        return super().destroy(request, *args, **kwargs)
