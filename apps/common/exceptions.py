from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError

def custom_exception_handler(exc, context):
    # Call DRF's default exception handler first to get the standard error response.
    response = exception_handler(exc, context)

    if response is not None:
        # Check if the response data is already formatted
        if isinstance(response.data, dict) and "success" in response.data:
            return response

        message = "An error occurred."
        errors = response.data

        if isinstance(exc, ValidationError):
            message = "Validation failed."
            # If errors is a list, normalize it to a dictionary
            if isinstance(errors, list):
                errors = {"non_field_errors": errors}
        else:
            if isinstance(errors, dict) and "detail" in errors:
                message = errors["detail"]

        response.data = {
            "success": False,
            "message": message,
            "errors": errors
        }

    return response
