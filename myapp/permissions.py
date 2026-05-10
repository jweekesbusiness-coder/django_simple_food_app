from rest_framework import permissions

#Custom permission class to allow only owners of an object to edit it, while allowing read-only access to everyone else.
class isOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        #Allow all read only methods
        if request.method in permissions.SAFE_METHODS:
            return True
        
        #Make sure a user only has permission to edit their own objects
        return obj.user == request.user