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

from accounts import serializers
from accounts.models import (
    FamilyAccount,
    FundRequest,
    SubAccount,
)
from famtrust import (
    permissions,
    utils,
)


@extend_schema(tags=["Sub Accounts"], auth=[])
class SubAccountViewSet(viewsets.ModelViewSet):
    """A collection of endpoints for SubAccount operations."""

    http_method_names = ("get", "post", "put", "delete")
    serializer_class = serializers.SubAccountSerializer
    queryset = SubAccount.objects.none()
    search_fields = ("name", "type")
    filterset_fields = ("name", "is_active")
    permission_classes = (
        permissions.IsAuthenticatedWithUserService,
        permissions.IsAccountOwnerOrCreator,
    )

    def get_queryset(self):
        """
        Return sub-accounts for the current user's family accounts.
        """
        user = self.request.ft_user
        family_groups = utils.get_family_group_ids(user_id=user.get("id"))
        family_accounts = FamilyAccount.objects.filter(
            family_group__id__in=family_groups
        ).values_list("id", flat=True)
        queryset = SubAccount.objects.filter(
            family_account__id__in=family_accounts
        )
        return queryset

    @extend_schema(
        summary="Retrieve all sub-accounts",
        responses=OpenApiResponse(
            response=serializers.SubAccountSerializer,
            description="Sub Accounts retrieved successfully",
        ),
    )
    def list(self, request, *args, **kwargs):
        """
        This endpoint returns all sub-accounts.
        """
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Retrieve a single sub-account",
        responses=OpenApiResponse(
            response=serializers.SubAccountSerializer,
            description="Sub Account retrieved successfully",
        ),
    )
    def retrieve(self, request, *args, **kwargs):
        """Retrieve a single sub-account."""
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Create a new sub-account",
        responses=OpenApiResponse(
            response=serializers.SubAccountSerializer,
            description="Sub Account created successfully",
        ),
        request=OpenApiRequest(
            request=serializers.SubAccountSerializer,
        ),
    )
    def create(self, request, *args, **kwargs):
        """Create a new sub-account."""
        user = self.request.ft_user
        self.request.data["created_by"] = user.id
        token = request.headers.get("Authorization")

        if owner_id := request.data.get("owner_id"):
            utils.fetch_user_data(token=token, user_id=owner_id)
            request.data["owner_id"] = owner_id
        else:
            raise utils.HTTPException(
                detail=_("owner_id must be provided"),
                code="required",
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Update an existing sub-account",
        responses=OpenApiResponse(
            description="Sub Account updated successfully",
            response=serializers.SubAccountSerializer,
        ),
        request=OpenApiRequest(
            request=serializers.SubAccountSerializer,
        ),
    )
    def update(self, request, *args, **kwargs):
        """Update an existing sub-account."""
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete an existing sub-account",
        responses=OpenApiResponse(
            response=None,
            description="Sub Account deleted successfully",
        ),
    )
    def destroy(self, request, *args, **kwargs):
        """Deletes an existing sub-account."""
        return super().destroy(request, *args, **kwargs)


@extend_schema(tags=["Family Accounts"], auth=[])
class FamilyAccountViewSet(viewsets.ModelViewSet):
    """A collection of endpoints for FamilyAccount operations."""

    http_method_names = ("get", "post", "put", "delete")
    queryset = FamilyAccount.objects.all()
    serializer_class = serializers.FamilyAccountSerializer
    permission_classes = (
        permissions.IsAuthenticatedWithUserService,
        permissions.IsAccountOwnerOrCreator,
    )

    @extend_schema(
        summary="Retrieve all family accounts",
        responses=OpenApiResponse(
            response=serializers.FamilyAccountSerializer,
            description="Family Accounts retrieved successfully",
        ),
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Retrieve a single family account",
        responses=OpenApiResponse(
            response=serializers.FamilyAccountSerializer,
            description="Family Account retrieved successfully",
        ),
    )
    def retrieve(self, request, *args, **kwargs):
        """Retrieve a single family account."""
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Create a new family account",
        responses=OpenApiResponse(
            response=serializers.FamilyAccountSerializer,
            description="Family Account created successfully",
        ),
        request=OpenApiRequest(
            request=serializers.FamilyAccountSerializer,
        ),
    )
    def create(self, request, *args, **kwargs):
        """Create a new family account.

        This endpoint is only accessible to admin users or users with the
        appropriate permissions. The sole purpose of this endpoint is to
        create new family accounts for a specific family group.

        Everyone who is in the family group that this account is created for
        can withdraw of interact with the account. A default family account
        will be created when a user is first registered on the platform. If
        no further accounts are created, everyone will be allowed to interact
        with that account. For finer control and access, consider creating
        groups and assigning specific accounts to them.
        """
        user = request.ft_user
        request.data = request.data["created_by"] = user.get("id")

        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Update an existing family account",
        responses=OpenApiResponse(
            description="Family Account updated successfully",
            response=serializers.FamilyAccountSerializer,
        ),
        request=OpenApiRequest(
            request=serializers.FamilyAccountSerializer,
        ),
    )
    def update(self, request, *args, **kwargs):
        """Update an existing family account."""
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete an existing family account",
    )
    def destroy(self, request, *args, **kwargs):
        """Deletes an existing family account."""
        return super().destroy(request, *args, **kwargs)


@extend_schema(tags=["Accounts"], auth=[])
class AccountViewSet(viewsets.GenericViewSet):
    """
    This is useful for requests that need both sub-accounts and
    family accounts in a single response. The response is paginated and then
    returned to the user.

    If you need to perform other operations outside listing the accounts
    for a particular user, use the specific endpoint collections.
    """

    permission_classes = [permissions.IsAuthenticatedWithUserService]

    def get_queryset(self):
        """
        Returns both SubAccount and FamilyAccount query sets.
        """
        user = self.request.ft_user

        sub_accounts = SubAccount.objects.filter(owner_id=user.get("id"))
        family_group_ids = utils.get_family_group_ids(user_id=user.get("id"))

        if family_group_ids:
            family_accounts = FamilyAccount.objects.filter(
                family_group__id=family_group_ids
            )
        else:
            family_accounts = FamilyAccount.objects.none()

        return sub_accounts, family_accounts

    @extend_schema(
        summary="List all family and sub accounts",
        operation_id="list_all_accounts",
    )
    def list(self, request):
        """
        Retrieve a paginated list of all sub-accounts and family accounts
        for the current user.

        This is useful for requests that need both sub-accounts and
        family accounts in a single response. The response is paginated and
        then returned to the user.

        If you need to perform other operations outside listing the accounts
        for a particular user, use the specific endpoint collections.
        """
        sub_accounts, family_accounts = self.get_queryset()
        return self.paginate_accounts(
            sub_accounts=sub_accounts,
            family_accounts=family_accounts,
            request=request,
        )

    def paginate_accounts(self, *, sub_accounts, family_accounts, request):
        """
        Paginates both sub_accounts and family_accounts and returns a
        paginated response.
        """
        paginator = self.pagination_class()
        paginated_sub_accounts = paginator.paginate_queryset(
            sub_accounts, request
        )
        paginated_family_accounts = paginator.paginate_queryset(
            family_accounts, request
        )

        sub_accounts_serializer = serializers.SubAccountSummarySerializer(
            instance=paginated_sub_accounts,
            many=True,
            context={"request": request},
        )
        family_accounts_serializer = (
            serializers.FamilyAccountSummarySerializer(
                instance=paginated_family_accounts,
                many=True,
                context={"request": request},
            )
        )

        data = {
            "sub_accounts": sub_accounts_serializer.data,
            "family_accounts": family_accounts_serializer.data,
        }

        return paginator.get_paginated_response(data)


@extend_schema(tags=["Fund Requests"], auth=[])
class FundRequestViewSet(viewsets.ModelViewSet):
    """A collection of endpoints for fund requests."""

    http_method_names = ("get", "post", "put", "delete")
    queryset = FundRequest.objects.all()
    serializer_class = serializers.FundRequestSerializer
    permission_classes = (
        permissions.IsAuthenticatedWithUserService,
        permissions.IsFundRequestOwnerOrCreator,
    )

    def get_queryset(self):
        """Retrieves all fund requests for the current user."""
        user = self.request.ft_user
        return FundRequest.objects.filter(request_by=user.get("id"))

    @extend_schema(
        summary="Retrieve all fund requests",
        responses=OpenApiResponse(
            response=serializers.FundRequestSerializer,
            description="Fund Requests retrieved successfully",
        ),
    )
    def list(self, request, *args, **kwargs):
        """List all fund requests."""
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Retrieve a single fund request",
        responses=OpenApiResponse(
            response=serializers.FundRequestSerializer,
            description="Fund Request retrieved successfully",
        ),
    )
    def retrieve(self, request, *args, **kwargs):
        """Retrieve a single fund request."""
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Create a new fund request",
        responses=OpenApiResponse(
            response=serializers.FundRequestSerializer,
            description="Fund Request created successfully",
        ),
        request=OpenApiRequest(
            request=serializers.FundRequestSerializer,
        ),
    )
    def create(self, request, *args, **kwargs):
        """
        This endpoint is responsible for creating a new fund request in
        the system.
        It accepts a request object, which contains the necessary data for
        creating a new fund request, and any additional arguments and
        keyword arguments.
        """
        user = request.ft_user
        data = request.data

        data["requested_by"] = user.get("id")

        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Update an existing fund request",
        responses=OpenApiResponse(
            description="Fund Request updated successfully",
            response=serializers.FundRequestSerializer,
        ),
        request=OpenApiRequest(
            request=serializers.FundRequestSerializer,
        ),
    )
    def update(self, request, *args, **kwargs):
        """Update an existing fund request."""
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete an existing fund account.",
    )
    def destroy(self, request, *args, **kwargs):
        """Deletes an existing fund request."""
        return super().destroy(request, *args, **kwargs)
