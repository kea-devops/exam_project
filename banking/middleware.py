from django.http import QueryDict
from django.utils.deprecation import MiddlewareMixin
from django.core.exceptions import BadRequest

class BodyParsingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.method == "PUT" or request.method == "PATCH":
            if request.content_type == "application/x-www-form-urlencoded":
                # Handle Form payload
                if request.method == 'PUT':
                    request.PUT = QueryDict(request.body)
                else:
                    request.PATCH = QueryDict(request.body)
            else:
                raise BadRequest("Unsupported media type")