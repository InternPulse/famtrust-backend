"""
This module defines the middleware to perform user authentication
verification. The user data is saved in the `request` object as a Python
dictionary with the name `ft_user` (FamTrust user)
"""

import logging

from django.http import JsonResponse
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from django.utils.translation import gettext_lazy as _
from rest_framework import status

from famtrust import utils

logger = logging.getLogger(__name__)


class ValidateUserMiddleware(MiddlewareMixin):
    """Validates that the access token of a user is valid."""

    @staticmethod
    def process_request(request):
        """Validates that the access token of a user is valid."""

        logger.debug("Processing request %s", request.path)
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
            or request.path.startswith(reverse("admin:index"))
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

        valid_token, data = utils.is_valid_token(token=token)
        if not valid_token:
            return JsonResponse(
                data={
                    "error": _("Invalid or expired token"),
                    "status_code": status.HTTP_401_UNAUTHORIZED,
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        request.ft_user = data.get("user")
