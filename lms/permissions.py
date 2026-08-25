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
        # Проверяем, есть ли у объекта поле owner
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        return False


class IsOwnerOrModerator(permissions.BasePermission):
    """
    Проверка, что пользователь является владельцем объекта или модератором.
    """
    
    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name='Модератор').exists():
            return True
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        return False
