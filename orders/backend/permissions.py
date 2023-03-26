from rest_framework.permissions import BasePermission


class IsShopOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.user
    

class IsShop(BasePermission):
    def has_permission(self, request, view):
        return request.user.type == 'shop'
