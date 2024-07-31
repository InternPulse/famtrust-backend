from django.db.models import Q
from drf_spectacular.utils import (
    OpenApiRequest,
    OpenApiResponse,
    extend_schema,
)
from rest_framework import (
    status,
    viewsets,
)
from rest_framework.decorators import action
from rest_framework.response import Response

from famtrust import (
    permissions,
    utils,
)
from . import models
from .serializers import (
    FamilyGroupSerializer,
    FamilyMembershipInFamilyGroupSerializer,
    FamilyMembershipSerializer,
)


@extend_schema(tags=["Family Groups"])
class FamilyGroupViewSet(viewsets.ModelViewSet):
    """A collection of endpoints for FamilyGroup operations."""

    serializer_class = FamilyGroupSerializer
    permission_classes = (permissions.IsAuthenticatedWithUserService,)
    filterset_fields = ("name", "owner_id", "is_default")

    def get_queryset(self):
        """Returns a queryset of FamilyGroup objects.

        Members of a family can see only the groups they belong to, while
        Admins can see both the groups they own and the groups they belong to.
        """
        user = self.request.ft_user
        return models.FamilyGroup.objects.filter(
            Q(members__user_id=user.id) | Q(owner_id=user.id)
        )

    def perform_create(self, serializer):
        serializer.validated_data["owner_id"] = self.request.ft_user.id
        super().perform_create(
            serializer
        )

    def perform_destroy(self, instance):
        if instance.is_default:
            raise utils.HTTPException(
                detail={
                    "error": "The default family group cannot be deleted.",
                    "next_steps": "Assign a new default group before deleting "
                                  "this group.",
                },
                status_code=status.HTTP_409_CONFLICT,
            )
        if "force" in self.request.data:
            if self.request.data["force"]:
                return super().perform_destroy(
                    instance
                )
        if models.FamilyMembership.objects.filter(
            family_group_id=instance.id
        ).exists():
            raise utils.HTTPException(
                detail={
                    "error": "The family group has members and cannot be "
                             "deleted.",
                    "next_steps": "Move all members to another group "
                                  "before deleting the group.",
                },
                status_code=status.HTTP_409_CONFLICT,
            )
        return super().perform_destroy(
            instance
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
        return super().list(
            request,
            *args,
            **kwargs
        )

    @extend_schema(
        summary="Retrieve a single family group",
        responses=OpenApiResponse(
            response=FamilyGroupSerializer,
            description="Family Group retrieved successfully",
        ),
    )
    def retrieve(self, request, *args, **kwargs):
        """Retrieve a single family group."""
        return super().retrieve(
            request,
            *args,
            **kwargs
        )

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
        return super().create(
            request,
            *args,
            **kwargs
        )

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
        return super().update(
            request,
            *args,
            **kwargs
        )

    @extend_schema(
        summary="Delete an existing family group",
        responses=OpenApiResponse(
            response=None,
            description="Family Group deleted successfully",
        ),
    )
    def destroy(self, request, *args, **kwargs):
        """Deletes an existing family group."""
        return super().destroy(
            request,
            *args,
            **kwargs
        )

    @action(
        methods=["GET"],
        detail=True,
        description="Retrieve memberships in the family group",
        name="family_members",
    )
    def members(self, request, pk=None):
        """Retrieve all memberships in the family group."""
        try:
            family_group = models.FamilyGroup.objects.get(
                id=pk, members__user_id=request.ft_user.id
            )
        except models.FamilyGroup.DoesNotExist:
            raise utils.HTTPException(
                detail="Family group not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        family_members = FamilyMembershipInFamilyGroupSerializer(
            family_group.members.all(),
            many=True
        )
        return Response(
            {"data": family_members.data}
        )


@extend_schema(tags=["Family Memberships"])
class FamilyMembershipViewSet(viewsets.ModelViewSet):
    """A collection of endpoints for Family Membership operations."""

    http_method_names = ("get", "post", "put", "delete")
    serializer_class = FamilyMembershipSerializer
    permission_classes = (permissions.IsAuthenticatedWithUserService,)

    def get_queryset(self):
        user = self.request.ft_user
        return models.FamilyMembership.objects.filter(user_id=user.id)

    @extend_schema(
        summary="Retrieve all family memberships",
        responses=OpenApiResponse(
            response=FamilyMembershipSerializer,
            description="Family Memberships retrieved successfully",
        ),
    )
    def list(self, request, *args, **kwargs):
        """List all family memberships."""
        return super().list(
            request,
            *args,
            **kwargs
        )

    @extend_schema(
        summary="Retrieve a single family membership",
        responses=OpenApiResponse(
            response=FamilyMembershipSerializer,
            description="Family Membership retrieved successfully",
        ),
    )
    def retrieve(self, request, *args, **kwargs):
        """Retrieve a single family membership."""
        return super().retrieve(
            request,
            *args,
            **kwargs
        )

    @extend_schema(
        summary="Create a new family membership",
        responses=OpenApiResponse(
            response=FamilyMembershipSerializer,
            description="Family Membership created successfully",
        ),
        request=OpenApiRequest(
            request=FamilyMembershipSerializer,
        ),
    )
    def create(self, request, *args, **kwargs):
        """Create a new family membership."""
        return super().create(
            request,
            *args,
            **kwargs
        )

    @extend_schema(
        summary="Update an existing family membership",
        responses=OpenApiResponse(
            description="Family Membership updated successfully",
            response=FamilyMembershipSerializer,
        ),
        request=OpenApiRequest(
            request=FamilyMembershipSerializer,
        ),
    )
    def update(self, request, *args, **kwargs):
        """Update an existing family membership."""
        return super().update(
            request,
            *args,
            **kwargs
        )

    @extend_schema(
        summary="Delete an existing family membership",
        responses=OpenApiResponse(
            response=None,
            description="Family Membership deleted successfully",
        ),
    )
    def destroy(self, request, *args, **kwargs):
        """Deletes an existing family membership."""
        return super().destroy(
            request,
            *args,
            **kwargs
        )
