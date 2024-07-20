"""
This module defines the middleware to perform user authentication
verification. The user data is saved in the `request` object as a Python
dictionary with the name `ft_user` (FamTrust user)
"""

from django.http import JsonResponse
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from django.utils.translation import gettext_lazy as _
from rest_framework import status

from famtrust import utils


class ValidateUserMiddleware(MiddlewareMixin):
    """Validates that the access token of a user is valid."""

    @staticmethod
    def process_request(request):
        """Validates that the access token of a user is valid."""

        # Allow the API status documentation to be viewable without
        # authentication
        allowed_routes = (
            reverse("api-status"),
            reverse("swagger"),
            reverse("redoc"),
            reverse("schema"),
            reverse("api-root"),
        )
        if any(
            path
            for path in allowed_routes
            if request.path.rstrip("/") == path.rstrip("/")
        ):
            return

        token = request.headers.get("Authorization")

        if not token:
            return JsonResponse(
                data={
                    "error": _("Authorization token required"),
                    "status_code": status.HTTP_401_UNAUTHORIZED,
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not utils.is_valid_token(token=token):
            return JsonResponse(
                data={
                    "error": _("Invalid or expired token"),
                    "status_code": status.HTTP_401_UNAUTHORIZED,
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if "X-User-Id" not in request.headers:
            return JsonResponse(
                data={
                    "error": _("'X-User-Id' must be set in request header"),
                    "status_code": status.HTTP_400_BAD_REQUEST,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = utils.fetch_user_data(
            token=token, user_id=request.headers.get("X-User-Id")
        )
        request.ft_user = user
