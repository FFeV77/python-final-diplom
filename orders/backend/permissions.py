from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsShopOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.user


class IsOrderUserOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.user_id


class IsShop(BasePermission):
    def has_permission(self, request, view):
        return request.user.type == 'shop'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            if obj.user == request.user:
                return True
            else:
                return False
