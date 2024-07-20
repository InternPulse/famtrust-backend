from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

api_prefix = f"api/{settings.API_VERSION}"


@extend_schema(
    summary="Get API status",
    tags=["API Status"],
    auth=[],
    responses=(
        OpenApiResponse(
            description="API is running",
            response=dict[str, str],
            examples=[
                OpenApiExample(
                    name="API status",
                    value={
                        "message": "Data retrieved successfully",
                        "status_code": 200,
                        "success": True,
                        "data": {"status": "OK"},
                    },
                )
            ],
        )
    ),
)
@api_view(["GET"])
def api_status(_):
    """Returns 'OK' if the API is up and running."""
    return Response(data={"status": "OK"}, status=status.HTTP_200_OK)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/status/", api_status, name="api-status"),
    path(
        f"{api_prefix}/schema/", SpectacularAPIView.as_view(), name="schema"
    ),
    path(
        f"{api_prefix}/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger",
    ),
    path(
        f"{api_prefix}/docs/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path(f"{api_prefix}/", include("accounts_transactions.urls")),
    path(f"{api_prefix}/", include("family_memberships.urls")),
]
