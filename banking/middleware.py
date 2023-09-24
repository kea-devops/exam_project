from django.http import QueryDict
from django.utils.deprecation import MiddlewareMixin
from django.core.exceptions import BadRequest, PermissionDenied

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

import re
class AuthorizationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        
        # Employee Route Authorization
        if re.match(r'^/employee($|/|\?)', request.path):
            if not request.user.groups.filter(name='employees').exists():
                raise PermissionDenied("You do not have access to this resource")
            
        # Customer Route Authorization
        elif re.match(r'^/customer($|/|\?)', request.path):
            if not request.user.groups.filter(name='customers').exists():
                raise PermissionDenied("You do not have access to this resource")