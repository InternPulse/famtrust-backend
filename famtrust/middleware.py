"""
This module defines the middleware to perform user authentication
verification. The user data is saved in the `request` object as a Pydantic
model with the name `ft_user` (FamTrust user)

Example usage:

```python

user = request.ft_user
print(user.id)

if user.isAdmin:
    print("User is an admin")
```
"""
import logging

from django.http import JsonResponse
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from django.utils.translation import gettext_lazy as _
from rest_framework import status

from famtrust import models, utils

logger = logging.getLogger(__name__)


class ValidateUserMiddleware(MiddlewareMixin):
    """Validates that the access token of a user is valid."""

    @staticmethod
    def process_request(request):
        """Validates that the access token of a user is valid."""

        logger.debug("Processing request %s", request.path)
        # Allow the API status documentation to be viewable without
        # authentication
        if request.path.startswith(reverse("admin:index")):
            return

        if request.path.startswith("/static") or request.path.startswith(
            "/favicon"
        ):
            return

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

        valid_token, data = utils.is_valid_token(token=token)
        if not valid_token:
            return JsonResponse(
                data={
                    "error": _("Invalid or expired token"),
                    "status_code": status.HTTP_401_UNAUTHORIZED,
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not data:
            raise utils.HTTPException(
                detail="Server error occurred",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        user_data = data.get("user")
        admin = user_data.get("role").get("id") == "admin"

        request.ft_user = models.User(**user_data, isAdmin=admin)
