import contextlib

from rest_framework.renderers import JSONRenderer


class CustomJSONRenderer(JSONRenderer):
    """A custom renderer for JSON responses."""

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Render the data into a response based on the HTTP method and status
        code.

        Args:
            data (dict): The data to be rendered.
            accepted_media_type (str): The accepted media type.
            renderer_context (dict): Additional context for rendering.

        Returns:
            The rendered response based on the HTTP method and
            status code.
        """

        view = renderer_context.get("view", None)
        http_method = view.request.method if view else "GET"
        if renderer_context and "response" in renderer_context:
            status_code = renderer_context["response"].status_code
        else:
            status_code = 200  # Assume success by default

        if http_method == "GET":
            action = "retrieved"
        elif http_method == "POST":
            action = "created"
        elif http_method in ("PUT", "PATCH"):
            action = "updated"
        elif http_method == "DELETE" and status_code == 204:
            return super().render(None, accepted_media_type, renderer_context)
        else:
            action = "processed"

        basename = "Data"
        if view:
            with contextlib.suppress(AttributeError):
                detail = view.detail
                if not detail and action != "created":
                    basename = f"{view.basename}s".title()
                else:
                    basename = view.basename.title()
        data_name = basename.lower()

        message = "An error occurred"
        if status_code >= 500:
            message = "An error occurred on the server"
        elif status_code >= 400:
            message = "An error occurred in the request"
        elif status_code >= 300:
            message = "Request redirected to another resource"
        elif status_code >= 200:
            message = f"{basename} {action} successfully"

        success = status_code < 300

        response_data = {
            "message": message,
            "status_code": status_code,
            "success": success,
        }

        if data:
            temp = data.get("data", {})
            if isinstance(temp, list):
                response_data["metadata"] = data.get("metadata", None)
            if status_code < 400:
                response_data[data_name] = data.pop("data", data)
            else:
                response_data["errors"] = data

        return super().render(
            response_data, accepted_media_type, renderer_context
        )
