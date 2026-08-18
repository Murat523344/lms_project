from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    """
    Проверка, что пользователь является модератором.
    """
    
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Модератор').exists()


class IsOwner(permissions.BasePermission):
    """
    Проверка, что пользователь является владельцем объекта.
    """
    
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsOwnerOrModerator(permissions.BasePermission):
    """
    Проверка, что пользователь является владельцем объекта или модератором.
    """
    
    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name='Модератор').exists():
            return True
        return obj.owner == request.user


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Проверка, что пользователь является владельцем объекта или запрос только на чтение.
    """
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
