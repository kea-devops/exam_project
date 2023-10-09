from django.core.exceptions import BadRequest, PermissionDenied
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.http import QueryDict

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
            if not request.user.is_authenticated:
                return redirect('/accounts/login')
            elif not request.user.is_staff:
                raise PermissionDenied("You do not have access to this resource")
            
        # Customer Route Authorization
        elif re.match(r'^/customer($|/|\?)', request.path):
            if not request.user.is_authenticated:
                return redirect('/accounts/login')
            elif request.user.is_staff:
                raise PermissionDenied("You do not have access to this resource")