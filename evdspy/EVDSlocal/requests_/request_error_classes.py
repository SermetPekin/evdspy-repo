from evdspy.EVDSlocal.messages.error_classes import ApiKeyNotSetError


class BaseException_Request(Exception):
    """BaseException_Request"""


class Req_NotFound(BaseException_Request):
    """Req_NotFound"""


class Req_Unauthorized(BaseException_Request):
    """Req_NotFound"""


class Req_Forbidden(BaseException_Request):
    """Req_NotFound"""


class Req_BadRequest(BaseException_Request):
    """Req_NotFound"""


class Req_TooMany(BaseException_Request):
    """Req_TooMany"""


class Internal(BaseException_Request):
    """Internal"""

class Bad_Gateway(BaseException_Request):
    """Bad_Gateway"""


class ServiceUnavailable(BaseException_Request):
    """ServiceUnavailable"""


class GatewayNotImplemented(BaseException_Request):
    """GatewayNotImplemented"""


REQUEST_ERROR_CODES = {
        400: Req_BadRequest,
        401: Req_Unauthorized,
        403: Req_Forbidden,
        404: Req_NotFound,
        429: Req_TooMany,
        500: Internal,
        502: Bad_Gateway,
        503: ServiceUnavailable,
        504: GatewayNotImplemented
}
