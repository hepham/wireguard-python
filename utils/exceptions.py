from flask import jsonify
from werkzeug.exceptions import HTTPException

class APIError(Exception):
    """Base class cho các exception API."""
    def __init__(self, message: str, status_code: int = 400, payload: dict = None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self) -> dict:
        """Chuyển exception thành dictionary để trả về JSON response."""
        error_dict = self.payload or {}
        error_dict["message"] = self.message
        error_dict["status"] = "error"
        return error_dict

class InvalidRequestError(APIError):
    """Exception cho request không hợp lệ (400 Bad Request)."""
    def __init__(self, message: str = "Invalid request", payload: dict = None):
        super().__init__(message, 400, payload)

class UnauthorizedError(APIError):
    """Exception cho truy cập trái phép (401 Unauthorized)."""
    def __init__(self, message: str = "Unauthorized", payload: dict = None):
        super().__init__(message, 401, payload)

class ForbiddenError(APIError):
    """Exception cho truy cập bị cấm (403 Forbidden)."""
    def __init__(self, message: str = "Forbidden", payload: dict = None):
        super().__init__(message, 403, payload)

class NotFoundError(APIError):
    """Exception cho resource không tồn tại (404 Not Found)."""
    def __init__(self, message: str = "Resource not found", payload: dict = None):
        super().__init__(message, 404, payload)

class InternalServerError(APIError):
    """Exception cho lỗi server (500 Internal Server Error)."""
    def __init__(self, message: str = "Internal server error", payload: dict = None):
        super().__init__(message, 500, payload)

def register_error_handlers(app):
    """Đăng ký error handlers cho Flask app."""
    # Xử lý các exception tùy chỉnh
    @app.errorhandler(APIError)
    def handle_api_error(error: APIError):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    # Xử lý các HTTPException mặc định của Werkzeug/Flask
    @app.errorhandler(HTTPException)
    def handle_http_exception(error: HTTPException):
        response = jsonify({
            "status": "error",
            "message": error.description,
        })
        response.status_code = error.code
        return response

    # Xử lý mọi exception không được bắt
    @app.errorhandler(Exception)
    def handle_generic_exception(error: Exception):
        # Log lỗi ở đây (nếu cần)
        response = jsonify({
            "status": "error",
            "message": "Internal server error",
        })
        response.status_code = 500
        return response