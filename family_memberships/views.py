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
from rest_framework.response import Response

from .models import FamilyGroup, Membership
from .serializers import FamilyGroupSerializer, MembershipSerializer


@extend_schema(tags=["Family Groups"], auth=[])
class FamilyGroupViewSet(viewsets.ModelViewSet):
    """A collection of endpoints for FamilyGroup operations."""

    http_method_names = ("get", "post", "put", "delete")
    queryset = FamilyGroup.objects.all()
    serializer_class = FamilyGroupSerializer

    @extend_schema(
        summary="Retrieve all family groups",
        responses=OpenApiResponse(
            response=FamilyGroupSerializer,
            description="Family Groups retrieved successfully",
        ),
    )
    def list(self, request, *args, **kwargs):
        """
        This endpoint returns all family groups.
        """
        family_groups = self.get_queryset()
        if not family_groups.exists():
            response_data = {
                'status': 404,
                'success': False,
                'message': 'No family groups found'
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(family_groups, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

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
        """
        This endpoint is responsible for creating a new family group.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                'status': 201,
                'success': True,
                'message': 'Family group successfully created',
                'data': serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        response_data = {
            'status': 400,
            'success': False,
            'message': 'Failure while creating a family group',
            'errors': serializer.errors
        }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

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
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer

    @extend_schema(
        summary="Retrieve all memberships",
        responses=OpenApiResponse(
            response=MembershipSerializer,
            description="Memberships retrieved successfully",
        ),
    )
    def list(self, request, *args, **kwargs):
        """
        This endpoint returns all memberships.
        """
        memberships = self.get_queryset()
        if not memberships.exists():
            response_data = {
                'status': 404,
                'success': False,
                'message': 'No memberships found'
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(memberships, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

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
        """
        This endpoint is responsible for creating a new membership.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                'status': 201,
                'success': True,
                'message': 'Membership successfully created',
                'data': serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        response_data = {
            'status': 400,
            'success': False,
            'message': 'Failure while creating a member',
            'errors': serializer.errors
        }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

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
