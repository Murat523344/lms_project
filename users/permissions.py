from rest_framework import permissions


class IsOwnerOrStaff(permissions.BasePermission):
    """
    Проверка, что пользователь является владельцем объекта или администратором.
    """
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj == request.user
