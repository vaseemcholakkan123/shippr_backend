from rest_framework.permissions import BasePermission
from django.contrib.auth.models import AnonymousUser

class IsVendor(BasePermission):

    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return False

        else:
            return request.user.is_vendor

    def has_object_permission(self, request, view, OrderOBJ):
        return OrderOBJ.product.vendor == request.user