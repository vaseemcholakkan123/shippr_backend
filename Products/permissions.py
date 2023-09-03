from rest_framework.permissions import BasePermission
from django.contrib.auth.models import AnonymousUser

class IsVendorOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return False

        elif request.method == "GET":
            return True
        else:
            return request.user.is_vendor


    def has_object_permission(self, request, view, obj):
        return obj.vendor == request.user
