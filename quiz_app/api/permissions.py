import rest_framework.permissions as permissions

class isCreatorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow creators of an object to edit or delete it.
    """
    def has_permission(self, request, view): 
        return True 

    def has_object_permission(self, request, view, obj):
        if request.method in [permissions.SAFE_METHODS, 'PATCH', 'PUT', 'DELETE']:
            return obj.creator == request.user