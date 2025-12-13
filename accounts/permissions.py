from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    message = 'siz admin emassiz'

    def has_permission(self, request, view):
        return request.user and request.user.is_admin
    
class IsManager(BasePermission):
    message = 'siz manager emassiz'

    def has_permission(self, request, view):
        return request.user and request.user.is_manager

class IsUser(BasePermission):
    message = 'siz user emassiz '

    def has_permission(self, request, view):
        return request.user and request.user.is_user
    

class IsStaff(BasePermission):
    massage = 'siz staff massiz'

    def has_permission(self, request, view):
        return request.user and not (request.user.is_admin or request.user.is_manager)


