import os

from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.routers import APIRootView, DefaultRouter
from rest_framework.views import exception_handler


class FamTrustAPI(APIRootView):
    """
    A view which returns a list of all existing endpoints, not just the ones
    on this router.
    """

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        base_names = [
            "account-list",
            "transaction-list",
            "family-group-list",
            "membership-list",
        ]

        for basename in base_names:
            relative_url = f"/api/{settings.API_VERSION}{reverse(basename)}"
            absolute_url = request.build_absolute_uri(relative_url)
            key = absolute_url.split("/")[-1]
            response.data[key] = absolute_url

        relative_url = reverse(
            "api-status",
            args=args,
            kwargs=kwargs,
        )

        full_url = request.build_absolute_uri(relative_url)
        response.data["status"] = full_url

        return response


class CustomDefaultRouter(DefaultRouter):
    APIRootView = FamTrustAPI

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.trailing_slash = "/?"


class HTTPException(APIException):
    """Handles all HTTP Exceptions that occur during API requests."""

    def __init__(self, detail=None, code=None, status_code=None):
        super().__init__(detail, code)
        self.status_code = status_code


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        response.data["status_code"] = response.status_code

        if response.status_code == 404:
            response.data["message"] = "The requested resource was not found"

    return response


class Pagination(PageNumberPagination):
    """
    A custom pagination class that includes links to the next and previous
    pages.

    Attributes:
        page_size (int): The number of items to include on each page.
        page_size_query_param (str): The query parameter to control the page
        size.
        max_page_size (int): The maximum allowed page size.
        page_query_param (str): The query parameter to control the current
        page number.
        last_page_strings (tuple): A tuple of strings to represent the last
        page in the pagination response.
    """

    page_query_param = "page"
    page_size_query_param = "page_size"
    last_page_strings = ("last", "end")
    try:
        max_page_size = min(int(os.environ.get("MAX_PAGE_SIZE")), 100)
    except ValueError:
        max_page_size = 100

    def get_page_size(self, request):
        """Returns the page size."""
        size = request.query_params.get(self.page_size_query_param, None)
        if not size:
            return self.page_size

        try:
            size = int(size)
        except ValueError as e:
            raise HTTPException(
                detail="Page size must be an integer",
                code="invalid_page_size",
                status_code=status.HTTP_400_BAD_REQUEST,
            ) from e

        if size <= 0 or size > self.max_page_size:
            raise HTTPException(
                detail="Page size must be a positive integer and not exceed "
                f"{self.max_page_size}",
                code="invalid_page_size",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        return super().get_page_size(request)

    def get_paginated_response(self, data) -> Response:
        """
        Get the paginated response with links to the next and previous pages.

        Args:
            data (list): The paginated data.

        Returns:
            dict: The paginated response containing links, count, total pages,
            current page, and results.
        """
        return Response(
            data={
                "metadata": {
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                    "count": len(data),
                    "total_pages": self.page.paginator.num_pages,
                    "current_page": self.page.number,
                },
                "data": data,
            }
        )

    def get_paginated_response_schema(self, schema):
        """Schema for paginated response."""
        return {
            "type": "object",
            "properties": {
                "metadata": {
                    "type": "object",
                    "required": [
                        "count",
                        "data",
                        "total_pages",
                        "current_page",
                    ],
                    "properties": {
                        "next": {
                            "type": "string",
                            "nullable": True,
                            "format": "uri",
                            "example": (
                                "https://famtrust.com/api/v1/accounts/?"
                                f"{self.page_query_param}=4"
                            ),
                        },
                        "previous": {
                            "type": "string",
                            "nullable": True,
                            "format": "uri",
                            "example": (
                                "https://famtrust.com/api/v1/accounts/?"
                                f"{self.page_query_param}=2"
                            ),
                        },
                        "count": {"type": "integer", "example": 100},
                        "total_pages": {"type": "integer", "example": 5},
                        "current_page": {"type": "integer", "example": 3},
                    },
                },
                "data": schema,
            },
        }
