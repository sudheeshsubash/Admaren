from rest_framework.permissions import BasePermission
from django.contrib.auth.models import User



class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return User.objects.filter(username=request.user)[0].is_superuser
        return False
    
    
class UserPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return not User.objects.filter(username=request.user)[0].is_superuser
        return False